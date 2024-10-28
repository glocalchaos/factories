from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
# from app.models.agent import Agent
# from app.models.shipping import Shipping

class Factory(db.Model):
    __tablename__ = 'shipping_points'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    agent_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("agents.id"),
                                               index=True)
    
    # agent: so.Mapped['Agent'] = so.relationship(
    #                 back_populates='shipping_points')
    agent = so.relationship('agents', foreign_keys=sa.Column(sa.ForeignKey('agents.id')))
    # shippings: so.Mapped[List['Shipping']] = so.relationship(
    #                 back_populates='shipping_point')
    shippings = so.relationship('Shipping', backref=so.backref('shipments'))
    
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)