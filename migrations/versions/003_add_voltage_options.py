"""Add voltage options table

Revision ID: 003
Revises: 002
Create Date: 2024-03-21

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Create voltage_options table
    op.create_table(
        'voltage_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_family', sa.String(), nullable=False),
        sa.Column('voltage', sa.String(), nullable=False),
        sa.Column('is_available', sa.Integer(), nullable=False, server_default='1'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes for faster lookups
    op.create_index(op.f('ix_voltage_options_product_family'), 'voltage_options', ['product_family'], unique=False)
    op.create_index(op.f('ix_voltage_options_voltage'), 'voltage_options', ['voltage'], unique=False)

    # Insert initial voltage options data based on product documentation
    op.execute("""
        INSERT INTO voltage_options (product_family, voltage) VALUES
        -- LS2000
        ('LS2000', '24VDC'),
        ('LS2000', '115VAC'),
        
        -- LS2100 (Loop powered only)
        ('LS2100', '24VDC'),
        
        -- LS6000
        ('LS6000', '12VDC'),
        ('LS6000', '24VDC'),
        ('LS6000', '115VAC'),
        ('LS6000', '240VAC'),
        
        -- LS7000
        ('LS7000', '12VDC'),
        ('LS7000', '24VDC'),
        ('LS7000', '115VAC'),
        ('LS7000', '240VAC'),
        
        -- LS7000/2 (Dual Point)
        ('LS7000/2', '12VDC'),
        ('LS7000/2', '24VDC'),
        ('LS7000/2', '115VAC'),
        ('LS7000/2', '240VAC'),
        
        -- LS8000 (Remote Mounted)
        ('LS8000', '12VDC'),
        ('LS8000', '24VDC'),
        ('LS8000', '115VAC'),
        ('LS8000', '240VAC'),
        
        -- LS8000/2 (Remote Mounted Dual Point)
        ('LS8000/2', '12VDC'),
        ('LS8000/2', '24VDC'),
        ('LS8000/2', '115VAC'),
        ('LS8000/2', '240VAC'),
        
        -- LT9000 (Level Transmitter)
        ('LT9000', '24VDC'),
        ('LT9000', '230VAC'),
        
        -- FS10000 (Flow Switch)
        ('FS10000', '24VDC'),
        ('FS10000', '115VAC')
    """)


def downgrade():
    op.drop_index(op.f('ix_voltage_options_voltage'), table_name='voltage_options')
    op.drop_index(op.f('ix_voltage_options_product_family'), table_name='voltage_options')
    op.drop_table('voltage_options') 