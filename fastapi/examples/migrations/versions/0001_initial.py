"""Immutable RelayDesk baseline. Never import mutable app metadata here."""
from alembic import op
import sqlalchemy as sa
revision = '0001'
down_revision = None
branch_labels = depends_on = None


def upgrade():
    op.create_table('credentials', sa.Column('digest', sa.String(64), primary_key=True), sa.Column('tenant', sa.String(64), nullable=False), sa.Column('role', sa.String(16), nullable=False), sa.CheckConstraint("role IN ('reader','editor')", name='credential_role'))
    op.create_table('documents', sa.Column('id', sa.Integer, primary_key=True), sa.Column('tenant', sa.String(64), nullable=False), sa.Column('title', sa.String(120), nullable=False), sa.Column('text', sa.Text, nullable=False), sa.Column('digest', sa.String(64), nullable=False), sa.Column('version', sa.Integer, nullable=False), sa.Column('deleted', sa.Integer, nullable=False), sa.UniqueConstraint('tenant', 'digest', name='document_content'))
    op.create_index('document_tenant_id', 'documents', ['tenant', 'id'])
    op.create_table('jobs', sa.Column('id', sa.String(32), primary_key=True), sa.Column('tenant', sa.String(64), nullable=False), sa.Column('key', sa.String(64), nullable=False), sa.Column('fingerprint', sa.String(64), nullable=False), sa.Column('request_json', sa.Text, nullable=False), sa.Column('state', sa.String(16), nullable=False), sa.Column('attempt', sa.Integer, nullable=False), sa.Column('lease_until', sa.Integer, nullable=False), sa.Column('lease_token', sa.String(32), nullable=False), sa.Column('cancel_requested', sa.Integer, nullable=False), sa.Column('result_json', sa.Text, nullable=True), sa.UniqueConstraint('tenant', 'key', name='job_idempotency'), sa.CheckConstraint("state IN ('queued','running','succeeded','failed','cancelled')", name='job_state'))
    op.create_index('job_claim', 'jobs', ['state', 'lease_until'])
    op.create_table('events', sa.Column('id', sa.Integer, primary_key=True), sa.Column('job_id', sa.String(32), sa.ForeignKey('jobs.id'), nullable=False), sa.Column('kind', sa.String(32), nullable=False), sa.Column('data_json', sa.Text, nullable=False))
    op.create_index('event_job_id', 'events', ['job_id', 'id'])


def downgrade():
    for name in ['events', 'jobs', 'documents', 'credentials']:
        op.drop_table(name)
