"""replace_variants_with_base_models_and_update_quoteitem_fk

Revision ID: a21ee0210300
Revises: 7238353449f6
Create Date: 2025-06-20 03:09:46.964773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a21ee0210300'
down_revision: Union[str, None] = '7238353449f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Drop FK from quote_items.product_id to product_variants.id
    with op.batch_alter_table('quote_items') as batch_op:
        batch_op.drop_constraint('quote_items_product_id_fkey', type_='foreignkey')
    # 2. Drop product_variants table
    op.drop_table('product_variants')
    # 3. Create base_models table
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
    op.create_index(
        op.f('ix_base_models_id'), 'base_models', ['id'], unique=False
    )
    op.create_index(
        op.f('ix_base_models_model_number'), 'base_models', ['model_number'], unique=True
    )
    # 4. Add FK from quote_items.product_id to base_models.id
    with op.batch_alter_table('quote_items') as batch_op:
        batch_op.create_foreign_key(
            'quote_items_product_id_fkey',
            'base_models',
            ['product_id'],
            ['id'],
        )


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Drop FK from quote_items.product_id to base_models.id
    with op.batch_alter_table('quote_items') as batch_op:
        batch_op.drop_constraint('quote_items_product_id_fkey', type_='foreignkey')
    # 2. Drop base_models table
    op.drop_index(op.f('ix_base_models_model_number'), table_name='base_models')
    op.drop_index(op.f('ix_base_models_id'), table_name='base_models')
    op.drop_table('base_models')
    # 3. Recreate product_variants table
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
        op.f('ix_product_variants_model_number'), 'product_variants', ['model_number'], unique=False
    )
    # 4. Add FK from quote_items.product_id to product_variants.id
    with op.batch_alter_table('quote_items') as batch_op:
        batch_op.create_foreign_key(
            'quote_items_product_id_fkey',
            'product_variants',
            ['product_id'],
            ['id'],
        )
