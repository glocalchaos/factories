from app import db
from typing import Mapping, Iterable
from ..models.factory import FactoryModel
from .agent_repository import AgentRepository

class FactoryRepository:
    def upload_factories(self, agent_points_dict: Mapping[str, Iterable[str]]): # TODO ИТЕРАБЛЕ of strs
        session = db.session
    
        # TODO сделать не по корявому
        for agent in agent_points_dict.keys():
            # session.add(FactoryModel(
            #     name = FactoryModel,
            # ))
            
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
    
    def get_id_by_name(self, name: str) -> int:
        session = db.session
        product = session.query(FactoryModel).filter(FactoryModel.name == name).scalar()
        return product.id