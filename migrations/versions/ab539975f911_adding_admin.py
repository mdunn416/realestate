"""adding admin

Revision ID: ab539975f911
Revises: ecd9e7088e99
Create Date: 2020-12-25 13:04:26.557837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab539975f911'
down_revision = 'ecd9e7088e99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin_flag', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin_flag')
    # ### end Alembic commands ###
