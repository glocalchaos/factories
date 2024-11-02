from app import db
from typing import Dict
from ..models.region import RegionModel

#   TODO catch ERRORS где надо

class RegionRepository:
    def upload_regions(self, regions: Dict[str, int]):
        session = db.session
    
        # TODO сделать не по корявому
        for name, code in regions.items():
            if session.query(RegionModel).filter(RegionModel.code == code).scalar():
                continue

            session.add(RegionModel(
                name = name,
                code = code
            ))
            
        session.commit()
        session.close()

        
    # def upload_region(self, agent_name: str):
    #     session = db.session
    #     if session.query(RegionModel).filter(RegionModel.name == agent_name).scalar():
    #         return

    #     session.add(RegionModel(
    #         name = agent_name,
    #     ))
    #     session.commit()
    #     session.close()
    
    # def get_agent_id_by_name(self, agent_name: str) -> int:
    #     session = db.session
    #     agent = session.query(RegionModel).filter(RegionModel.name == agent_name).scalar()
    #     if agent:
    #         return agent.id
    #     else:
    #         return None


    