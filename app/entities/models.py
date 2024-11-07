from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
from sqlalchemy import func
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.hybrid import hybrid_method


from app import db, ma



class ShippingModel(db.Model):
    __tablename__ = 'shipments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("products.id"),
                                               index=True)
    transport_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("transports.id"),
                                               index=True)
    shipping_point_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("factories.id"),
                                               index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True)
    monthly_plan: so.Mapped[Optional[float]] = so.mapped_column()
    shipping_plan: so.Mapped[Optional[float]] = so.mapped_column()
    shipping_done: so.Mapped[Optional[float]] = so.mapped_column()
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))


    shipping_point: so.Mapped['FactoryModel'] = so.relationship(
                    back_populates='shippings')
    # transport: so.Mapped['TransportModel'] = so.relationship(
    #                 back_populates='shippings_involved')

    def __repr__(self):
        return '<Shipping {}>'.format(self.name)
    
    # @hybrid_method
    # def monthly_plan_by_factory(self, factory_id : int, date: datetime) -> int:
    #     return ShippingModel.query(
    #         func.sum(ShippingModel.monthly_plan)
    #     ).join(TransportModel, self.id==ShippingModel.transport_id).filter(
    #         ShippingModel.shipping_point_id==factory_id,
    #         ShippingModel.timestamp==date,
    #         TransportModel.name==self.name
    #     ).one()[0]
    
    # @hybrid_method
    # def daily_plan_by_factory(self, factory_id : int, date: datetime) -> int:
    #     return ShippingModel.query(
    #         func.sum(ShippingModel.shipping_plan)
    #     ).join(TransportModel, self.id==ShippingModel.transport_id).filter(
    #         ShippingModel.shipping_point_id==factory_id,
    #         ShippingModel.timestamp==date,
    #         TransportModel.name==self.name
    #     ).one()[0]
    
    # @hybrid_property
    # def daily_plan_by_factory(self, factory : FactoryModel, date_from: datetime, date_to: datetime) -> int:
    #     pass

'''
    SELECT s.timestamp, s.id, products.name as product, transports.name as transport, factories.name as factory,
		s.monthly_plan, s.shipping_plan, s.shipping_done, s.notes from shipments as s JOIN products ON products.id = s.product_id
 							JOIN transports on s.transport_id = transports.id
							JOIN factories on s.shipping_point_id = factories.id
'''


class TransportModel(db.Model):
    __tablename__ = 'transports'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    
    # shippings_involved: so.Mapped[list['ShippingModel']] = so.relationship(
    #                 "ShippingModel",
    #                 back_populates='transport')
    
    def __repr__(self):
        return '<Transport {}>'.format(self.name)
    
    # @hybrid_method
    # def monthly_plan_by_factory(self, factory_id : int, date: datetime) -> int:
    #     return ShippingModel.query(
    #         func.sum(ShippingModel.monthly_plan)
    #     ).join(TransportModel, self.id==ShippingModel.transport_id).filter(
    #         ShippingModel.shipping_point_id==factory_id,
    #         ShippingModel.timestamp==date,
    #         TransportModel.name==self.name
    #     ).one()[0]

class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    production: so.Mapped['ProductModel'] = so.relationship(
                    back_populates='category')
    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
    # @hybrid_method
    # def monthly_plan_by_factory(factory_id: int, date: datetime) -> int:
    #     return ShippingModel.query(
    #         func.sum(ShippingModel.monthly_plan)
    #     ).join(ProductModel, ShippingModel.product_id==ProductModel.id
    #     ).join(
    #         CategoryModel, ProductModel.category_id==CategoryModel.id
    #     ).filter(
    #         ShippingModel.shipping_point_id==factory_id,
    #         CategoryModel.name==category[0]
    #     ).one()[0]

class FactoryModel(db.Model):
    __tablename__ = 'factories'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("regions.code"),
                                               index=True,
                                               nullable=True) # ! пока неполные данные - так
    

    industry: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), nullable=True) # TODO тип завода (переработка и т. д.)
    

    shippings : so.Mapped['ShippingModel'] = so.relationship(
                    back_populates='shipping_point')

    
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)
    
    @hybrid_method
    def sum_plan(self, from_date: datetime, to_date: datetime) -> int:
        return ShippingModel.query(
            func.sum(ShippingModel.shipping_plan)
        ).filter(
            ShippingModel.shipping_point==self,
            ShippingModel.timestamp>=from_date,
            ShippingModel.timestamp<=to_date,
        ).one()[0]
    
    @hybrid_method
    def sum_done(self, from_date: datetime, to_date: datetime) -> int:
        return ShippingModel.query(
            func.sum(ShippingModel.shipping_done)
        ).filter(
            ShippingModel.shipping_point==self,
            ShippingModel.timestamp>=from_date,
            ShippingModel.timestamp<=to_date,
        ).one()[0]
    
    @hybrid_method
    def daily_plan(self, date: datetime) -> int:
        return ShippingModel.query(ShippingModel.shipping_plan).filter(
            ShippingModel.timestamp == date
        ).one()[0]
    
    @hybrid_method
    def daily_done(self, date: datetime) -> int:
        return ShippingModel.query(ShippingModel.shipping_done).filter(
            ShippingModel.timestamp == date
        ).one()[0]
    
    # TODO
    # @hybrid_method
    # def transport_used(self, from_date: datetime, to_date: datetime) -> List[TransportModel]:
    #     return (FactoryModel.query(
    #         FactoryModel, ShippingModel, TransportModel
    #     ).distinct(
    #         ShippingModel.transport_id
    #     ).filter(
    #         ShippingModel.shipping_point==self
    #     ).filter(
    #         ShippingModel.transport_id==TransportModel.id
    #     ).filter(
    #         ShippingModel.timestamp>=from_date
    #     ).filter(
    #         ShippingModel.timestamp<=to_date
    #     ).all())
    
    # TODO
    # @hybrid_method
    # def product_category_produced(self, from_date: datetime, to_date: datetime) -> List[ProductCategory]:
    #     pass
    


class ProductModel(db.Model):
    __tablename__ = 'products'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True,
                                                unique=True)
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("categories.id"),
                                            index=True)
    
    category: so.Mapped['CategoryModel'] = so.relationship(
                    back_populates='production')
    
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)
    


class RegionModel(db.Model):
    __tablename__ = 'regions'
    code: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True, nullable=False)
    shipping_points: so.Mapped[List['FactoryModel']] = so.relationship()

    def __repr__(self):
        return '<Region {}>'.format(self.name)
    
class RegionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RegionModel
    code = ma.auto_field()
    name = ma.auto_field()
    shipping_points = ma.auto_field()



