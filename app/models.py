from datetime import datetime, timezone 
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Agent(db.Model):
    __tablename__ = 'agents'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    
    shipping_points: so.Mapped[List['Factory']] = so.relationship(
                    back_populates='agent')
    def __repr__(self):
        return '<Agent {}>'.format(self.name)

    
class Factory(db.Model):
    __tablename__ = 'shipping_points'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    agent_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("agents.id"),
                                               index=True)
    
    agent: so.Mapped['Agent'] = so.relationship(
                    back_populates='shipping_points')
    shippings: so.Mapped[List['Shipping']] = so.relationship(
                    back_populates='shipping_point')
    
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)


class Category(db.Model):
    __tablename__ = 'categories'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    production: so.Mapped['Product'] = so.relationship(
                    back_populates='category')
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)

class Product(db.Model):
    __tablename__ = 'products'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("categories.id"),
                                               index=True)
    
    category: so.Mapped['Category'] = so.relationship(
                    back_populates='production')
    
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)
    
class Transport(db.Model):
    __tablename__ = 'transports'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)
    
class Shipping(db.Model):
    __tablename__ = 'shipments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Product.id),
                                               index=True)
    transport_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Transport.id),
                                               index=True)
    shipping_point_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Factory.id),
                                               index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True)
    monthly_plan: so.Mapped[int] = so.mapped_column()
    shipping_plan: so.Mapped[int] = so.mapped_column()
    shipping_done: so.Mapped[int] = so.mapped_column()
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    shipping_point: so.Mapped['Factory'] = so.relationship(
                    back_populates='shippings')
    def __repr__(self):
        return '<Shipping {}>'.format(self.name)
    