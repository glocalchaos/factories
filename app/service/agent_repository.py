from app import db
from typing import Iterable
from ..models.agent import AgentModel

#   TODO catch ERRORS где надо

class AgentRepository:
    def upload_agents(self, agents: Iterable[str]):
        session = db.session
    
        # TODO сделать не по корявому
        for agent_name in agents:
            if session.query(AgentModel).filter(AgentModel.name == agent_name).scalar():
                continue

            session.add(AgentModel(
                name = agent_name,
            ))
            
        session.commit()
        session.close()

        
    def upload_agent(self, agent_name: str):
        session = db.session
        if session.query(AgentModel).filter(AgentModel.name == agent_name).scalar():
            return

        session.add(AgentModel(
            name = agent_name,
        ))
        session.commit()
        session.close()
    
    def get_agent_id_by_name(self, agent_name: str) -> int:
        session = db.session
        agent = session.query(AgentModel).filter(AgentModel.name == agent_name).scalar()
        return agent.id


    