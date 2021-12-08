"""first

Revision ID: dea3525ade2a
Revises: 9f0cf8db6476
Create Date: 2021-12-09 02:11:45.351416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dea3525ade2a'
down_revision = '9f0cf8db6476'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url_table', sa.Column('date', sa.DATE(), nullable=True))
    op.add_column('url_table', sa.Column('time', sa.TIME(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('url_table', 'time')
    op.drop_column('url_table', 'date')
    # ### end Alembic commands ###
