"""add domain to roadmaps

Revision ID: 007
Revises: 006
Create Date: 2026-02-17 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add domain column to roadmaps table
    op.add_column('roadmaps', sa.Column('domain', sa.String(), nullable=True))
    
    # Create index on domain for faster filtering
    op.create_index('ix_roadmaps_domain', 'roadmaps', ['domain'])


def downgrade() -> None:
    op.drop_index('ix_roadmaps_domain', 'roadmaps')
    op.drop_column('roadmaps', 'domain')
