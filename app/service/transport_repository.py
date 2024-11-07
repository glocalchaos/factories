from app import db
from typing import Iterable
from ..entities.models import TransportModel


class TransportRepository:
    def upload_transports(self, transports: Iterable[str]):
        session = db.session
    
        # TODO сделать не по корявому
        for transport_name in transports:
            if session.query(TransportModel).filter(TransportModel.name == transport_name).scalar():
                continue

            session.add(TransportModel(
                name=transport_name,
            ))
            
        session.commit()
        session.close()

    def upload_transport(self, transport: str):
        session = db.session

        if session.query(TransportModel).filter(TransportModel.name == transport).scalar():
            return
        
        session.add(TransportModel(
                name=transport,
            ))
            
        session.commit()
        session.close()

    def get_id_by_name(self, name: str) -> int:
        session = db.session
        t = session.query(TransportModel).filter(TransportModel.name == name).scalar()
        return t.id
