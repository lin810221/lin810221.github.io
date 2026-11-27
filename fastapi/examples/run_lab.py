"""32 observable experiments. Every default run is offline except loopback TCP."""
import argparse
import asyncio
import json
import secrets
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4
import httpx
import jwt
from fastapi.testclient import TestClient
from gateway.api import create_app, principal
from gateway.contracts import JobIn
from gateway.mechanics import async_database_example, create_mechanics_app
from gateway.providers import ExtractiveProvider, OpenAIProvider
from gateway.resilience import TokenBucket, fetch_json, nearest_rank
from gateway.security import decode_access_token
from gateway.settings import Settings
from gateway.store import DomainError, Store
from gateway.worker import InjectedCrash, run_once

TITLES=['HTTP and OpenAPI','Strict input and safe errors','Dependency override','Request identifiers','Lifespan cleanup','Yield scope order','Native dependency concurrency','Async SQLAlchemy query','Real migrations','Tenant boundaries','Token hashing and revocation','Deduplication and keyset pages','Actual multipart upload','Body and form limits','Idempotency and conflict','Concurrent unique-key race','Extractive answer and citations','Evidence abstention','Persistent job reopen','Lease fencing','Queued and running cancellation','SSE replay cursor','Native JSONL','Authenticated WebSocket','Non-durable BackgroundTasks','JWT claims and algorithm','Bounded HTTP retries','Deadline cancellation','Crash before publication','Provider contract through MockTransport','Rate and percentile arithmetic','Real Uvicorn and separate worker']


@contextmanager
def project():
    root = Path(__file__).resolve().parent / '.runtime'
    scratch = root / uuid4().hex
    scratch.mkdir(parents=True)
    app = create_app(Settings(database_path=scratch / 'relay.sqlite3', stream_seconds=.1))
    try:
        with TestClient(app) as client:
            store = app.state.store
            token = store.provision('alpha')
            headers = {'Authorization': 'Bearer ' + token}
            document = client.post('/api/v1/documents', headers=headers, json={'title': 'Policy', 'text': 'Warranty lasts 12 months.\nDelivery takes 7 days.'}).json()
            yield app, client, store, token, headers, document, scratch
    finally:
        assert scratch.resolve().is_relative_to(root.resolve())
        shutil.rmtree(scratch)


def run_lab(number):
    if not 1 <= number <= 32:
        raise ValueError('lab must be 1..32')
    if number == 32:
        from socket_smoke import run
        return run()
    with project() as (app, client, store, token, headers, document, scratch):
        def submit(key='example_001', question='warranty'):
            return store.submit('alpha', key, JobIn(question=question, document_ids=[document['id']]))
        if number == 1:
            return {'health': client.get('/health/live').json(), 'openapi_title': client.get('/openapi.json').json()['info']['title']}
        if number == 2:
            r = client.post('/api/v1/documents', headers=headers, json={'title': 3, 'text': 'private fixture'})
            return {'status': r.status_code, 'error': r.json(), 'input_hidden': 'private fixture' not in r.text}
        if number == 3:
            before = client.get('/api/v1/documents').status_code
            app.dependency_overrides[principal] = lambda: {'tenant': 'alpha', 'role': 'reader'}
            try:
                during = client.get('/api/v1/documents').status_code
            finally:
                app.dependency_overrides.clear()
            return {'before': before, 'override': during, 'restored': client.get('/api/v1/documents').status_code}
        if number == 4:
            r = client.get('/health/live', headers={'X-Request-ID': 'client_001'})
            return {'request_id': r.headers['X-Request-ID'], 'status': r.status_code}
        if number == 5:
            shared = app.state.http
            with TestClient(create_app(Settings(database_path=scratch / 'second.sqlite3'))) as other:
                opened = not other.app.state.http.is_closed
                inner = other.app.state.http
            return {'inside_open': opened, 'after_close': inner.is_closed, 'first_app_independent': not shared.is_closed}
        if number == 6:
            mechanics = create_mechanics_app()
            with TestClient(mechanics) as c:
                c.get('/function'); first = list(mechanics.state.trace); mechanics.state.trace.clear(); c.get('/request')
            return {'function': first, 'request': mechanics.state.trace}
        if number == 7:
            async def concurrent():
                a = create_mechanics_app()
                async with httpx.AsyncClient(transport=httpx.ASGITransport(a), base_url='http://testserver') as c:
                    await asyncio.gather(*(c.get('/limited') for _ in range(8)))
                return {'peak': a.state.peak, 'remaining': a.state.active}
            return asyncio.run(concurrent())
        if number == 8:
            return {'sql_result': asyncio.run(async_database_example())}
        if number == 9:
            from sqlalchemy import text
            store.migrate()
            with store.engine.connect() as connection:
                revision = connection.scalar(text('SELECT version_num FROM alembic_version'))
            return {'revision': revision, 'repeat_upgrade': 'safe'}
        if number == 10:
            other = store.provision('beta')
            r = client.get('/api/v1/documents', headers={'Authorization': 'Bearer ' + other})
            return {'alpha_documents': len(store.documents('alpha')), 'beta_documents': len(r.json())}
        if number == 11:
            from sqlalchemy import select
            from sqlalchemy.orm import Session
            from gateway.models import Credential
            with Session(store.engine) as session:
                hashes = list(session.scalars(select(Credential.digest)))
            store.revoke(token)
            return {'raw_token_stored': token in hashes, 'digest_lengths': [len(x) for x in hashes], 'after_revoke': client.get('/api/v1/documents', headers=headers).status_code}
        if number == 12:
            again = store.add_document('alpha', 'New title', document['text'])
            second = store.add_document('alpha', 'Second', 'Other content')
            path = '/api/v1/documents/' + str(document['id'])
            etag = client.get(path, headers=headers).headers['ETag']
            updated = client.patch(path, headers=headers | {'If-Match': etag}, json={'title': 'Updated policy'})
            stale = client.patch(path, headers=headers | {'If-Match': etag}, json={'title': 'Stale title'})
            deleted = client.delete(path, headers=headers | {'If-Match': updated.headers['ETag']})
            return {'dedup_same_id': again['id'] == document['id'], 'next_page': [x['id'] for x in store.documents('alpha', document['id'], 1)], 'expected_next': second['id'], 'patch': updated.status_code, 'stale_patch': stale.status_code, 'logical_delete': deleted.status_code}
        if number == 13:
            r = client.post('/api/v1/uploads', headers=headers, files={'file': ('policy.txt', b'New policy.', 'text/plain')})
            return {'status': r.status_code, 'document': r.json()}
        if number == 14:
            body = client.post('/api/v1/documents', headers=headers, content=b' ' * 17000)
            files = client.post('/api/v1/uploads', headers=headers, files=[('file', ('a.txt', b'A', 'text/plain')), ('other', ('b.txt', b'B', 'text/plain'))])
            return {'oversize_body': body.status_code, 'too_many_files': files.status_code}
        if number == 15:
            a, b = submit(), submit()
            try:
                submit(question='delivery')
            except DomainError as error:
                return {'same_job': a['id'] == b['id'], 'different_payload': error.code}
        if number == 16:
            with ThreadPoolExecutor(max_workers=4) as pool:
                ids = list(pool.map(lambda _: submit()['id'], range(8)))
            return {'requests': len(ids), 'unique_jobs': len(set(ids))}
        if number in {17, 18}:
            submit(question='warranty' if number == 17 else 'unicorns')
            return asyncio.run(run_once(store))['result']
        if number == 19:
            job = submit()
            reopened = Store(scratch / 'relay.sqlite3')
            try:
                return {'reopened_state': reopened.job('alpha', job['id'])['state']}
            finally:
                reopened.engine.dispose()
        if number == 20:
            submit(); old = store.claim(100); new = store.claim(130)
            try:
                store.finish(old, {'status': 'abstained', 'text': 'No evidence.', 'citations': []}, 131)
            except DomainError as error:
                return {'new_attempt': new['attempt'], 'old_publication': error.code}
        if number == 21:
            a = submit(); queued = store.cancel('alpha', a['id'])
            b = submit('example_002'); claim = store.claim(100); store.cancel('alpha', b['id'])
            result = store.finish(claim, {'status': 'abstained', 'text': 'No evidence.', 'citations': []}, 101)
            return {'queued': queued['state'], 'running': result['state'], 'answer_published': result['result'] is not None}
        if number == 22:
            job = submit(); asyncio.run(run_once(store)); rows = store.events('alpha', job['id'])
            r = client.get('/api/v1/jobs/' + job['id'] + '/events', headers=headers | {'Last-Event-ID': str(rows[0]['id'])})
            return {'status': r.status_code, 'events': [line for line in r.text.splitlines() if line.startswith('event:')]}
        if number == 23:
            r = client.get('/api/v1/documents.ndjson', headers=headers)
            return {'media_type': r.headers['content-type'], 'rows': [json.loads(line) for line in r.text.splitlines()]}
        if number == 24:
            with client.websocket_connect('/ws/echo', headers={'Origin': 'http://localhost:3000'}) as ws:
                ws.send_text(token); auth = ws.receive_json(); ws.send_text('hello'); echo = ws.receive_json()
            return {'authentication': auth, 'reply': echo}
        if number == 25:
            r = client.post('/api/v1/audit-ping', headers=headers)
            return r.json() | {'completed_in_this_process': app.state.audit_count}
        if number == 26:
            key = secrets.token_bytes(64)
            claims = {'sub': 'demo', 'iat': int(time.time()), 'exp': int(time.time()) + 60, 'iss': 'https://issuer.example.test', 'aud': 'relaydesk'}
            encoded = jwt.encode(claims, key, algorithm='HS256')
            return {'verified_subject': decode_access_token(encoded, key)['sub'], 'raw_jwt_printed': False}
        if number == 27:
            calls = []
            def transport(request):
                calls.append(request)
                return httpx.Response(503 if len(calls) == 1 else 200, json={'ready': True})
            async def retry():
                async with httpx.AsyncClient(transport=httpx.MockTransport(transport), base_url='https://service.example.test') as c:
                    return await fetch_json(c, '/health')
            return {'value': asyncio.run(retry()), 'attempts': len(calls)}
        if number == 28:
            cleaned = []
            async def slow(request):
                try:
                    await asyncio.sleep(1)
                finally:
                    cleaned.append(True)
            async def deadline():
                async with httpx.AsyncClient(transport=httpx.MockTransport(slow), base_url='https://service.example.test') as c:
                    try:
                        await fetch_json(c, '/slow', deadline=.01)
                    except TimeoutError:
                        return {'deadline_expired': True, 'upstream_finally': bool(cleaned)}
            return asyncio.run(deadline())
        if number == 29:
            job = submit()
            try:
                asyncio.run(run_once(store, clock=lambda: 100, crash_before_publish=True))
            except InjectedCrash:
                pass
            before = store.job('alpha', job['id'])['state']
            after = asyncio.run(run_once(store, clock=lambda: 131))
            return {'after_crash': before, 'after_recovery': after['state'], 'attempts': after['attempt']}
        if number == 30:
            async def mocked():
                answer = await ExtractiveProvider().answer('warranty', [document])
                def transport(request):
                    return httpx.Response(200, json={'status': 'completed', 'output': [{'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': json.dumps(answer)}]}]})
                async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as c:
                    result = await OpenAIProvider(c, 'synthetic', 'explicit-test-model', live=True).answer('warranty', [document])
                return {'transport': 'mock; no network', 'status': result['status']}
            return asyncio.run(mocked())
        if number == 31:
            bucket = TokenBucket(2, 2)
            return {'admission': [bucket.take(t) for t in [0, 0, 0, .5]], 'p95_nearest_rank': nearest_rank([10, 20, 30, 100], .95)}


def main(number=None):
    if number is None:
        parser = argparse.ArgumentParser();parser.add_argument('number', type=int, nargs='?');parser.add_argument('--list', action='store_true');args = parser.parse_args()
        if args.list:
            for i, title in enumerate(TITLES, 1):print(f'{i:02d} {title}')
            return
        if args.number is None:
            parser.error('choose a lab number or --list')
        number = args.number
    if type(number) is not int or not 1 <= number <= 32:
        raise ValueError('lab must be 1..32')
    print(json.dumps({'lab': number, 'title': TITLES[number - 1], 'result': run_lab(number)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
