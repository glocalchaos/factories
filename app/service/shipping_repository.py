from app import db
from sqlalchemy import func
from ..utils.parser_utils import ShippingRecordType
from collections import namedtuple
from datetime import datetime
from .product_repository import ProductRepository
from ..models.shipping import ShippingModel
from ..models.transport import TransportModel
from ..models.factory import FactoryModel
from ..models.product import ProductModel
from ..models.category import CategoryModel
from .transport_repository import TransportRepository
from .factory_repository import FactoryRepository

class ShippingRepository:
    def __init__(self):
        self._product_repo = ProductRepository()
        self._transport_repo = TransportRepository()
        self._factory_repo = FactoryRepository()

    def upload_shipping(self, shippingRecord : ShippingRecordType, cur_datetime: datetime):
        self._product_repo.upload_product(shippingRecord.product, shippingRecord.product_category) # TODO catch errors
        self._transport_repo.upload_transport(shippingRecord.transport)
        session = db.session

        factory_id = self._factory_repo.get_id_by_name(shippingRecord.shipping_point)

        print(self._factory_repo.get_id_by_name(shippingRecord.shipping_point), shippingRecord.shipping_point)
        if factory_id is None:
            self._factory_repo.upload_factory(shippingRecord.shipping_point)
        session.add(ShippingModel(
            product_id = self._product_repo.get_id_by_name(shippingRecord.product),
            transport_id = self._transport_repo.get_id_by_name(shippingRecord.transport),
            shipping_point_id = self._factory_repo.get_id_by_name(shippingRecord.shipping_point),
            timestamp = cur_datetime,
            monthly_plan = shippingRecord.monthly_plan,
            shipping_plan = shippingRecord.shipping_plan,
            shipping_done = shippingRecord.shipping_done,
            notes = shippingRecord.notes
        ))
        session.commit()
        session.close()

    def monthly_plan_by_factory(self, factory: FactoryModel):
        session = db.session
        return session.query(
            func.sum(ShippingModel.monthly_plan)
        ).filter(ShippingModel.shipping_point==factory).one()[0]
    
    def monthly_plan_by_factory_and_transport(self, factory: FactoryModel, transport: TransportModel):
        session = db.session
        #t_id = transport.id
        return session.query(
            func.sum(ShippingModel.monthly_plan)
        ).join(TransportModel, TransportModel.id==ShippingModel.transport_id).filter(
            ShippingModel.shipping_point==factory,
            TransportModel.name==transport[0]
        ).one()[0]
    
    def monthly_plan_by_factory_and_category(self, factory: FactoryModel, category: CategoryModel):
        session = db.session
        return session.query(
            func.sum(ShippingModel.monthly_plan)
        ).join(ProductModel, ShippingModel.product_id==ProductModel.id
        ).join(
            CategoryModel, ProductModel.category_id==CategoryModel.id
        ).filter(
            ShippingModel.shipping_point==factory,
            CategoryModel.name==category[0]
        ).one()[0]
