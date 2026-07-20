"""merge heads

Revision ID: d5d1026432f4
Revises: 001_initial_schema, a006570f9309
Create Date: 2026-07-20 11:03:47.456571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5d1026432f4'
down_revision: Union[str, Sequence[str], None] = ('001_initial_schema', 'a006570f9309')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
