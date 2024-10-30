from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class FactoryModel(db.Model):
    __tablename__ = 'factories'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    agent_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("agents.id"),
                                               index=True)
    

    industry: so.Mapped[str] = so.mapped_column(sa.String(64), index=True) # тип завода (переработка и т. д.)
    
    # agent = so.relationship('Agent', foreign_keys=sa.Column(sa.ForeignKey('agents.id')))
    # agent: so.Mapped[int] = so.mapped_column(sa.ForeignKey("agents.id'"))

    shippings = so.relationship('ShippingModel')#, backref=so.backref('shipments'))

    
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)