"""
Add process_connection_type and process_connection_size columns, remove process_connection from base_models
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('base_models', sa.Column('process_connection_type', sa.Text(), nullable=True))
    op.add_column('base_models', sa.Column('process_connection_size', sa.Text(), nullable=True))
    op.drop_column('base_models', 'process_connection')

def downgrade():
    op.add_column('base_models', sa.Column('process_connection', sa.Text(), nullable=True))
    op.drop_column('base_models', 'process_connection_type')
    op.drop_column('base_models', 'process_connection_size') 