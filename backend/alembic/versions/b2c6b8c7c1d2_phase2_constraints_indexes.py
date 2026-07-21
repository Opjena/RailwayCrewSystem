"""Phase 2 constraints & indexes (assignments/availabilities)

Revision ID: b2c6b8c7c1d2
Revises: d5d1026432f4
Create Date: 2026-07-20

"""

from alembic import op
import sqlalchemy as sa


revision = 'b2c6b8c7c1d2'
down_revision = 'd5d1026432f4'

# This migration assumes the base schema is present.
# If your environment starts from a fresh DB, run `alembic upgrade 001_initial_schema`
# (or `alembic upgrade head`) after ensuring requirements/psycopg are installed.

branch_labels = None
depends_on = None


def upgrade() -> None:
    # assignments: enforce uniqueness per (shift_id, crew_id)
    op.create_unique_constraint(
        'uq_assignments_shift_crew',
        'assignments',
        ['shift_id', 'crew_id'],
    )

    # assignments indexes
    op.create_index('ix_assignments_shift_id', 'assignments', ['shift_id'], unique=False)
    op.create_index('ix_assignments_crew_id', 'assignments', ['crew_id'], unique=False)
    op.create_index('ix_assignments_status', 'assignments', ['status'], unique=False)

    # availabilities: enforce uniqueness per (crew_id, available_date)
    op.create_unique_constraint(
        'uq_availabilities_crew_date',
        'availabilities',
        ['crew_id', 'available_date'],
    )

    # availabilities indexes
    op.create_index('ix_availabilities_crew_id', 'availabilities', ['crew_id'], unique=False)
    op.create_index('ix_availabilities_status', 'availabilities', ['status'], unique=False)


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('ix_availabilities_status', table_name='availabilities')
    op.drop_index('ix_availabilities_crew_id', table_name='availabilities')

    op.drop_constraint('uq_availabilities_crew_date', 'availabilities', type_='unique')

    op.drop_index('ix_assignments_status', table_name='assignments')
    op.drop_index('ix_assignments_crew_id', table_name='assignments')
    op.drop_index('ix_assignments_shift_id', table_name='assignments')

    op.drop_constraint('uq_assignments_shift_crew', 'assignments', type_='unique')
