from app import db
from typing import List, Mapping, Iterable
from ..entities.models import CategoryModel, ProductModel

class ProductRepository:
    def upload_product(self, product_name: str, product_category_id: int):
        if self.exists_by_name(product_name):
            return
        
        session = db.session

        session.add(ProductModel(
            name=product_name,
            product_category_id=product_category_id,
        ))
            
        session.commit()
        session.close()
        
    def get_by_name(self, name: str) -> ProductModel:
        session = db.session
        product = session.query(ProductModel).filter(ProductModel.name == name).scalar()
        return product
    
    def get_by_id(self, id: int) -> ProductModel:
        return db.session.query(
            ProductModel
        ).filter(
            ProductModel.id == id
        ).scalar()
    
    def exists_by_id(self, id: int) -> bool:
        return self.get_by_id(id) is not None

    def exists_by_name(self, name: str) -> bool:
        return self.get_by_name(name) is not None
    
    def get_by_category_id(self, category_id: int) -> List[ProductModel]:
        return db.session.query(
            ProductModel
            ).filter(
                ProductModel.category_id == category_id
            ).all()
    
    def get_by_category(self, category: CategoryModel) -> List[ProductModel]:
        return db.session.query(
            ProductModel
            ).filter(
                ProductModel.category == category
            ).all()
    
    def get_ids_by_category_id(self, category_id: int) -> List[int]:
        return db.session.query(
            ProductModel.id
            ).filter(
                ProductModel.category_id == category_id
            ).all()