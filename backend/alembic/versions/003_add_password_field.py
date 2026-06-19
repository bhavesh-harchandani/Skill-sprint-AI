"""add password field to users

Revision ID: 003
Revises: 002
Create Date: 2026-02-17 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add hashed_password column to users table
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    
    # Set a default password hash for existing users (they'll need to reset)
    op.execute("UPDATE users SET hashed_password = '$2b$12$default' WHERE hashed_password IS NULL")
    
    # Make it non-nullable
    op.alter_column('users', 'hashed_password', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'hashed_password')
