"""quoteitem_to_base_model_fk

Revision ID: 7238353449f6
Revises: 806ecdc3a65b
Create Date: 2025-06-20 03:08:41.958579

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7238353449f6"
down_revision: Union[str, None] = "806ecdc3a65b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Skipped due to missing product_variants table
    # with op.batch_alter_table("quote_items") as batch_op:
    #     batch_op.drop_constraint("quote_items_product_id_fkey", type_="foreignkey")
    #     batch_op.create_foreign_key(
    #         "quote_items_product_id_fkey",
    #         "base_models",
    #         ["product_id"],
    #         ["id"],
    #     )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert to old foreign key
    # with op.batch_alter_table("quote_items") as batch_op:
    #     batch_op.drop_constraint("quote_items_product_id_fkey", type_="foreignkey")
    #     batch_op.create_foreign_key(
    #         "quote_items_product_id_fkey",
    #         "product_variants",
    #         ["product_id"],
    #         ["id"],
    #     )
