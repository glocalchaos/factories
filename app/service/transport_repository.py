from app import db
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from typing import Iterable
from ..models.transport import TransportModel

class TransportRepository:
    # def __init__
    def upload_transport(self, transports: Iterable[str]): # TODO ИТЕРАБЛЕ of strs
        session = db.session
    
        # TODO сделать не по корявому
        for transport_name in transports:
            if session.query(TransportModel).filter(TransportModel.name == transport_name).scalar(): # ERROR моделька не видит собственные поля???(
                continue

            session.add(TransportModel(
                name = transport_name,
            ))
            
        session.commit()
        session.close()
'''
            # t = Transport(
            #     name = transport_name,
            # )
            # session.add(t)
            # try:
            #     session.commit()
            # except IntegrityError:
            #     session.rollback()
            #     session.flush()
'''
        
        