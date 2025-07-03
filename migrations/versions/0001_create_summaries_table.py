from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'summaries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('summary', sa.Text, nullable=False),
        sa.Column('source', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

def downgrade():
    op.drop_table('summaries') 