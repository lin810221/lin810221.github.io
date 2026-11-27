"""SQLAlchemy sessions are short-lived; worker publication is lease-fenced."""
import hashlib
import json
import re
import secrets
from pathlib import Path
from uuid import uuid4
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .contracts import Answer, JobIn
from .models import Credential, Document, Event, Job


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


class DomainError(Exception):
    def __init__(self, status, code):
        self.status, self.code = status, code


class Store:
    def __init__(self, path):
        path = Path(path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine('sqlite:///' + path.as_posix(), connect_args={'check_same_thread': False, 'timeout': 5}, pool_pre_ping=True)
        @event.listens_for(self.engine, 'connect')
        def pragmas(connection, _):
            connection.execute('PRAGMA foreign_keys=ON')
            connection.execute('PRAGMA busy_timeout=5000')

    def migrate(self):
        base = Path(__file__).resolve().parents[1]
        config = Config()
        config.set_main_option('script_location', str(base / 'migrations'))
        with self.engine.begin() as connection:
            config.attributes['connection'] = connection
            command.upgrade(config, 'head')

    def provision(self, tenant, role='editor'):
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,31}', tenant) or role not in {'reader', 'editor'}:
            raise ValueError('invalid identity')
        token = secrets.token_urlsafe(32)
        with Session(self.engine) as session, session.begin():
            session.add(Credential(digest=digest(token), tenant=tenant, role=role))
        return token

    def identity(self, token):
        with Session(self.engine) as session:
            row = session.get(Credential, digest(token))
            if row is None:
                raise DomainError(401, 'unauthorized')
            return {'tenant': row.tenant, 'role': row.role}

    def revoke(self, token):
        with Session(self.engine) as session, session.begin():
            row = session.get(Credential, digest(token))
            if row:
                session.delete(row)

    def add_document(self, tenant, title, content):
        value = digest(content)
        try:
            with Session(self.engine) as session, session.begin():
                row = Document(tenant=tenant, title=title, text=content, digest=value, version=1, deleted=0)
                session.add(row)
                session.flush()
                return self._document(row)
        except IntegrityError:
            with Session(self.engine) as session:
                row = session.scalar(select(Document).where(Document.tenant == tenant, Document.digest == value))
                if row is None:
                    raise
                if row.deleted:
                    raise DomainError(409, 'content_tombstoned')
                return self._document(row)

    @staticmethod
    def _document(row):
        return {'id': row.id, 'title': row.title, 'text': row.text, 'version': row.version}

    def document(self, tenant, identifier):
        with Session(self.engine) as session:
            row = session.scalar(select(Document).where(Document.tenant == tenant, Document.id == identifier, Document.deleted == 0))
            if row is None:
                raise DomainError(404, 'document_not_found')
            return self._document(row)

    def change_document(self, tenant, identifier, version, *, title=None, delete=False):
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.scalar(select(Document).where(Document.tenant == tenant, Document.id == identifier, Document.deleted == 0))
            if row is None:
                raise DomainError(404, 'document_not_found')
            if row.version != version:
                raise DomainError(412, 'version_precondition_failed')
            if delete:
                row.deleted = 1
            else:
                row.title = title
            row.version += 1
            return self._document(row)

    def documents(self, tenant, after=0, limit=20):
        with Session(self.engine) as session:
            rows = session.scalars(select(Document).where(Document.tenant == tenant, Document.id > after, Document.deleted == 0).order_by(Document.id).limit(limit))
            return [self._document(row) for row in rows]

    def selected(self, tenant, identifiers):
        with Session(self.engine) as session:
            rows = list(session.scalars(select(Document).where(Document.tenant == tenant, Document.id.in_(identifiers), Document.deleted == 0).order_by(Document.id)))
            if len(rows) != len(identifiers):
                raise DomainError(404, 'document_not_found')
            return [self._document(row) for row in rows]

    def submit(self, tenant, key, request: JobIn):
        if not re.fullmatch(r'[A-Za-z0-9_-]{8,64}', key):
            raise DomainError(422, 'invalid_idempotency_key')
        self.selected(tenant, request.document_ids)
        payload = canonical(request.model_dump())
        fingerprint = digest(payload)
        try:
            with Session(self.engine) as session, session.begin():
                row = Job(id=uuid4().hex, tenant=tenant, key=key, fingerprint=fingerprint, request_json=payload, state='queued', attempt=0, lease_until=0, lease_token='', cancel_requested=0)
                session.add(row)
                session.flush()
                session.add(Event(job_id=row.id, kind='queued', data_json=canonical({'state': 'queued'})))
                result = self._job(row)
            return result
        except IntegrityError:
            with Session(self.engine) as session:
                row = session.scalar(select(Job).where(Job.tenant == tenant, Job.key == key))
                if row is None:
                    raise
                if row.fingerprint != fingerprint:
                    raise DomainError(409, 'idempotency_conflict')
                return self._job(row)

    @staticmethod
    def _job(row):
        return {'id': row.id, 'state': row.state, 'attempt': row.attempt, 'cancel_requested': bool(row.cancel_requested), 'result': json.loads(row.result_json) if row.result_json else None}

    def job(self, tenant, identifier):
        with Session(self.engine) as session:
            row = session.scalar(select(Job).where(Job.id == identifier, Job.tenant == tenant))
            if row is None:
                raise DomainError(404, 'job_not_found')
            return self._job(row)

    def cancel(self, tenant, identifier):
        with Session(self.engine) as session, session.begin():
            # SQLite obtains its writer lock before checking state.
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.scalar(select(Job).where(Job.id == identifier, Job.tenant == tenant))
            if row is None:
                raise DomainError(404, 'job_not_found')
            if row.state in {'queued', 'running'} and not row.cancel_requested:
                row.cancel_requested = 1
                if row.state == 'queued':
                    row.state = 'cancelled'
                session.add(Event(job_id=row.id, kind='cancel_requested', data_json=canonical({'state': row.state})))
            return self._job(row)

    def claim(self, now, lease_seconds=30):
        if type(now) is not int or now < 0 or type(lease_seconds) is not int or lease_seconds <= 0:
            raise ValueError('invalid clock or lease')
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.scalar(select(Job).where((Job.state == 'queued') | ((Job.state == 'running') & (Job.lease_until <= now))).order_by(Job.id).limit(1))
            if row is None:
                return None
            if row.attempt >= 3:
                row.state = 'cancelled' if row.cancel_requested else 'failed'
                row.lease_until = 0
                session.add(Event(job_id=row.id, kind=row.state, data_json=canonical({'code': 'attempt_limit'})))
                return None
            row.state = 'running'
            row.attempt += 1
            row.lease_token = uuid4().hex
            row.lease_until = now + lease_seconds
            session.add(Event(job_id=row.id, kind='running', data_json=canonical({'attempt': row.attempt})))
            return {'id': row.id, 'tenant': row.tenant, 'token': row.lease_token, 'request': json.loads(row.request_json), 'attempt': row.attempt}

    def finish(self, claim, result, now):
        answer = Answer.model_validate(result).model_dump()
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.get(Job, claim['id'])
            if row is None or row.state != 'running' or row.lease_token != claim['token'] or row.lease_until <= now:
                raise DomainError(409, 'stale_lease')
            if row.cancel_requested:
                row.state = 'cancelled'
            else:
                row.state, row.result_json = 'succeeded', canonical(answer)
            row.lease_until = 0
            session.add(Event(job_id=row.id, kind=row.state, data_json=canonical({'state': row.state})))
            return self._job(row)

    def fail(self, claim, now):
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.get(Job, claim['id'])
            if row and row.state == 'running' and row.lease_token == claim['token'] and row.lease_until > now:
                row.state = 'cancelled' if row.cancel_requested else 'failed'
                row.lease_until = 0
                session.add(Event(job_id=row.id, kind=row.state, data_json=canonical({'code': 'work_failed'})))

    def events(self, tenant, identifier, after=0):
        self.job(tenant, identifier)
        with Session(self.engine) as session:
            rows = session.scalars(select(Event).where(Event.job_id == identifier, Event.id > after).order_by(Event.id).limit(100))
            return [{'id': row.id, 'event': row.kind, 'data': json.loads(row.data_json)} for row in rows]
