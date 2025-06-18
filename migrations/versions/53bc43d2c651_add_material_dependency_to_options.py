"""add_material_dependency_to_options

Revision ID: 53bc43d2c651
Revises: 3a7689ab8245
Create Date: 2025-06-16 17:20:42.514331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53bc43d2c651'
down_revision: Union[str, None] = '3a7689ab8245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
