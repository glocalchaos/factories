from app import db
from typing import Mapping, Iterable
from ..models.factory import FactoryModel
from .region_repository import RegionRepository

class FactoryRepository:
    def upload_factories(self, agent_points_dict: Mapping[str, Iterable[str]]):
        session = db.session
    
        # TODO сделать не по корявому
        for agent in agent_points_dict.keys():
            AgentRepository().upload_agent(agent_name=agent)
            for factory in agent_points_dict[agent]:
                if session.query(FactoryModel).filter(FactoryModel.name == factory).scalar():
                    continue
                session.add(FactoryModel(
                    name = factory,
                    agent_id = AgentRepository().get_agent_id_by_name(agent_name=agent)
                ))
            
        session.commit()
        session.close()
    def upload_factory(self, factory_name: str, agent_name=None):
        session = db.session
        agent_id = AgentRepository().get_agent_id_by_name(agent_name=agent_name)
        session.add(FactoryModel(
                    name = factory_name,
                    agent_id = agent_id,
                ))
        
    
    def get_id_by_name(self, name: str) -> int:
        session = db.session
        factory = session.query(FactoryModel).filter(FactoryModel.name == name).scalar()
        if factory is None:
            return None
        return factory.id