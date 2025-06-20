"""Add length_adder_rules table

Revision ID: add_length_adder_rules
Revises: 806ecdc3a65b
Create Date: 2024-01-15 10:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'add_length_adder_rules'
down_revision = '806ecdc3a65b'
branch_labels = None
depends_on = None


def upgrade():
    # Create length_adder_rules table
    op.create_table(
        'length_adder_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_family', sa.String(), nullable=False),
        sa.Column('material_code', sa.String(), nullable=False),
        sa.Column('adder_type', sa.String(), nullable=False),
        sa.Column('first_threshold', sa.Float(), nullable=False),
        sa.Column('adder_amount', sa.Float(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Insert length adder rules data
    op.execute(
        """
        INSERT INTO length_adder_rules (id, product_family, material_code, adder_type, first_threshold, adder_amount, description) VALUES
        -- Per-foot adders for most product families (first adder at 24")
        (1,'LS2000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (2,'LS2000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (3,'LS2000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (4,'LS2000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (5,'LS2100','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (6,'LS2100','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (7,'LS2100','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (8,'LS2100','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (9,'LS6000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (10,'LS6000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (11,'LS6000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (12,'LS6000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (13,'LS7000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (14,'LS7000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (15,'LS7000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (16,'LS7000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (17,'LS7000/2','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (18,'LS7000/2','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (19,'LS8000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (20,'LS8000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (21,'LS8000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (22,'LS8000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (23,'LS8000/2','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (24,'LS8000/2','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (25,'LT9000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (26,'LT9000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
        (27,'LS7500','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        (28,'LS8500','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
        -- FS10000 special case (first adder at 18")
        (29,'FS10000','S','per_foot',18.0,45.0,'$45 per foot starting at 18"'),
        -- Per-inch adders (no threshold, apply immediately)
        (30,'LS2000','U','per_inch',4.0,40.0,'$40 per inch starting at 4"'),
        (31,'LS2000','T','per_inch',4.0,50.0,'$50 per inch starting at 4"'),
        (32,'LS2100','U','per_inch',4.0,40.0,'$40 per inch starting at 4"'),
        (33,'LS2100','T','per_inch',4.0,50.0,'$50 per inch starting at 4"'),
        (34,'LS6000','CPVC','per_inch',4.0,50.0,'$50 per inch starting at 4"'),
        (35,'LS7000','CPVC','per_inch',4.0,50.0,'$50 per inch starting at 4"')
    """
    )


def downgrade():
    # Drop length_adder_rules table
    op.drop_table('length_adder_rules')
