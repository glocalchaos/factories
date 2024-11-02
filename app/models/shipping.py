from datetime import datetime
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
# from app.models.factory import FactoryModel

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


    # shipping_point = so.relationship('factories', foreign_keys=sa.Column(sa.ForeignKey('factories.id')))
    shipping_point: so.Mapped['FactoryModel'] = so.relationship(
                    back_populates='shippings')

    def __repr__(self):
        return '<Shipping {}>'.format(self.name)
    


'''
    SELECT s.timestamp, s.id, products.name as product, transports.name as transport, factories.name as factory,
		s.monthly_plan, s.shipping_plan, s.shipping_done, s.notes from shipments as s JOIN products ON products.id = s.product_id
 							JOIN transports on s.transport_id = transports.id
							JOIN factories on s.shipping_point_id = factories.id
'''