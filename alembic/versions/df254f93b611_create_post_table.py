"""create post table

Revision ID: df254f93b611
Revises: 
Create Date: 2022-01-14 17:12:29.600820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df254f93b611'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                            sa.Column("title",sa.String(),nullable=False))
                            
    pass


def downgrade():
    op.drop_table("posts")
    pass
