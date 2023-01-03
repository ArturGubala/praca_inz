from flask_marshmallow.fields import fields
from marshmallow import post_load

from . import marshmallow
from .models import (
    AppUser, Producer, BulkPackType, Catalogue,
    DocumentType, Document, Item, DocumentNumberParts
)


class UserSchema(marshmallow.Schema):
    name = fields.Str()
    surname = fields.Str()
    phone_number = fields.Str()
    email_address = fields.Email()

    @post_load
    def make_user(self, data, **kwargs) -> dict:
        return AppUser(**data)


class ProducerSchema(marshmallow.Schema):
    name = fields.Str()
    email_address = fields.Email()
    phone_number = fields.Str()

    @post_load
    def make_producer(self, data, **kwargs) -> dict:
        return Producer(**data)


class BulkPackTypeSchema(marshmallow.Schema):
    name = fields.Str()
    abbreviation = fields.Str()

    @post_load
    def make_bulk_pack_type(self, data, **kwargs) -> dict:
        return BulkPackType(**data)


class CatalogueSchema(marshmallow.Schema):
    measurement_unit_id = fields.Int()
    catalogue_type_id = fields.Int()
    bulk_pack_id = fields.Int()
    producer_id = fields.Int()
    stack_code = fields.Str()
    name = fields.Str()
    alias = fields.Str()
    last_purchase_price = fields.Decimal()
    bulk_pack_capacity = fields.Float()
    no_bulk_pack_on_palette = fields.Int()
    burning_time = fields.Float()
    height = fields.Float()
    width = fields.Float()
    diameter = fields.Float()

    @post_load
    def make_catalogue(self, data, **kwargs) -> dict:
        return Catalogue(**data)


class DocumentTypeSchema(marshmallow.Schema):
    name = fields.Str()
    abbreviation = fields.Str()
    numeration_template = fields.Str()

    @post_load
    def make_document_type(self, data, **kwargs) -> dict:
        return DocumentType(**data)


class DocumentSchema(marshmallow.Schema):
    document_type_id = fields.Int()
    app_user_id = fields.Int()
    warehouse_from_id = fields.Int()
    warehouse_to_id = fields.Int()
    trade_partner_id = fields.Int()
    number = fields.Str()
    total = fields.Decimal()

    @post_load
    def make_document(self, data, **kwargs) -> dict:
        return Document(**data)


class ItemSchema(marshmallow.Schema):
    document_id = fields.Int()
    catalogue_id = fields.Int()
    quantity = fields.Float()
    price = fields.Decimal()
    amount = fields.Float()

    @post_load(pass_many=True)
    def make_item(self, data, **kwargs) -> dict:
        items = [Item(**params) for params in data]

        return items


class DocumentNumberPartsSchema(marshmallow.Schema):
    warehouse_id = fields.Int()
    document_date = fields.Date()
    last_document_number = fields.Int()

    @post_load
    def make_document_numers_parts(self, data, **kwargs) -> dict:
        return DocumentNumberParts(**data)
