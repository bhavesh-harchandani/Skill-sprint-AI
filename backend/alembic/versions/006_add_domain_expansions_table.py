"""add domain expansions table

Revision ID: 006
Revises: 005
Create Date: 2026-02-17 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create domain_expansions table
    op.create_table(
        'domain_expansions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('expanded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('items_generated', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_expanding', sa.Boolean(), server_default='false', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('domain')
    )
    
    # Create indexes
    op.create_index('ix_domain_expansions_domain', 'domain_expansions', ['domain'])


def downgrade() -> None:
    op.drop_index('ix_domain_expansions_domain', 'domain_expansions')
    op.drop_table('domain_expansions')
