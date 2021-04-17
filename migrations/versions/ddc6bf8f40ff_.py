"""empty message

Revision ID: ddc6bf8f40ff
Revises: 8132678ec54e
Create Date: 2021-04-10 18:14:44.652225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddc6bf8f40ff'
down_revision = '8132678ec54e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_notification_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_notification_read_time')
    # ### end Alembic commands ###
