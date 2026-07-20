"""Phase 2 constraints & indexes (safe, only if tables exist)

Revision ID: a0a1b2c3d4e5
Revises: d5d1026432f4
Create Date: 2026-07-20

This migration is idempotent with respect to missing base tables.
If the base tables (assignments/availabilities) are not present in the DB,
it will skip adding constraints/indexes.
"""

from alembic import op
import sqlalchemy as sa

revision = 'a0a1b2c3d4e5'
down_revision = 'd5d1026432f4'
branch_labels = None
depends_on = None


def _table_exists(table_name: str) -> bool:
    conn = op.get_bind()
    return conn.execute(
        sa.text(
            "SELECT 1 FROM information_schema.tables "
            "WHERE table_schema='public' AND table_name=:t"
        ),
        {"t": table_name},
    ).first() is not None


def upgrade() -> None:
    if _table_exists('assignments'):
        # unique constraint
        op.create_unique_constraint(
            'uq_assignments_shift_crew',
            'assignments',
            ['shift_id', 'crew_id'],
        )
        # indexes
        op.create_index('ix_assignments_shift_id', 'assignments', ['shift_id'], unique=False)
        op.create_index('ix_assignments_crew_id', 'assignments', ['crew_id'], unique=False)
        op.create_index('ix_assignments_status', 'assignments', ['status'], unique=False)

    if _table_exists('availabilities'):
        op.create_unique_constraint(
            'uq_availabilities_crew_date',
            'availabilities',
            ['crew_id', 'available_date'],
        )
        op.create_index('ix_availabilities_crew_id', 'availabilities', ['crew_id'], unique=False)
        op.create_index(
            'ix_availabilities_available_date',
            'availabilities',
            ['available_date'],
            unique=False,
        )
        op.create_index('ix_availabilities_status', 'availabilities', ['status'], unique=False)


def downgrade() -> None:
    # Best-effort downgrade.
    if _table_exists('availabilities'):
        op.drop_index('ix_availabilities_status', table_name='availabilities')
        op.drop_index('ix_availabilities_available_date', table_name='availabilities')
        op.drop_index('ix_availabilities_crew_id', table_name='availabilities')
        op.drop_constraint('uq_availabilities_crew_date', 'availabilities', type_='unique')

    if _table_exists('assignments'):
        op.drop_index('ix_assignments_status', table_name='assignments')
        op.drop_index('ix_assignments_crew_id', table_name='assignments')
        op.drop_index('ix_assignments_shift_id', table_name='assignments')
        op.drop_constraint('uq_assignments_shift_crew', 'assignments', type_='unique')

