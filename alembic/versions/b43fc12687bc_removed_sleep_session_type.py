"""removed sleep session type

Revision ID: b43fc12687bc
Revises: 328d268973e2
Create Date: 2021-12-07 17:33:52.090107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b43fc12687bc'
down_revision = '328d268973e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sleepsessions', 'is_sleep')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sleepsessions', sa.Column('is_sleep', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
