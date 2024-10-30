from app import db
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from ..models.transport import TransportModel

class TransportRepository:
    # def __init__
    def upload_transport(self, transports): # TODO ИТЕРАБЛЕ of strs
        session = db.session
    
        # TODO сделать не по корявому
        for transport_name in transports:
            if TransportModel.query(exists(TransportModel).where(name == transport_name)).scalar(): # ERROR моделька не видит собственные поля???(
                continue
            # if TransportModel.exists(transport_name):
            #     continue
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
        
        