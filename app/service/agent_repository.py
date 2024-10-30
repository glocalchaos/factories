from app import db
from ..models.agent import AgentModel

#   TODO ERRORS где надо

class AgentRepository:
    def upload_agents(self, agents): # TODO ИТЕРАБЛЕ of strs
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
    def upload_agent(self, agent_name: str): # TODO return type int (agent id)
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


    