from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Credential(Base):
    __tablename__ = 'credentials'
    digest: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(16))
    __table_args__ = (CheckConstraint("role IN ('reader','editor')", name='credential_role'),)


class Document(Base):
    __tablename__ = 'documents'
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(120))
    text: Mapped[str] = mapped_column(Text)
    digest: Mapped[str] = mapped_column(String(64))
    version: Mapped[int] = mapped_column(Integer, default=1)
    deleted: Mapped[int] = mapped_column(Integer, default=0)
    __table_args__ = (UniqueConstraint('tenant', 'digest', name='document_content'), Index('document_tenant_id', 'tenant', 'id'))


class Job(Base):
    __tablename__ = 'jobs'
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tenant: Mapped[str] = mapped_column(String(64))
    key: Mapped[str] = mapped_column(String(64))
    fingerprint: Mapped[str] = mapped_column(String(64))
    request_json: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(String(16), default='queued')
    attempt: Mapped[int] = mapped_column(Integer, default=0)
    lease_until: Mapped[int] = mapped_column(Integer, default=0)
    lease_token: Mapped[str] = mapped_column(String(32), default='')
    cancel_requested: Mapped[int] = mapped_column(Integer, default=0)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    __table_args__ = (
        UniqueConstraint('tenant', 'key', name='job_idempotency'),
        CheckConstraint("state IN ('queued','running','succeeded','failed','cancelled')", name='job_state'),
        Index('job_claim', 'state', 'lease_until'),
    )


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[str] = mapped_column(ForeignKey('jobs.id'))
    kind: Mapped[str] = mapped_column(String(32))
    data_json: Mapped[str] = mapped_column(Text)
    __table_args__ = (Index('event_job_id', 'job_id', 'id'),)
