"""update sleepSession to include type

Revision ID: 49e2b3818910
Revises: 6fbcf983b2f7
Create Date: 2021-12-07 09:15:51.180730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e2b3818910'
down_revision = '6fbcf983b2f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sleepsessions', sa.Column('is_sleep', sa.Boolean(), server_default='true', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sleepsessions', 'is_sleep')
    # ### end Alembic commands ###
