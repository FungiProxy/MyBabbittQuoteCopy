"""Add connection options table

Revision ID: 002
Revises: 001
Create Date: 2024-03-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create connection_options table
    op.create_table(
        'connection_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('rating', sa.String(), nullable=True),
        sa.Column('size', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('product_families', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes for faster lookups
    op.create_index(op.f('ix_connection_options_type'), 'connection_options', ['type'], unique=False)
    op.create_index(op.f('ix_connection_options_rating'), 'connection_options', ['rating'], unique=False)
    op.create_index(op.f('ix_connection_options_size'), 'connection_options', ['size'], unique=False)

    # Insert initial connection options data
    op.execute("""
        INSERT INTO connection_options (type, rating, size, price, product_families) VALUES
        -- Flange 150#
        ('Flange', '150#', '1"', 75.0, 'LS2000,LS6000'),
        ('Flange', '150#', '1.5"', 85.0, 'LS2000,LS6000'),
        ('Flange', '150#', '2"', 95.0, 'LS2000,LS6000'),
        ('Flange', '150#', '3"', 125.0, 'LS2000,LS6000'),
        ('Flange', '150#', '4"', 155.0, 'LS2000,LS6000'),
        
        -- Flange 300#
        ('Flange', '300#', '1"', 95.0, 'LS2000,LS6000'),
        ('Flange', '300#', '1.5"', 110.0, 'LS2000,LS6000'),
        ('Flange', '300#', '2"', 125.0, 'LS2000,LS6000'),
        ('Flange', '300#', '3"', 165.0, 'LS2000,LS6000'),
        ('Flange', '300#', '4"', 205.0, 'LS2000,LS6000'),
        
        -- Tri-Clamp
        ('Tri-Clamp', NULL, '1"', 45.0, 'LS2000,LS6000'),
        ('Tri-Clamp', NULL, '1.5"', 50.0, 'LS2000,LS6000'),
        ('Tri-Clamp', NULL, '2"', 55.0, 'LS2000,LS6000'),
        ('Tri-Clamp', NULL, '3"', 75.0, 'LS2000,LS6000'),
        ('Tri-Clamp', NULL, '4"', 95.0, 'LS2000,LS6000')
    """)


def downgrade():
    op.drop_table('connection_options') 