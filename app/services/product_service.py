from typing import List
from app.entities.models import CategoryModel, ProductModel
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_repository = CategoryRepository()

    def upload_product(self, product_name: str, product_category_name: str):
        if self.repository.exists_by_name(product_name):
            return
        self.category_repository.upload_category(product_category_name)
        product_category_id = self.category_repository.get_by_name(product_category_name).id

        self.product_repository.upload_product(product_name, product_category_id)

        

    def upload_products(self):
        # TODO
        pass

    def get_product_by_name(self):
        # TODO
        pass

    def get_products_by_category_name(self, category_name: str) -> List[ProductModel]:
        category = self.get_category_by_name(category_name)
        return self.product_repository.get_by_category_id(category.id)
    
    def get_products_by_category(self, category: CategoryModel) -> List[ProductModel]:
        return self.product_repository.get_by_category(category)
    
    def get_product_ids_by_category_name(self, category_name: str) -> List[int]:
        category = self.get_category_by_name(category_name)
        return self.product_repository.get_ids_by_category_id(category.id)
    

    def get_category_by_name(self, name: str) -> CategoryModel:
        return self.category_repository.get_by_name(name)
