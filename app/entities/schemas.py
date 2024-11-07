from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import ShippingModel, FactoryModel
from marshmallow import fields, Schema
from marshmallow.fields import Nested

from app import db, ma

class PlanVsFactSchema(Schema):
    plan=fields.Integer()
    fact=fields.Integer()

class FactorySchema(ma.SQLAlchemySchema):#ma.SQLAlchemySchema):
    # class Meta:
        # model = FactoryModel
        # include_fk = True
    class Meta:
        model = FactoryModel
    name = auto_field()
    
    daily = Nested(PlanVsFactSchema)
    sum = Nested(PlanVsFactSchema)