from app import db
from typing import Mapping, Iterable, List
from ..models.factory import FactoryModel
from ..models.transport import TransportModel
from ..models.shipping import ShippingModel
from ..models.category import CategoryModel
from ..models.product import ProductModel
from .region_repository import RegionRepository

class FactoryRepository:
    def upload_factories(self, agent_points_dict: Mapping[str, Iterable[str]]):
        session = db.session
    
        # TODO сделать не по корявому            
        session.commit()
        session.close()

    def upload_factory(self, factory_name: str, agent_name=None):
        session = db.session
        session.add(FactoryModel(
                    name = factory_name,
                    # agent_id = agent_id,
                ))
        
    
    def get_id_by_name(self, name: str) -> int:
        session = db.session
        factory = session.query(
            FactoryModel
        ).filter(
            FactoryModel.name == name
        ).scalar()
        if factory is None:
            return None
        session.close()
        return factory.id
    

    def get_used_transports(factory: FactoryModel) -> List[TransportModel]:
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
    
    def get_product_categories(factory: FactoryModel) -> List[CategoryModel]:
        session = db.session
        categories = session.query(ShippingModel).filter(ShippingModel.shipping_point == factory).join(ProductModel).distinct(ProductModel.category_id).join(CategoryModel).with_entities(CategoryModel.name).all()
        session.close()
        return categories