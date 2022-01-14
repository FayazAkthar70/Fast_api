"""add foreign key to post table

Revision ID: 9106a1a99a7f
Revises: 72788147af0c
Create Date: 2022-01-14 19:57:37.886864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9106a1a99a7f'
down_revision = '72788147af0c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
