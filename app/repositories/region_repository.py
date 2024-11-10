from app import db
from typing import Dict, List
# from multipledispatch import dispatch
from ..entities.models import RegionModel, FactoryModel

class RegionRepository:
    def upload_region_model(self, model: RegionModel):#code: int, name: str):
        session = db.session
        session.add(model)
        session.commit()
        session.close()

    def upload_region(self, code: int, name: str):
        session = db.session
        session.add(RegionModel(
                code=code,
                name=name
            ))
        session.commit()
        session.close()

    def upload_regions_models(self, models: List[RegionModel]):
        session = db.session
        session.add_all(models)
        session.commit()
        session.close()

    def upload_regions(self, regions: Dict[int, str]):
        session = db.session
        for code, name in regions.items:
            session.add(RegionModel(
                code=code,
                name=name
            ))
        session.commit()
        session.close()

    def get_all_regions(self) -> List[RegionModel]:
        regions = db.session.query(RegionModel).all() 
        regions = list(regions)
        return regions
    

    def get_by_code(self, code: int) -> RegionModel:
        return db.session.query(RegionModel).filter(RegionModel.code == code).one()

    def get_by_name(self, name: str) -> RegionModel:
        return db.session.query(RegionModel).filter(RegionModel.name == name).sone()
    
    def get_shipping_points_by_region(self, region: RegionModel) -> List[FactoryModel]:
        return db.session.query(FactoryModel).where(FactoryModel.region_id == region.code)

    def region_exists_by_code(self, code: int):
        return self.get_by_code(code) is not None

    def region_exists_by_name(self, name: str):
        return self.get_by_name(name) is not None