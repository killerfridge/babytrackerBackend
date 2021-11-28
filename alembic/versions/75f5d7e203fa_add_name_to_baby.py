"""add name to baby

Revision ID: 75f5d7e203fa
Revises: 029656c27efa
Create Date: 2021-11-28 13:46:33.888462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75f5d7e203fa'
down_revision = '029656c27efa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('babies', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('babies', 'name')
    # ### end Alembic commands ###
