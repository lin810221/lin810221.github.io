"""Real ASGI/SQLite/SQLAlchemy/HTTPX tests; no external model calls."""
import asyncio
import json
import secrets
import shutil
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4
import httpx
import jwt
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from fastapi.testclient import TestClient
from fastapi.sse import ServerSentEvent
from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from gateway.api import create_app, principal
from gateway.contracts import DocumentIn, JobIn
from gateway.mechanics import async_database_example, create_mechanics_app
from gateway.models import Base, Credential, Event, Job
from gateway.providers import ExtractiveProvider, OpenAIProvider, validate_answer
from gateway.resilience import TokenBucket, fetch_json, nearest_rank
from gateway.security import decode_access_token
from gateway.settings import Settings
from gateway.store import DomainError, Store, canonical
from gateway.worker import InjectedCrash, run_once


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.runtime = Path(__file__).resolve().parent / '.runtime'
        self.directory = self.runtime / uuid4().hex
        self.directory.mkdir(parents=True)
        self.path = self.directory / 'relay.sqlite3'
        self.app = create_app(Settings(database_path=self.path, stream_seconds=.1))
        self.client_context = TestClient(self.app)
        self.client = self.client_context.__enter__()
        self.store = self.app.state.store
        self.token = self.store.provision('alpha')
        self.reader = self.store.provision('alpha', 'reader')
        self.other = self.store.provision('beta')
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def tearDown(self):
        self.client_context.__exit__(None, None, None)
        assert self.directory.resolve().is_relative_to(self.runtime.resolve())
        shutil.rmtree(self.directory)

    def document(self, text='Warranty lasts 12 months.\nDelivery takes 7 days.', **kwargs):
        result = self.client.post('/api/v1/documents', headers=kwargs.get('headers', self.headers), json={'title': 'Policy', 'text': text})
        self.assertEqual(result.status_code, 201, result.text)
        return result.json()

    def job(self, doc=None, key='request_001', question='warranty'):
        doc = doc or self.document()
        response = self.client.post('/api/v1/jobs', headers=self.headers | {'Idempotency-Key': key}, json={'question': question, 'document_ids': [doc['id']]})
        self.assertEqual(response.status_code, 202, response.text)
        return response.json()

    def test_health_lifespan_cleanup_and_shared_client(self):
        self.assertEqual(self.client.get('/health/live').json(), {'status': 'alive'})
        self.assertEqual(self.client.get('/health/ready').status_code, 200)
        self.assertTrue(self.app.state.ready)
        self.assertFalse(self.app.state.http.is_closed)

    def test_unauthorized_challenge(self):
        r = self.client.get('/api/v1/documents')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.headers['WWW-Authenticate'], 'Bearer')

    def test_reader_cannot_create(self):
        r = self.client.post('/api/v1/documents', headers={'Authorization': 'Bearer ' + self.reader}, json={'title': 'A', 'text': 'B'})
        self.assertEqual(r.status_code, 403)

    def test_revocation_and_hashed_storage(self):
        with Session(self.store.engine) as session:
            serialized = str([(x.digest, x.tenant) for x in session.scalars(select(Credential))])
        self.assertNotIn(self.token, serialized)
        self.store.revoke(self.token)
        self.assertEqual(self.client.get('/api/v1/documents', headers=self.headers).status_code, 401)

    def test_strict_schema_and_redacted_error(self):
        secret = 'rejected-secret-content'
        for payload in [{'title': 3, 'text': secret}, {'title': '', 'text': secret}, {'title': 'A', 'text': secret, 'tenant': 'beta'}]:
            r = self.client.post('/api/v1/documents', headers=self.headers, json=payload)
            self.assertEqual(r.status_code, 422)
            self.assertNotIn(secret, r.text)

    def test_document_dedup_scoped_and_first_title_retained(self):
        a = self.document()
        self.assertEqual(self.document()['id'], a['id'])
        b = self.document(headers={'Authorization': 'Bearer ' + self.other})
        self.assertNotEqual(a['id'], b['id'])
        self.assertEqual(len(self.client.get('/api/v1/documents', headers=self.headers).json()), 1)

    def test_keyset_pagination(self):
        a, b = self.document('first'), self.document('second')
        rows = self.client.get('/api/v1/documents', headers=self.headers, params={'after': a['id'], 'limit': 1}).json()
        self.assertEqual([x['id'] for x in rows], [b['id']])
        self.assertEqual(self.client.get('/api/v1/documents', headers=self.headers, params={'limit': 51}).status_code, 422)

    def test_crud_etag_prevents_lost_title_update(self):
        doc = self.document()
        path = '/api/v1/documents/' + str(doc['id'])
        read = self.client.get(path, headers=self.headers)
        self.assertEqual(read.headers['ETag'], '"1"')
        changed = self.client.patch(path, headers=self.headers | {'If-Match': '"1"'}, json={'title': 'Updated'})
        self.assertEqual(changed.status_code, 200)
        self.assertEqual(changed.headers['ETag'], '"2"')
        stale = self.client.patch(path, headers=self.headers | {'If-Match': '"1"'}, json={'title': 'Stale'})
        self.assertEqual(stale.status_code, 412)
        self.assertEqual(self.client.patch(path, headers=self.headers, json={'title': 'Missing precondition'}).status_code, 428)
        self.assertEqual(self.client.get(path, headers=self.headers).json()['text'], doc['text'])

    def test_logical_delete_hides_source_and_preserves_tombstone(self):
        doc = self.document()
        path = '/api/v1/documents/' + str(doc['id'])
        response = self.client.delete(path, headers=self.headers | {'If-Match': '"1"'})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'')
        self.assertEqual(self.client.get(path, headers=self.headers).status_code, 404)
        self.assertEqual(self.client.get('/api/v1/documents', headers=self.headers).json(), [])
        self.assertEqual(self.client.post('/api/v1/documents', headers=self.headers, json={'title': 'Again', 'text': doc['text']}).status_code, 409)
        with self.assertRaises(DomainError):self.store.selected('alpha', [doc['id']])

    def test_valid_upload_without_filename_path_use(self):
        r = self.client.post('/api/v1/uploads', headers=self.headers, files={'file': ('../../private.txt', b'Warranty is one year.', 'text/plain')})
        self.assertEqual(r.status_code, 201, r.text)
        self.assertEqual(r.json()['title'], 'Uploaded text')
        self.assertFalse((self.directory / 'private.txt').exists())

    def test_upload_wrong_type_encoding_and_length(self):
        for filename, data, mime, expected in [('image.png', b'PNG', 'image/png', 415), ('a.txt', b'\xff\xfe', 'text/plain', 422), ('a.txt', b'x' * 8193, 'text/plain', 413)]:
            r = self.client.post('/api/v1/uploads', headers=self.headers, files={'file': (filename, data, mime)})
            self.assertEqual(r.status_code, expected, r.text)

    def test_latest_form_file_and_field_limits(self):
        r = self.client.post('/api/v1/uploads', headers=self.headers, files=[('file', ('a.txt', b'A', 'text/plain')), ('other', ('b.txt', b'B', 'text/plain'))])
        self.assertEqual(r.status_code, 400)
        r = self.client.post('/api/v1/uploads', headers=self.headers, files={'file': ('a.txt', b'A', 'text/plain')}, data={'unexpected': 'field'})
        self.assertEqual(r.status_code, 400)

    def test_latest_body_limit(self):
        r = self.client.post('/api/v1/documents', headers=self.headers, content=b' ' * 17000)
        self.assertEqual(r.status_code, 413)

    def test_tenant_cannot_submit_another_document(self):
        doc = self.document(headers={'Authorization': 'Bearer ' + self.other})
        r = self.client.post('/api/v1/jobs', headers=self.headers | {'Idempotency-Key': 'request_001'}, json={'question': 'warranty', 'document_ids': [doc['id']]})
        self.assertEqual(r.status_code, 404)

    def test_job_body_duplicate_bool_and_missing_key(self):
        doc = self.document()
        for ids in [[True], [doc['id'], doc['id']], []]:
            r = self.client.post('/api/v1/jobs', headers=self.headers | {'Idempotency-Key': 'request_001'}, json={'question': 'test', 'document_ids': ids})
            self.assertEqual(r.status_code, 422)
        self.assertEqual(self.client.post('/api/v1/jobs', headers=self.headers, json={'question': 'x', 'document_ids': [doc['id']]}).status_code, 422)

    def test_idempotency_same_and_conflict(self):
        doc = self.document()
        a, b = self.job(doc), self.job(doc)
        self.assertEqual(a['id'], b['id'])
        r = self.client.post('/api/v1/jobs', headers=self.headers | {'Idempotency-Key': 'request_001'}, json={'question': 'delivery', 'document_ids': [doc['id']]})
        self.assertEqual(r.status_code, 409)

    def test_parallel_idempotency_database_constraint(self):
        doc = self.document()
        value = JobIn(question='warranty', document_ids=[doc['id']])
        with ThreadPoolExecutor(max_workers=4) as pool:
            ids = list(pool.map(lambda _: self.store.submit('alpha', 'parallel_001', value)['id'], range(8)))
        self.assertEqual(len(set(ids)), 1)
        self.assertEqual(len(self.store.events('alpha', ids[0])), 1)

    def test_worker_answer_and_unicode_offsets(self):
        doc = self.document('前言\nWarranty lasts 12 months.\n')
        job = self.job(doc)
        result = asyncio.run(run_once(self.store))
        self.assertEqual(result['state'], 'succeeded')
        citation = result['result']['citations'][0]
        self.assertEqual(citation['start'], 3)
        self.assertEqual(doc['text'][citation['start']:citation['end']], citation['quote'])
        self.assertEqual(self.store.job('alpha', job['id'])['attempt'], 1)

    def test_worker_abstains_and_empty_queue(self):
        self.job(question='unicorns')
        result = asyncio.run(run_once(self.store))
        self.assertEqual(result['result']['status'], 'abstained')
        self.assertIsNone(asyncio.run(run_once(self.store)))

    def test_cross_tenant_job_and_events_hidden(self):
        job = self.job()
        for suffix in ['', '/events', '/cancel']:
            method = self.client.post if suffix == '/cancel' else self.client.get
            r = method('/api/v1/jobs/' + job['id'] + suffix, headers={'Authorization': 'Bearer ' + self.other})
            self.assertEqual(r.status_code, 404)

    def test_cancel_queued_and_running(self):
        queued = self.job()
        r = self.client.post('/api/v1/jobs/' + queued['id'] + '/cancel', headers=self.headers)
        self.assertEqual(r.json()['state'], 'cancelled')
        running = self.job(key='request_002')
        claim = self.store.claim(100)
        self.store.cancel('alpha', running['id'])
        answer = {'status': 'abstained', 'text': 'No evidence.', 'citations': []}
        result = self.store.finish(claim, answer, 101)
        self.assertEqual(result['state'], 'cancelled')
        self.assertIsNone(result['result'])

    def test_expired_lease_fences_stale_worker(self):
        self.job()
        first = self.store.claim(100)
        self.assertIsNone(self.store.claim(129))
        second = self.store.claim(130)
        self.assertEqual(second['attempt'], 2)
        answer = {'status': 'abstained', 'text': 'No evidence.', 'citations': []}
        with self.assertRaises(DomainError):
            self.store.finish(first, answer, 131)
        self.assertEqual(self.store.finish(second, answer, 131)['state'], 'succeeded')

    def test_crash_restart_recovers_persistent_job(self):
        job = self.job()
        with self.assertRaises(InjectedCrash):
            asyncio.run(run_once(self.store, clock=lambda: 100, crash_before_publish=True))
        restarted = Store(self.path)
        try:
            restarted.migrate()
            self.assertEqual(asyncio.run(run_once(restarted, clock=lambda: 131))['state'], 'succeeded')
            self.assertEqual(restarted.job('alpha', job['id'])['attempt'], 2)
        finally:
            restarted.engine.dispose()

    def test_invalid_provider_output_is_failed_without_secret(self):
        class Bad:
            async def answer(self, *_):
                raise ValueError('private-provider-secret')
        job = self.job()
        with self.assertRaises(ValueError):
            asyncio.run(run_once(self.store, Bad()))
        self.assertEqual(self.store.job('alpha', job['id'])['state'], 'failed')
        self.assertNotIn('private-provider-secret', str(self.store.events('alpha', job['id'])))

    def test_sse_persistence_resume_and_no_double_event(self):
        job = self.job()
        asyncio.run(run_once(self.store))
        rows = self.store.events('alpha', job['id'])
        r = self.client.get('/api/v1/jobs/' + job['id'] + '/events', headers=self.headers | {'Last-Event-ID': str(rows[0]['id'])})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.headers['content-type'].startswith('text/event-stream'))
        self.assertNotIn('event: queued', r.text)
        self.assertIn('event: succeeded', r.text)
        self.assertEqual(r.text.count('event: running'), 1)
        r = self.client.get('/api/v1/jobs/' + job['id'] + '/events', headers=self.headers | {'Last-Event-ID': str(rows[-1]['id'])})
        self.assertNotIn('event:', r.text)
        with Session(self.store.engine) as session, session.begin():
            session.add_all(Event(job_id=job['id'], kind='fixture', data_json='{}') for _ in range(105))
        replay = self.client.get('/api/v1/jobs/' + job['id'] + '/events', headers=self.headers | {'Last-Event-ID': str(rows[-1]['id'])})
        self.assertEqual(replay.text.count('event: fixture'), 105)

    def test_sse_openapi_ndjson_actual_native_serialization(self):
        self.document()
        r = self.client.get('/api/v1/documents.ndjson', headers=self.headers)
        self.assertEqual(r.headers['content-type'].split(';')[0], 'application/jsonl')
        self.assertEqual(json.loads(r.text.splitlines()[0])['title'], 'Policy')
        schema = self.client.get('/openapi.json').json()
        self.assertIn('HTTPBearer', schema['components']['securitySchemes'])
        self.assertIn('text/event-stream', schema['paths']['/api/v1/jobs/{job_id}/events']['get']['responses']['200']['content'])

    def test_request_id_safe_and_no_query_log(self):
        r = self.client.get('/health/live', headers={'X-Request-ID': 'client_001'})
        self.assertEqual(r.headers['X-Request-ID'], 'client_001')
        r = self.client.get('/health/live', headers={'X-Request-ID': 'unsafe value'})
        self.assertEqual(len(r.headers['X-Request-ID']), 32)
        with self.assertLogs('relaydesk', level='INFO') as logs:
            self.client.get('/health/live?secret=private-test-value', headers=self.headers)
        self.assertNotIn('private-test-value', '\n'.join(logs.output))
        self.assertNotIn(self.token, '\n'.join(logs.output))

    def test_poison_job_has_a_finite_attempt_limit(self):
        job = self.job()
        for clock in [100, 130, 160]:
            self.assertIsNotNone(self.store.claim(clock))
        self.assertIsNone(self.store.claim(190))
        self.assertEqual(self.store.job('alpha', job['id'])['state'], 'failed')
        self.assertEqual(self.store.events('alpha', job['id'])[-1]['data']['code'], 'attempt_limit')

    def test_cors_allowlist_and_host(self):
        good = self.client.options('/api/v1/jobs', headers={'Origin': 'http://localhost:3000', 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'authorization,idempotency-key'})
        self.assertEqual(good.headers['access-control-allow-origin'], 'http://localhost:3000')
        bad = self.client.options('/api/v1/jobs', headers={'Origin': 'https://untrusted.example.test', 'Access-Control-Request-Method': 'POST'})
        self.assertNotIn('access-control-allow-origin', bad.headers)
        self.assertEqual(self.client.get('/health/live', headers={'host': 'untrusted.example.test'}).status_code, 400)

    def test_websocket_authenticated_first_frame_and_bounded_echo(self):
        with self.client.websocket_connect('/ws/echo', headers={'Origin': 'http://localhost:3000'}) as ws:
            ws.send_text(self.token)
            self.assertTrue(ws.receive_json()['authenticated'])
            ws.send_text('hello')
            self.assertEqual(ws.receive_json(), {'echo': 'hello'})

    def test_websocket_rejects_missing_origin_and_wrong_token(self):
        from starlette.websockets import WebSocketDisconnect
        with self.assertRaises(WebSocketDisconnect):
            with self.client.websocket_connect('/ws/echo'):
                pass
        with self.client.websocket_connect('/ws/echo', headers={'Origin': 'http://localhost:3000'}) as ws:
            ws.send_text('invalid')
            with self.assertRaises(WebSocketDisconnect):
                ws.receive_json()

    def test_background_task_is_process_local(self):
        r = self.client.post('/api/v1/audit-ping', headers=self.headers)
        self.assertEqual(r.json(), {'scheduled': True, 'durable': False})
        self.assertEqual(self.app.state.audit_count, 1)

    def test_dependency_override_and_restore(self):
        self.app.dependency_overrides[principal] = lambda: {'tenant': 'alpha', 'role': 'reader'}
        try:
            self.assertEqual(self.client.get('/api/v1/documents').status_code, 200)
        finally:
            self.app.dependency_overrides.clear()
        self.assertEqual(self.client.get('/api/v1/documents').status_code, 401)

    def test_migration_matches_models_and_idempotent_upgrade(self):
        self.store.migrate()
        with self.store.engine.connect() as connection:
            differences = compare_metadata(MigrationContext.configure(connection), Base.metadata)
            self.assertEqual(differences, [])
            self.assertEqual(connection.scalar(text('SELECT version_num FROM alembic_version')), '0001')


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_provider_response_byte_budget(self):
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, content=b' ' * 65_537))) as client:
            with self.assertRaisesRegex(ValueError, 'byte budget'):
                await OpenAIProvider(client, 'synthetic', 'explicit', live=True).answer('q', [])

    async def test_chunked_body_limit_without_content_length(self):
        from uuid import uuid4
        root = Path(__file__).resolve().parent / '.runtime'
        scratch = root / uuid4().hex
        scratch.mkdir(parents=True)
        app = create_app(Settings(database_path=scratch / 'relay.sqlite3'))
        async def content():
            yield b' ' * 9000
            yield b' ' * 9000
        try:
            async with app.router.lifespan_context(app):
                token = app.state.store.provision('chunked')
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url='http://testserver') as client:
                    response = await client.post('/api/v1/documents', headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, content=content())
                    self.assertEqual(response.status_code, 413)
        finally:
            assert scratch.resolve().is_relative_to(root.resolve())
            shutil.rmtree(scratch)

    async def test_native_concurrency_limit_actually_caps_inflight(self):
        app = create_mechanics_app()
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url='http://testserver') as client:
            replies = await asyncio.gather(*(client.get('/limited') for _ in range(8)))
        self.assertEqual([r.status_code for r in replies], [200] * 8)
        self.assertEqual(app.state.peak, 2)
        self.assertEqual(app.state.active, 0)

    async def test_async_session_real_sqlite(self):
        self.assertEqual(await async_database_example(), 42)

    async def test_retry_transient_and_finite_attempts(self):
        calls = []
        def transport(request):
            calls.append(request)
            return httpx.Response(503 if len(calls) == 1 else 200, json={'answer': 42})
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport), base_url='https://service.example.test') as client:
            result = await fetch_json(client, '/status', sleep=lambda _: asyncio.sleep(0))
        self.assertEqual(result, {'answer': 42})
        self.assertEqual(len(calls), 2)

    async def test_no_retry_on_auth_error_or_untrusted_url(self):
        calls = []
        def transport(request):
            calls.append(request)
            return httpx.Response(401)
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport), base_url='https://service.example.test') as client:
            with self.assertRaises(httpx.HTTPStatusError):
                await fetch_json(client, '/private')
            with self.assertRaises(ValueError):
                await fetch_json(client, '//169.254.169.254/metadata')
        self.assertEqual(len(calls), 1)

    async def test_total_deadline_cancels_upstream(self):
        closed = []
        async def transport(request):
            try:
                await asyncio.sleep(1)
            finally:
                closed.append(True)
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport), base_url='https://service.example.test') as client:
            with self.assertRaises(TimeoutError):
                await fetch_json(client, '/slow', deadline=.01)
        self.assertEqual(closed, [True])

    async def test_openai_adapter_contract_with_mock_transport(self):
        documents = [{'id': 1, 'text': 'Warranty: 12 months.'}]
        answer = {'status': 'answered', 'text': 'Warranty: 12 months.', 'citations': [{'document_id': 1, 'start': 0, 'end': 20, 'quote': 'Warranty: 12 months.'}]}
        answer['citations'][0]['end'] = len(answer['text'])
        def transport(request):
            payload = json.loads(request.content)
            self.assertEqual(str(request.url), 'https://api.openai.com/v1/responses')
            self.assertFalse(payload['store'])
            self.assertNotIn('tools', payload)
            self.assertEqual(payload['text']['format']['type'], 'json_schema')
            return httpx.Response(200, json={'status': 'completed', 'output': [{'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': json.dumps(answer)}]}]})
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as client:
            value = await OpenAIProvider(client, 'synthetic-key', 'explicit-model', live=True).answer('warranty', documents)
        self.assertEqual(value['citations'][0]['quote'], documents[0]['text'])

    async def test_openai_adapter_rejects_incomplete_refusal_and_wrong_quote(self):
        cases = [{'status': 'incomplete'}, {'status': 'completed', 'output': [{'type': 'message', 'role': 'assistant', 'content': [{'type': 'refusal', 'refusal': 'no'}]}]}, {'status': 'completed', 'output': [{'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': '{"status":"answered","text":"x","citations":[{"document_id":99,"start":0,"end":1,"quote":"x"}]}'}]}]}]
        for data in cases:
            async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=data))) as client:
                with self.assertRaises(ValueError):
                    await OpenAIProvider(client, 'synthetic', 'explicit', live=True).answer('q', [])

    async def test_unicode_extract_and_abstention_contract(self):
        docs = [{'id': 7, 'text': '前言\nWarranty: 12 months.\n'}]
        value = await ExtractiveProvider().answer('warranty', docs)
        self.assertEqual(validate_answer(value, docs, extractive=True)['citations'][0]['start'], 3)
        value['text'] = 'Unsupported paraphrase'
        with self.assertRaises(ValueError):
            validate_answer(value, docs, extractive=True)


class MechanicsTests(unittest.TestCase):
    def test_all_32_documented_lab_behaviors(self):
        from run_lab import run_lab
        for number in range(1, 33):
            with self.subTest(lab=number):
                result = run_lab(number)
                self.assertIsInstance(result, dict)
                self.assertTrue(result)

    def test_yield_function_and_request_cleanup_order(self):
        app = create_mechanics_app()
        with TestClient(app) as client:
            client.get('/function')
            self.assertEqual(app.state.trace, ['open', 'route', 'close', 'chunk'])
            app.state.trace.clear()
            client.get('/request')
            self.assertEqual(app.state.trace, ['open', 'route', 'chunk', 'close'])

    def test_token_bucket_refill_and_monotonic_guard(self):
        bucket = TokenBucket(2, 2)
        self.assertTrue(bucket.take(0));self.assertTrue(bucket.take(0));self.assertFalse(bucket.take(0))
        self.assertTrue(bucket.take(.5))
        with self.assertRaises(ValueError):bucket.take(.4)
        with self.assertRaises(ValueError):TokenBucket(float('nan'), 2)

    def test_nearest_rank_small_sample_and_tail(self):
        self.assertEqual(nearest_rank([10, 20, 30, 100], .95), 100)
        with self.assertRaises(ValueError):nearest_rank([], .95)

    def test_sse_control_char_injection_rejected(self):
        for kwargs in [{'id': 'one\ntwo'}, {'event': 'done\nmalicious'}, {'id': 'bad\0'}]:
            with self.assertRaises(ValueError):ServerSentEvent(**kwargs)

    def test_jwt_required_claims_audience_algorithm_and_expiry(self):
        key = secrets.token_bytes(64)
        claims = {'sub': 'user-1', 'iat': int(time.time()), 'exp': int(time.time()) + 60, 'iss': 'https://issuer.example.test', 'aud': 'relaydesk'}
        token = jwt.encode(claims, key, algorithm='HS256')
        self.assertEqual(decode_access_token(token, key)['sub'], 'user-1')
        for change in [{'aud': 'other'}, {'exp': 1}, {'iss': 'wrong'}]:
            with self.assertRaises(jwt.InvalidTokenError):decode_access_token(jwt.encode(claims | change, key, algorithm='HS256'), key)
        with self.assertRaises(jwt.InvalidTokenError):decode_access_token(jwt.encode(claims, key, algorithm='HS384'), key)

    def test_pydantic_strict_models_and_canonical_request(self):
        with self.assertRaises(ValidationError):JobIn(question='q', document_ids=[True])
        self.assertEqual(JobIn(question='q', document_ids=[2, 1]).document_ids, [1, 2])
        self.assertEqual(canonical({'b': 1, 'a': 2}), canonical({'a': 2, 'b': 1}))

    def test_live_adapter_opt_in_and_settings_bounds(self):
        with self.assertRaises(ValueError):OpenAIProvider(None, 'key', 'model')
        with self.assertRaises(ValueError):Settings(max_body_bytes=1)


if __name__ == '__main__':
    unittest.main()
