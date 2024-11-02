from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models.shipping import ShippingModel
from app import db

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