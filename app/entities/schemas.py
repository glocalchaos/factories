from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import ShippingModel, FactoryModel
from marshmallow import fields, Schema, post_dump
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

class FactorySchema(ma.SQLAlchemySchema):#ma.SQLAlchemySchema):
    # class Meta:
        # model = FactoryModel
        # include_fk = True
    class Meta:
        model = FactoryModel
    name = auto_field()
    
    daily = Nested(PlanVsFactSchema)
    sum = Nested(PlanVsFactSchema)