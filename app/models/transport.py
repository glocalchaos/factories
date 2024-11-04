from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models.shipping import ShippingModel
from app import db

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