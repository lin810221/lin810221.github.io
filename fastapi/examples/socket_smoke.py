"""Real loopback HTTP, Uvicorn lifespan, a separate worker process and SSE."""
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from uuid import uuid4
import httpx
import uvicorn
from gateway.api import create_app
from gateway.settings import Settings


def run():
    root = Path(__file__).resolve().parent
    scratch = root / '.runtime' / uuid4().hex
    scratch.mkdir(parents=True)
    app = create_app(Settings(database_path=scratch / 'relay.sqlite3', allowed_hosts=['127.0.0.1']))
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    sock.listen(128)
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host='127.0.0.1', port=port, log_level='error', access_log=False, loop='asyncio', lifespan='on'))
    thread = threading.Thread(target=server.run, kwargs={'sockets': [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 15
        while not server.started:
            if not thread.is_alive() or time.monotonic() > deadline:
                raise RuntimeError('server did not become ready')
            time.sleep(.01)
        token = app.state.store.provision('socket-demo')
        with httpx.Client(base_url=f'http://127.0.0.1:{port}', timeout=10, trust_env=False, headers={'Authorization': 'Bearer ' + token}) as client:
            assert client.get('/health/ready').status_code == 200
            uploaded = client.post('/api/v1/uploads', files={'file': ('policy.txt', b'Warranty lasts 12 months.', 'text/plain')})
            assert uploaded.status_code == 201, uploaded.text
            response = client.post('/api/v1/jobs', headers={'Idempotency-Key': 'socket_request'}, json={'question': 'warranty', 'document_ids': [uploaded.json()['id']]})
            assert response.status_code == 202, response.text
            job = response.json()
            env = os.environ.copy() | {'RELAY_DATABASE_PATH': str(scratch / 'relay.sqlite3')}
            worker = subprocess.run([sys.executable, 'manage.py', 'work-once'], cwd=root, env=env, capture_output=True, timeout=30)
            assert worker.returncode == 0, worker.stderr.decode(errors='replace')
            assert client.get('/api/v1/jobs/' + job['id']).json()['state'] == 'succeeded'
            with client.stream('GET', '/api/v1/jobs/' + job['id'] + '/events') as stream:
                frames = list(stream.iter_lines())
            assert any(line == 'event: succeeded' for line in frames), frames
            assert client.post('/api/v1/jobs', headers={'Idempotency-Key': 'socket_request'}, json={'question': 'warranty', 'document_ids': [uploaded.json()['id']]}).json()['id'] == job['id']
        return {'http': 'real loopback TCP', 'server': 'Uvicorn', 'worker': 'separate Python process', 'sse': 'queued/running/succeeded', 'replay': 'same job', 'shutdown': 'graceful'}
    finally:
        server.should_exit = True
        thread.join(10)
        sock.close()
        if thread.is_alive():
            raise RuntimeError('server shutdown timed out')
        assert scratch.resolve().is_relative_to((root / '.runtime').resolve())
        shutil.rmtree(scratch)


if __name__ == '__main__':
    print(json.dumps(run()))
