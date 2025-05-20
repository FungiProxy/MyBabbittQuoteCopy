"""Add material options table

Revision ID: 004
Revises: 003
Create Date: 2024-03-21

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Create material_options table
    op.create_table(
        'material_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_family', sa.String(), nullable=False),
        sa.Column('material_code', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=False),
        sa.Column('base_price', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_available', sa.Integer(), nullable=False, server_default='1'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes for faster lookups
    op.create_index(op.f('ix_material_options_product_family'), 'material_options', ['product_family'], unique=False)
    op.create_index(op.f('ix_material_options_material_code'), 'material_options', ['material_code'], unique=False)

    # Insert initial material options data based on product documentation
    op.execute("""
        INSERT INTO material_options (product_family, material_code, display_name, base_price) VALUES
        -- LS2000
        ('LS2000', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS2000', 'H', 'H - Hastelloy C', 400.0),
        ('LS2000', 'A', 'A - Aluminum', 50.0),
        ('LS2000', 'T', 'T - Titanium', 600.0),
        ('LS2000', 'U', 'U - UHMW Polyethylene', 80.0),
        
        -- LS2100 (Limited options due to loop powered)
        ('LS2100', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS2100', 'H', 'H - Hastelloy C', 400.0),
        
        -- LS6000 (Heavy duty - all materials)
        ('LS6000', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS6000', 'H', 'H - Hastelloy C', 400.0),
        ('LS6000', 'A', 'A - Aluminum', 50.0),
        ('LS6000', 'T', 'T - Titanium', 600.0),
        ('LS6000', 'U', 'U - UHMW Polyethylene', 80.0),
        
        -- LS7000 (Advanced features)
        ('LS7000', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS7000', 'H', 'H - Hastelloy C', 400.0),
        ('LS7000', 'T', 'T - Titanium', 600.0),
        
        -- LS7000/2 (Dual point - requires conductive materials)
        ('LS7000/2', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS7000/2', 'H', 'H - Hastelloy C', 400.0),
        
        -- LS8000 (Remote mounted)
        ('LS8000', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS8000', 'H', 'H - Hastelloy C', 400.0),
        ('LS8000', 'T', 'T - Titanium', 600.0),
        
        -- LS8000/2 (Remote mounted dual point)
        ('LS8000/2', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LS8000/2', 'H', 'H - Hastelloy C', 400.0),
        
        -- LT9000 (Level transmitter)
        ('LT9000', 'S', 'S - 316 Stainless Steel', 0.0),
        ('LT9000', 'H', 'H - Hastelloy C', 400.0),
        ('LT9000', 'T', 'T - Titanium', 600.0),
        
        -- FS10000 (Flow switch)
        ('FS10000', 'S', 'S - 316 Stainless Steel', 0.0),
        ('FS10000', 'H', 'H - Hastelloy C', 400.0),
        ('FS10000', 'T', 'T - Titanium', 600.0)
    """)


def downgrade():
    op.drop_index(op.f('ix_material_options_material_code'), table_name='material_options')
    op.drop_index(op.f('ix_material_options_product_family'), table_name='material_options')
    op.drop_table('material_options') 