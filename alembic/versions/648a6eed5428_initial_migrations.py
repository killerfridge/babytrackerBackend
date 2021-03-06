"""initial_migrations

Revision ID: 648a6eed5428
Revises: 
Create Date: 2021-11-27 23:14:44.058197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '648a6eed5428'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('babies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_awake', sa.Boolean(), server_default='True', nullable=False),
    sa.Column('is_feeding', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feeds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feed_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_start', sa.Boolean(), nullable=False),
    sa.Column('baby_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['baby_id'], ['babies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sleeps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sleep_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_awake', sa.Boolean(), nullable=False),
    sa.Column('baby_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['baby_id'], ['babies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sleepsession',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sleep_start', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('sleep_end', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('sleep_length', sa.Float(), nullable=True),
    sa.Column('baby_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['baby_id'], ['babies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sleepsession')
    op.drop_table('sleeps')
    op.drop_table('feeds')
    op.drop_table('babies')
    # ### end Alembic commands ###
