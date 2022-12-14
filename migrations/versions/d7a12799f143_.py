"""empty message

Revision ID: d7a12799f143
Revises: e99f3a52bfaa
Create Date: 2022-09-05 19:28:24.944813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a12799f143'
down_revision = 'e99f3a52bfaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addproduct', schema=None) as batch_op:
        batch_op.add_column(sa.Column('size', sa.Text(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addproduct', schema=None) as batch_op:
        batch_op.drop_column('size')

    # ### end Alembic commands ###
