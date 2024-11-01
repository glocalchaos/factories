from app import db
from typing import Mapping, Iterable
from ..models.product import ProductModel
from .category_repository import CategoryRepository

class ProductRepository:
    def upload_product(self, product_name: str, product_category_name: str):
        session = db.session 
        if session.query(ProductModel).filter(ProductModel.name == product_name).scalar():
            return

        CategoryRepository().upload_category(category_name=product_category_name)

        
        session.add(ProductModel(
            name = product_name,
            category_id = CategoryRepository().get_category_id_by_name(product_category_name)
        ))
            
        session.commit()
        session.close()
        
    def get_id_by_name(self, name: str) -> int:
        session = db.session
        product = session.query(ProductModel).filter(ProductModel.name == name).scalar()
        return product.id