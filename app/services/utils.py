from typing import List
from app.entities.models import ProductModel, ShippingModel, TransportModel
from sqlalchemy.orm import Query

def apply_shippings_transport_filter(q: Query, transport_types: List[TransportModel]) -> Query:
    if (transport_types is None or len(transport_types) == 0 
            or (len(transport_types) == 1 and transport_types[0] is None)): # TODO не могу найти где там ошибка блин
        return q
    # print("hhh", transport_types)
    return q.filter(ShippingModel.transport_id.in_(t.id for t in transport_types))

def apply_shippings_product_filter(q: Query, products: List[ProductModel]) -> Query:
    if products is None or len(products) == 0:
        return q
    return q.filter(ShippingModel.product_id.in_(p.id for p in products))