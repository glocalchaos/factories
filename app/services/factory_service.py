from datetime import datetime
from typing import Dict, List
from app.repositories.factory_repository import FactoryRepository
from app.repositories.transport_repository import TransportRepository
from app.services.utils import apply_shippings_product_filter, apply_shippings_transport_filter
from sqlalchemy import func, extract

from app.entities.models import CategoryModel, FactoryModel, ProductModel, RegionModel, ShippingModel, TransportModel
from app import db

class FactoryService:
    def __init__(self):
        self.factory_repository = FactoryRepository()
        self.transport_repository = TransportRepository()

    def upload_factory(self, factory_name: str, agent_name=None):
        self.factory_repository.upload_factory(factory_name, agent_name)

    def upload_factories(self, factories: Dict[str, int]):
        factories_list = {}
        for name, region_code in factories.items:
            if not self.factory_repository.exists_by_name:
                factories_list[name] = region_code
            self.factory_repository.upload_factories(factories_list)

    def get_by_name(self, name: str):
        return self.factory_repository.get_by_name(name)
    def get_transport_by_name(self, name: str):
        return self.transport_repository.get_by_name(name)
    
    def get_factories_by_region(self, region: RegionModel) -> List[RegionModel]:
        return self.factory_repository.get_by_region(region)
    
    # Месячный план
    def sum_plan(self, factory: FactoryModel, date: datetime,
                 transport_types: List[TransportModel]=None,
                 products: List[ProductModel]=None) -> int:
        query = db.session.query(
            func.sum(ShippingModel.monthly_plan)
        )

        subquery = db.session.query(ShippingModel.product_id, 
                                    func.max(ShippingModel.monthly_plan
                                    ).label('monthly_plan'))
        subquery = apply_shippings_transport_filter(subquery, transport_types)
        subquery = apply_shippings_product_filter(subquery, products)
        
        query = query.select_from(
                    subquery.group_by(ShippingModel.product_id).subquery()
                )
        
        query = apply_shippings_transport_filter(query, transport_types) 
        query = apply_shippings_product_filter(query, products)

        subquery = subquery.filter(ShippingModel.shipping_point==factory
                                ).filter(
                                   extract("year", ShippingModel.timestamp) == date.year
                                ).filter(
                                   extract("month", ShippingModel.timestamp) == date.month
                                )

        query = query.filter(ShippingModel.shipping_point==factory,
                            extract("year", ShippingModel.timestamp) == date.year,
                            extract("month", ShippingModel.timestamp) == date.month
                )
        # print(query) # & OTLADKA
        return query.scalar()
    
    # Факт накопительно за период
    def sum_fact(self, factory: FactoryModel, 
                 from_date: datetime, 
                 to_date: datetime,
                 transport_types: List[TransportModel]=None,
                 products: List[ProductModel]= None) -> int:

        query = db.session.query(
            func.sum(ShippingModel.shipping_done)
        ).filter(
            ShippingModel.shipping_point==factory,
            ShippingModel.timestamp>=from_date,
            ShippingModel.timestamp<=to_date,
        )
        
        # if transport_types:
        query = apply_shippings_transport_filter(query, transport_types)
        # if products:
        query = apply_shippings_product_filter(query, products)
        

        return query.one()[0]
    
    # Факт за день
    def daily_fact(self, factory: FactoryModel, date: datetime,
                   transport_types: List[TransportModel]=None,
                   products: List[ProductModel]= None) -> int:

        query = db.session.query(
            func.sum(ShippingModel.shipping_done)
            ).filter(
            ShippingModel.timestamp == date,
            ShippingModel.shipping_point == factory
        )

        query = apply_shippings_transport_filter(query, transport_types)
        query = apply_shippings_product_filter(query, products)
        
        return query.first()[0]
    
    # План на день
    def daily_plan(self, factory: FactoryModel, date: datetime,
                   transport_types: List[TransportModel]=None,
                   products: List[ProductModel]= None) -> int:
        query = db.session.query(
            func.sum(ShippingModel.shipping_plan)
            ).filter(
            ShippingModel.timestamp == date,
            ShippingModel.shipping_point == factory
        )

        query = apply_shippings_transport_filter(query, transport_types)
        query = apply_shippings_product_filter(query, products)
        
        return query.one()[0]
    
    def get_used_transports_by_factory(self, 
                                   factory: FactoryModel, 
                                   from_date: datetime, 
                                   to_date: datetime,
                                   transport_types: List[TransportModel]=None,
                                   products: List[ProductModel]=None) -> List[TransportModel]:
        query = db.session.query(
            TransportModel,
            # ShippingModel,
        ).join(
            ShippingModel
        ).distinct(
            ShippingModel.transport_id
        ).filter(
            ShippingModel.shipping_point==factory,
            ShippingModel.transport_id==TransportModel.id,
            ShippingModel.timestamp>=from_date,
            ShippingModel.timestamp<=to_date,
        )


        # * TODO FIX: filters
        query = apply_shippings_transport_filter(query, transport_types)
        # CHECK
        if products:
            query = apply_shippings_product_filter(query, products)
        # if product_ids is not None:
        #     query = query.filter(
        #         ShippingModel.product_id in product_ids
        #     )

        return query.all()
    
    def get_shipped_categories_by_factory(self, 
                                        factory: FactoryModel, 
                                        from_date: datetime, 
                                        to_date: datetime,
                                        transport_types: List[TransportModel]=None,
                                        products: List[ProductModel]=None) -> List[CategoryModel]:
        # TODO 
        query = db.session.query(
                CategoryModel,
                # ShippingModel,
            ).join(
                ProductModel
            ).join(
                ShippingModel
            ).distinct(
                CategoryModel.id
            ).filter(
                ShippingModel.shipping_point == factory,
                ShippingModel.timestamp>=from_date,
                ShippingModel.timestamp<=to_date,
            )
        query = apply_shippings_transport_filter(query, transport_types)
        query = apply_shippings_product_filter(query, products)
        # print(query)
        return query.all()
