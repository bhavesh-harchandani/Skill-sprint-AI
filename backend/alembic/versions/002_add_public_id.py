"""add public_id to roadmaps

Revision ID: 002
Revises: 001
Create Date: 2026-02-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add public_id column to roadmaps table
    op.add_column('roadmaps', sa.Column('public_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_roadmaps_public_id'), 'roadmaps', ['public_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_roadmaps_public_id'), table_name='roadmaps')
    op.drop_column('roadmaps', 'public_id')
