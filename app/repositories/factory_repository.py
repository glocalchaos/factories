from app import db
from typing import Dict, Mapping, Iterable, List
from ..entities.models import FactoryModel, RegionModel, TransportModel, ShippingModel, CategoryModel, ProductModel
from .region_repository import RegionRepository

class FactoryRepository:
    def upload_factory(self, factory_name: str, region_code: int):
        session = db.session
        session.add(FactoryModel(
                    name = factory_name,
                    region_id = region_code,
                ))
        session.commit()
        session.close()
        
    def upload_factory_model(self, model: FactoryModel):
        session = db.session
        session.add(model)
        session.commit()
        session.close()

    def upload_factories_models(self, models: List[FactoryModel]):
        session = db.session
        session.add_all(models)
        session.commit()
        session.close()
    
    def upload_factories(self, factories: Dict[str, int]):
        session = db.session
        for name, region_code in factories.items:
            session.add(FactoryModel(
                region_id=region_code,
                name=name
            ))
        session.commit()
        session.close()
        
    def get_by_name(self, name: str) -> FactoryModel:
        return db.session.query(
            FactoryModel
        ).filter(
            FactoryModel.name == name
        ).scalar()
    
    def get_by_id(self, id: int) -> FactoryModel:
        return db.session.query(
            FactoryModel
        ).filter(
            FactoryModel.id == id
        ).scalar()
    
    def get_by_region(self, region: RegionModel) -> List[RegionModel]:
        return db.session.query(
            FactoryModel
        ).filter(
            FactoryModel.region == region
        ).all()
    
    def exists_by_id(self, id: int) -> bool:
        return self.get_by_id(id) is not None
    
    def exists_by_name(self, name: str) -> bool:
        return self.get_by_name(name) is not None


    def get_used_transports(self, factory: FactoryModel) -> List[TransportModel]:
        session = db.session
        transports = session.query(
            FactoryModel, ShippingModel, TransportModel
        ).distinct(
            ShippingModel.transport_id
        ).filter(
            ShippingModel.shipping_point==factory
        ).filter(
            ShippingModel.transport_id==TransportModel.id
        ).with_entities(
            TransportModel.name
        ).all()
        session.close()
        return transports
    
    def get_product_categories(self, factory: FactoryModel) -> List[CategoryModel]:
        session = db.session
        categories = session.query(ShippingModel).filter(ShippingModel.shipping_point == factory).join(ProductModel).distinct(ProductModel.category_id).join(CategoryModel).with_entities(CategoryModel.name).all()
        session.close()
        return categories