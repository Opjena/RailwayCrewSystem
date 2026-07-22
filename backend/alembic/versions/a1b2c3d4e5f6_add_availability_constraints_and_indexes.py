"""Add unique constraint and indexes to availabilities

Revision ID: a1b2c3d4e5f6
Revises: e10baefcaf46
Create Date: 2026-07-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'e10baefcaf46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove the old standalone index on available_date (it's now part of __table_args__)
    op.drop_index('ix_availabilities_available_date', table_name='availabilities')

    # Add new unique constraint and indexes
    op.create_unique_constraint(
        'uq_availabilities_crew_date',
        'availabilities',
        ['crew_id', 'available_date'],
    )
    op.create_index(
        'ix_availabilities_crew_id',
        'availabilities',
        ['crew_id'],
    )
    op.create_index(
        'ix_availabilities_status',
        'availabilities',
        ['status'],
    )
    op.create_index(
        'ix_availabilities_available_date',
        'availabilities',
        ['available_date'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the new indexes and constraint
    op.drop_index('ix_availabilities_available_date', table_name='availabilities')
    op.drop_index('ix_availabilities_status', table_name='availabilities')
    op.drop_index('ix_availabilities_crew_id', table_name='availabilities')
    op.drop_constraint('uq_availabilities_crew_date', 'availabilities', type_='unique')

    # Restore the original standalone index
    op.create_index(
        'ix_availabilities_available_date',
        'availabilities',
        ['available_date'],
    )

