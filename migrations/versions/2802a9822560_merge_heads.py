"""merge heads

Revision ID: 2802a9822560
Revises: a21ee0210300, add_length_adder_rules
Create Date: 2025-06-22 12:36:22.923746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2802a9822560'
down_revision: Union[str, None] = ('a21ee0210300', 'add_length_adder_rules')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
