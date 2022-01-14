"""add content column to posts

Revision ID: 00f4016389aa
Revises: df254f93b611
Create Date: 2022-01-14 19:29:02.137009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f4016389aa'
down_revision = 'df254f93b611'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
