"""initial migration

Revision ID: 001
Revises: 
Create Date: 2026-02-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create roadmaps table
    op.create_table(
        'roadmaps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('goal', sa.Text(), nullable=False),
        sa.Column('duration_weeks', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roadmaps_id'), 'roadmaps', ['id'], unique=False)

    # Create weekplans table
    op.create_table(
        'weekplans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('roadmap_id', sa.Integer(), nullable=False),
        sa.Column('week_number', sa.Integer(), nullable=False),
        sa.Column('focus_title', sa.String(), nullable=False),
        sa.Column('topics_json', sa.JSON(), nullable=False),
        sa.Column('tasks_json', sa.JSON(), nullable=False),
        sa.Column('target_problems', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['roadmap_id'], ['roadmaps.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weekplans_id'), 'weekplans', ['id'], unique=False)

    # Create progress table
    op.create_table(
        'progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('weekplan_id', sa.Integer(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['weekplan_id'], ['weekplans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_progress_id'), 'progress', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_progress_id'), table_name='progress')
    op.drop_table('progress')
    op.drop_index(op.f('ix_weekplans_id'), table_name='weekplans')
    op.drop_table('weekplans')
    op.drop_index(op.f('ix_roadmaps_id'), table_name='roadmaps')
    op.drop_table('roadmaps')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
