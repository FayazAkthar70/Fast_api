"""create table users

Revision ID: 72788147af0c
Revises: 00f4016389aa
Create Date: 2022-01-14 19:37:55.996619

"""
from datetime import timezone
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP, String


# revision identifiers, used by Alembic.
revision = '72788147af0c'
down_revision = '00f4016389aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table("users")
    pass
