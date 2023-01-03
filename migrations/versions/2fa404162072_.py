"""empty message

Revision ID: 2fa404162072
Revises: 
Create Date: 2023-01-02 20:03:06.262092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fa404162072'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bulk_pack_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('abbreviation', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbreviation'),
    sa.UniqueConstraint('name')
    )
    op.create_table('catalogue_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('document_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('abbreviation', sa.String(length=10), nullable=False),
    sa.Column('numeration_template', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbreviation'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurement_unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('abbreviation', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbreviation'),
    sa.UniqueConstraint('name')
    )
    op.create_table('producer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email_address', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('trade_partner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email_address', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.Column('street', sa.String(length=50), nullable=True),
    sa.Column('street_number', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('post_code', sa.String(length=50), nullable=True),
    sa.Column('nip', sa.String(length=50), nullable=True),
    sa.Column('regon', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('name')
    )
    op.create_table('warehouse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.create_table('app_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('password', sa.LargeBinary(length=255), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('email_address', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_address')
    )
    op.create_table('catalogue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measurement_unit_id', sa.Integer(), nullable=False),
    sa.Column('catalogue_type_id', sa.Integer(), nullable=False),
    sa.Column('bulk_pack_id', sa.Integer(), nullable=False),
    sa.Column('producer_id', sa.Integer(), nullable=False),
    sa.Column('stock_code', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('alias', sa.String(length=50), nullable=True),
    sa.Column('last_purchase_price', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('bulk_pack_capacity', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('no_bulk_pack_on_palette', sa.Integer(), nullable=True),
    sa.Column('burning_time', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('height', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('width', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('diameter', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['bulk_pack_id'], ['bulk_pack_type.id'], ),
    sa.ForeignKeyConstraint(['catalogue_type_id'], ['catalogue_type.id'], ),
    sa.ForeignKeyConstraint(['measurement_unit_id'], ['measurement_unit.id'], ),
    sa.ForeignKeyConstraint(['producer_id'], ['producer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('alias'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('stock_code')
    )
    op.create_table('document_number_parts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('document_date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=True),
    sa.Column('last_document_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouse.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_type_id', sa.Integer(), nullable=False),
    sa.Column('app_user_id', sa.Integer(), nullable=False),
    sa.Column('warehouse_from_id', sa.Integer(), nullable=False),
    sa.Column('warehouse_to_id', sa.Integer(), nullable=False),
    sa.Column('trade_partner_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=50), nullable=False),
    sa.Column('date_added', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('modification_date', sa.DateTime(), nullable=True),
    sa.Column('total', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['app_user_id'], ['app_user.id'], ),
    sa.ForeignKeyConstraint(['document_type_id'], ['document_type.id'], ),
    sa.ForeignKeyConstraint(['trade_partner_id'], ['trade_partner.id'], ),
    sa.ForeignKeyConstraint(['warehouse_from_id'], ['warehouse.id'], ),
    sa.ForeignKeyConstraint(['warehouse_to_id'], ['warehouse.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('catalogue_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=18, scale=2), nullable=False),
    sa.Column('price', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['catalogue_id'], ['catalogue.id'], ),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    op.drop_table('document')
    op.drop_table('document_number_parts')
    op.drop_table('catalogue')
    op.drop_table('app_user')
    op.drop_table('warehouse')
    op.drop_table('trade_partner')
    op.drop_table('role')
    op.drop_table('producer')
    op.drop_table('measurement_unit')
    op.drop_table('document_type')
    op.drop_table('catalogue_type')
    op.drop_table('bulk_pack_type')
    # ### end Alembic commands ###