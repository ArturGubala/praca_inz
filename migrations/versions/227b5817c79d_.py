"""empty message

Revision ID: 227b5817c79d
Revises: 2fa404162072
Create Date: 2023-01-09 20:33:21.049160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '227b5817c79d'
down_revision = '2fa404162072'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('edition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('language',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code_two_char', sa.String(length=2), nullable=False),
    sa.Column('country_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code_two_char'),
    sa.UniqueConstraint('country_name')
    )
    op.create_table('platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alias', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('alias'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('platform')
    op.drop_table('language')
    op.drop_table('edition')
    # ### end Alembic commands ###
