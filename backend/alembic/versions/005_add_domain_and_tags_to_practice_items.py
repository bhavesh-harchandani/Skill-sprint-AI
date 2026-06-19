"""add domain and tags to practice items

Revision ID: 005
Revises: 004
Create Date: 2026-02-17 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add domain column
    op.add_column('practice_items', sa.Column('domain', sa.String(), nullable=True))
    
    # Add tags column (JSON array)
    op.add_column('practice_items', sa.Column('tags', JSONB, nullable=True, server_default='[]'))
    
    # Set default domain for existing items (assume DSA)
    op.execute("UPDATE practice_items SET domain = 'DSA' WHERE domain IS NULL")
    
    # Make domain non-nullable after setting defaults
    op.alter_column('practice_items', 'domain', nullable=False)
    
    # Create index on domain for faster filtering
    op.create_index('ix_practice_items_domain', 'practice_items', ['domain'])


def downgrade() -> None:
    op.drop_index('ix_practice_items_domain', 'practice_items')
    op.drop_column('practice_items', 'tags')
    op.drop_column('practice_items', 'domain')
