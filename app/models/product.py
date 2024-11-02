import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

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