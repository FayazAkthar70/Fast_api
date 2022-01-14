"""finish posts table

Revision ID: f081c6d6111c
Revises: 9106a1a99a7f
Create Date: 2022-01-14 20:18:26.156390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f081c6d6111c'
down_revision = '9106a1a99a7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column("posts",sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
