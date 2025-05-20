"""Remove ProductFamily and update ProductVariant to Product

Revision ID: 001
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create new products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_number', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('base_length', sa.Float(), nullable=True),
        sa.Column('voltage', sa.String(), nullable=True),
        sa.Column('material', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_model_number'), 'products', ['model_number'], unique=False)
    op.create_index(op.f('ix_products_category'), 'products', ['category'], unique=False)

    # Copy data from product_variants to products
    op.execute("""
        INSERT INTO products (model_number, description, category, base_price, base_length, voltage, material)
        SELECT pv.model_number, pv.description, pf.category, pv.base_price, pv.base_length, pv.voltage, pv.material
        FROM product_variants pv
        JOIN product_families pf ON pv.product_family_id = pf.id
    """)

    # Update foreign keys in quote_items
    op.execute("""
        UPDATE quote_items
        SET product_id = (
            SELECT p.id 
            FROM products p
            JOIN product_variants pv ON p.model_number = pv.model_number
            WHERE pv.id = quote_items.product_id
        )
    """)

    # Drop old tables
    op.drop_table('product_variants')
    op.drop_table('product_families')


def downgrade():
    # Create old tables
    op.create_table(
        'product_families',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_families_id'), 'product_families', ['id'], unique=False)
    op.create_index(op.f('ix_product_families_name'), 'product_families', ['name'], unique=False)
    op.create_index(op.f('ix_product_families_category'), 'product_families', ['category'], unique=False)

    op.create_table(
        'product_variants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_family_id', sa.Integer(), nullable=False),
        sa.Column('model_number', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('base_price', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('base_length', sa.Float(), nullable=True),
        sa.Column('voltage', sa.String(), nullable=True),
        sa.Column('material', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['product_family_id'], ['product_families.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_variants_id'), 'product_variants', ['id'], unique=False)
    op.create_index(op.f('ix_product_variants_model_number'), 'product_variants', ['model_number'], unique=False)

    # Copy data back
    op.execute("""
        INSERT INTO product_families (name, description, category)
        SELECT DISTINCT 
            SUBSTR(model_number, 1, INSTR(model_number, '/')-1),
            'Migrated from products',
            category
        FROM products
    """)

    op.execute("""
        INSERT INTO product_variants (
            product_family_id, model_number, description, 
            base_price, base_length, voltage, material
        )
        SELECT 
            pf.id,
            p.model_number,
            p.description,
            p.base_price,
            p.base_length,
            p.voltage,
            p.material
        FROM products p
        JOIN product_families pf ON pf.name = SUBSTR(p.model_number, 1, INSTR(p.model_number, '/')-1)
    """)

    # Update foreign keys in quote_items
    op.execute("""
        UPDATE quote_items
        SET product_id = (
            SELECT pv.id
            FROM product_variants pv
            JOIN products p ON p.model_number = pv.model_number
            WHERE p.id = quote_items.product_id
        )
    """)

    # Drop new table
    op.drop_table('products') 