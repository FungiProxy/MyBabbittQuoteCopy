"""replace_product_variants_with_base_models

Revision ID: 806ecdc3a65b
Revises: 2e9b3c6d02e0
Create Date: 2025-06-20 03:06:36.730862

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '806ecdc3a65b'
down_revision: Union[str, None] = '2e9b3c6d02e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the product_variants table
    op.drop_table('product_variants')

    # Create the base_models table
    op.create_table(
        'base_models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_family_id', sa.Integer(), nullable=False),
        sa.Column('model_number', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('base_price', sa.Float(), nullable=False),
        sa.Column('base_length', sa.Float(), nullable=False),
        sa.Column('voltage', sa.String(), nullable=False),
        sa.Column('material', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ['product_family_id'],
            ['product_families.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create indexes
    op.create_index(op.f('ix_base_models_id'), 'base_models', ['id'], unique=False)
    op.create_index(
        op.f('ix_base_models_model_number'),
        'base_models',
        ['model_number'],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the base_models table
    op.drop_index(op.f('ix_base_models_model_number'), table_name='base_models')
    op.drop_index(op.f('ix_base_models_id'), table_name='base_models')
    op.drop_table('base_models')

    # Recreate the product_variants table
    op.create_table(
        'product_variants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_family_id', sa.Integer(), nullable=False),
        sa.Column('model_number', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=False),
        sa.Column('base_length', sa.Float(), nullable=True),
        sa.Column('voltage', sa.String(), nullable=True),
        sa.Column('material', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ['product_family_id'],
            ['product_families.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_product_variants_id'), 'product_variants', ['id'], unique=False
    )
    op.create_index(
        op.f('ix_product_variants_model_number'),
        'product_variants',
        ['model_number'],
        unique=False,
    )
