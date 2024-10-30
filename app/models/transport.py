from datetime import datetime, timezone 
from typing import List, Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import exists
from app import db

class TransportModel(db.Model):
    __tablename__ = 'transports'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    def __repr__(self):
        return '<Transport {}>'.format(self.name)
    
    # def exists(transport_name: str):
    #     return TransportModel.query(exists().where(TransportModel.name == transport_name)).scalar() # ERROR моделька не видит собственные поля???(