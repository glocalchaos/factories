from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .models import ShippingModel, FactoryModel
from marshmallow import fields, Schema, post_dump, validate
from marshmallow.fields import Nested

from app import db, ma

class PlanVsFactSchema(Schema):

    product_category = fields.String(allow_none=True, missing=None)
    transport_type  = fields.String(allow_none=True, missing=None)
    plan=fields.Integer()
    fact=fields.Integer()

    @post_dump
    def remove_empty_fields(self, data, **kwargs):
        return {k: v for k, v in data.items() if v not in [None, ""]}

planfact_schema = PlanVsFactSchema()
planfact_schemas = PlanVsFactSchema(many=True)

class FactorySchema(ma.SQLAlchemySchema):
    factory_name = fields.String()
    
    daily = Nested(PlanVsFactSchema)
    sum = Nested(PlanVsFactSchema)

factory_schema = FactorySchema()

class TransportSchema(Schema):
    factory_name = fields.String()
    transports=fields.List(fields.Nested(PlanVsFactSchema))
transport_schema = TransportSchema()



# TODO переделать схемы без дублирования FactorySchema?

class NameFactSchema(Schema):
    name = fields.String()
    value = fields.Integer()

class FactoryGeneralSchema(Schema):
    name = fields.String()
    value = fields.Integer()

    oil_type = fields.List(fields.Nested(NameFactSchema))
    transport_type = fields.List(fields.Nested(NameFactSchema))

class RegionSchema(Schema):
    region = fields.String()
    code = fields.Integer()
    
    factories = fields.List(fields.Nested(FactoryGeneralSchema), validate=validate.Length(min=1))

class AllSchema(Schema):
    regions_info = fields.List(fields.Nested(RegionSchema))

    @post_dump
    def remove_empty_fields(self, data, **kwargs):
        return {k: v for k, v in data.items() if v not in [None, ""]}