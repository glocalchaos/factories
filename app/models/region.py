from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.factory import FactoryModel

class Region(db.Model):
    __tablename__ = 'regions'
    region_code: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True, nullable=False)
    shipping_points: so.Mapped[List['FactoryModel']] = so.relationship()

    def __repr__(self):
        return '<Region {}>'.format(self.name)