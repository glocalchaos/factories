from app import db
from ..utils.parser_utils import ShippingRecordType
from collections import namedtuple
from datetime import datetime
from .product_repository import ProductRepository
from ..models.shipping import ShippingModel
from .transport_repository import TransportRepository
from .factory_repository import FactoryRepository



# ShippingTuple = namedtuple('ShippingTuple', 'factory product category transport monthly_plan ship_plan ship_done note')

class ShippingRepository:
    def __init__(self):
        self._product_repo = ProductRepository()
        self._transport_repo = TransportRepository()
        self._factory_repo = FactoryRepository()

    def upload_shipping(self, shippingRecord : ShippingRecordType, cur_datetime: datetime):
        self._product_repo.upload_product(shippingRecord.product, shippingRecord.product_category) # TODO catch errors
        self._transport_repo.upload_transport(shippingRecord.transport)
        session = db.session

        #########
        # print(shippingRecord.monthly_plan, shippingRecord.shipping_plan, shippingRecord.shipping_done)
        #########
        factory_id = self._factory_repo.get_id_by_name(shippingRecord.shipping_point)
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

