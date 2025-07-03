"""add tasks table

Revision ID: 0002
Revises: 0001
Create Date: 2024-03-07
"""
from alembic import op
import sqlalchemy as sa

# Create an enum type for task status
task_status = sa.Enum('pending', 'processing', 'completed', 'failed', name='taskstatus')

def upgrade():
    # Create the enum type
    task_status.create(op.get_bind())
    
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('status', task_status, nullable=False),
        sa.Column('result_id', sa.Integer, nullable=True),
        sa.Column('error', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

def downgrade():
    op.drop_table('tasks')
    task_status.drop(op.get_bind()) 