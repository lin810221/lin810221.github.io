import asyncio
import json
import logging
import re
import time
from collections.abc import AsyncIterable
from contextlib import asynccontextmanager
from typing import Annotated
from uuid import uuid4
import anyio
import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, File, Header, Query, Request, Response, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.sse import EventSourceResponse, ServerSentEvent
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .contracts import DocumentIn, DocumentOut, DocumentTitleIn, JobIn, JobOut
from .settings import Settings
from .store import DomainError, Store

log = logging.getLogger('relaydesk')
bearer = HTTPBearer(auto_error=False)


def get_store(request: Request):
    return request.app.state.store


def principal(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], store: Annotated[Store, Depends(get_store)]):
    if credentials is None or credentials.scheme.lower() != 'bearer' or len(credentials.credentials) > 512:
        raise DomainError(401, 'unauthorized')
    return store.identity(credentials.credentials)


def editor(user: Annotated[dict, Depends(principal)]):
    if user['role'] != 'editor':
        raise DomainError(403, 'write_forbidden')
    return user


Identity = Annotated[dict, Depends(principal)]
Editor = Annotated[dict, Depends(editor)]
Database = Annotated[Store, Depends(get_store)]


def expected_version(if_match: Annotated[str | None, Header(max_length=14)] = None):
    if if_match is None:
        raise DomainError(428, 'if_match_required')
    if not re.fullmatch(r'"[1-9][0-9]{0,9}"', if_match):
        raise DomainError(422, 'invalid_if_match')
    return int(if_match[1:-1])


def job_access(job_id: str, user: Identity, store: Database):
    store.job(user['tenant'], job_id)
    return user


class PrivateEventSourceResponse(EventSourceResponse):
    def __init__(self, content, status_code: int = 200, headers=None, media_type=None, background=None):
        headers = dict(headers or {}) | {'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'}
        super().__init__(content, status_code=status_code, headers=headers, media_type=media_type, background=background)


def create_app(settings=None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        store = Store(settings.database_path)
        try:
            await anyio.to_thread.run_sync(store.migrate)
            async with httpx.AsyncClient(timeout=httpx.Timeout(5, connect=2), limits=httpx.Limits(max_connections=8, max_keepalive_connections=4), follow_redirects=False, trust_env=False) as client:
                app.state.store, app.state.http, app.state.ready = store, client, True
                app.state.audit_count = 0
                yield
        finally:
            app.state.ready = False
            await anyio.to_thread.run_sync(store.engine.dispose)

    app = FastAPI(title='RelayDesk AI Backend', version='1.0.0', lifespan=lifespan, max_body_size=settings.max_body_bytes)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_methods=['GET', 'POST', 'PATCH', 'DELETE'], allow_headers=['Authorization', 'Content-Type', 'Idempotency-Key', 'Last-Event-ID', 'If-Match'], expose_headers=['X-Request-ID', 'ETag'], allow_credentials=False)

    @app.middleware('http')
    async def request_id(request, call_next):
        supplied = request.headers.get('X-Request-ID', '')
        request.state.request_id = supplied if re.fullmatch(r'[A-Za-z0-9_-]{1,64}', supplied) else uuid4().hex
        start = time.perf_counter()
        response = await call_next(request)
        response.headers['X-Request-ID'] = request.state.request_id
        # Never log query strings, input bodies, authorization or document text.
        route = request.scope.get('route')
        log.info('request id=%s route=%s status=%d duration_ms=%.2f', request.state.request_id, getattr(route, 'path', 'unmatched'), response.status_code, (time.perf_counter() - start) * 1000)
        return response

    @app.exception_handler(DomainError)
    async def domain_error(request, error):
        headers = {'WWW-Authenticate': 'Bearer'} if error.status == 401 else None
        return JSONResponse({'error': {'code': error.code, 'request_id': request.state.request_id}}, status_code=error.status, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, error):
        # Pydantic's raw errors can include rejected secrets in input/ctx.
        details = [{'location': list(x['loc']), 'type': x['type']} for x in error.errors()]
        return JSONResponse({'error': {'code': 'invalid_request', 'details': details, 'request_id': request.state.request_id}}, status_code=422)

    @app.get('/health/live')
    def live():
        return {'status': 'alive'}

    @app.get('/health/ready')
    def ready(store: Database):
        with store.engine.connect() as connection:
            from sqlalchemy import text
            connection.execute(text('SELECT 1'))
        return {'status': 'ready'}

    router = APIRouter(prefix='/api/v1')

    @router.post('/documents', response_model=DocumentOut, status_code=201)
    def add_document(value: DocumentIn, user: Editor, store: Database):
        return store.add_document(user['tenant'], value.title, value.text)

    @router.get('/documents', response_model=list[DocumentOut])
    def documents(user: Identity, store: Database, after: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=1, le=50)] = 20):
        return store.documents(user['tenant'], after, limit)

    @router.get('/documents/{document_id}', response_model=DocumentOut)
    def document(document_id: int, response: Response, user: Identity, store: Database):
        value = store.document(user['tenant'], document_id)
        response.headers['ETag'] = '"' + str(value['version']) + '"'
        return value

    @router.patch('/documents/{document_id}', response_model=DocumentOut)
    def edit_document(document_id: int, value: DocumentTitleIn, response: Response, user: Editor, store: Database, version: Annotated[int, Depends(expected_version)]):
        result = store.change_document(user['tenant'], document_id, version, title=value.title)
        response.headers['ETag'] = '"' + str(result['version']) + '"'
        return result

    @router.delete('/documents/{document_id}', status_code=204)
    def delete_document(document_id: int, user: Editor, store: Database, version: Annotated[int, Depends(expected_version)]):
        store.change_document(user['tenant'], document_id, version, delete=True)
        return Response(status_code=204)

    @router.post('/uploads', response_model=DocumentOut, status_code=201, max_body_size=20_000, form_limits={'max_files': 1, 'max_fields': 0, 'max_part_size': 8192})
    async def upload(user: Editor, store: Database, file: Annotated[UploadFile, File()]):
        try:
            if not (file.filename or '').lower().endswith('.txt') or file.content_type not in {'text/plain', 'application/octet-stream'}:
                raise DomainError(415, 'text_file_required')
            data = await file.read(8193)
            if len(data) > 8192:
                raise DomainError(413, 'file_too_large')
            try:
                value = DocumentIn(title='Uploaded text', text=data.decode('utf-8'))
            except (UnicodeError, ValueError):
                raise DomainError(422, 'invalid_utf8_document') from None
            return await anyio.to_thread.run_sync(store.add_document, user['tenant'], value.title, value.text)
        finally:
            await file.close()

    @router.post('/jobs', response_model=JobOut, status_code=202)
    def submit(value: JobIn, user: Editor, store: Database, idempotency_key: Annotated[str, Header()]):
        return store.submit(user['tenant'], idempotency_key, value)

    @router.get('/jobs/{job_id}', response_model=JobOut)
    def job(job_id: str, user: Identity, store: Database):
        return store.job(user['tenant'], job_id)

    @router.post('/jobs/{job_id}/cancel', response_model=JobOut)
    def cancel(job_id: str, user: Editor, store: Database):
        return store.cancel(user['tenant'], job_id)

    @router.get('/jobs/{job_id}/events', response_class=PrivateEventSourceResponse)
    async def stream(job_id: str, request: Request, user: Annotated[dict, Depends(job_access)], store: Database, last_event_id: Annotated[int, Header(ge=0)] = 0) -> AsyncIterable[ServerSentEvent]:
        # Dependency authorization runs before HTTP 200; sessions close per poll.
        cursor, deadline = last_event_id, asyncio.get_running_loop().time() + settings.stream_seconds
        while True:
            rows = await anyio.to_thread.run_sync(store.events, user['tenant'], job_id, cursor)
            for row in rows:
                cursor = row['id']
                yield ServerSentEvent(id=str(cursor), event=row['event'], data=row['data'])
            state = await anyio.to_thread.run_sync(store.job, user['tenant'], job_id)
            if (state['state'] in {'succeeded', 'failed', 'cancelled'} and len(rows) < 100) or asyncio.get_running_loop().time() >= deadline or await request.is_disconnected():
                break
            await asyncio.sleep(.05)

    @router.get('/documents.ndjson')
    async def ndjson(user: Identity, store: Database) -> AsyncIterable[DocumentOut]:
        rows = await anyio.to_thread.run_sync(store.documents, user['tenant'], 0, 50)
        for row in rows:
            yield DocumentOut.model_validate(row)

    @router.post('/audit-ping', status_code=202)
    def audit_ping(tasks: BackgroundTasks, request: Request, user: Editor):
        def audit():
            request.app.state.audit_count += 1
        tasks.add_task(audit)
        return {'scheduled': True, 'durable': False}

    app.include_router(router)

    @app.websocket('/ws/echo')
    async def websocket(websocket: WebSocket):
        # No tokens in URLs. First frame authenticates after origin validation.
        if websocket.headers.get('origin') not in settings.allowed_origins:
            await websocket.close(code=1008)
            return
        await websocket.accept()
        try:
            async with asyncio.timeout(3):
                value = await websocket.receive_text()
            if len(value) > 256:
                raise ValueError('oversize authentication frame')
            user = await anyio.to_thread.run_sync(app.state.store.identity, value)
            await websocket.send_json({'authenticated': True, 'role': user['role']})
            async with asyncio.timeout(3):
                value = await websocket.receive_text()
            if len(value) > 128:
                raise ValueError('oversize echo')
            await websocket.send_json({'echo': value})
            await websocket.close(code=1000)
        except WebSocketDisconnect:
            pass
        except (DomainError, ValueError, TimeoutError):
            await websocket.close(code=1008)

    return app
