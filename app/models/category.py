import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.product import ProductModel

class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    production: so.Mapped['ProductModel'] = so.relationship(
                    back_populates='category')
    def __repr__(self):
        return '<ShippingPoint {}>'.format(self.name)