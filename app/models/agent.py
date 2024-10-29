from typing import List
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.factory import Factory
# from app.models.factory import Factory

class Agent(db.Model):
    __tablename__ = 'agents'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    shipping_points: so.Mapped[List['Factory']] = so.relationship()
    # shipping_points = so.relationship('Factory', backref=so.backref('factories'))

    def __repr__(self):
        return '<Agent {}>'.format(self.name)