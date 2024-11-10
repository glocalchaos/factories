from app import db
from typing import Iterable
from ..entities.models import CategoryModel

class CategoryRepository:
    def upload_categories(self, categories: Iterable[str]):
        session = db.session

        for category_name in categories:
            if not self.exists_by_name(category_name):
                session.add(CategoryModel(
                    name = category_name,
                ))
            
        session.commit()
        session.close()


    def upload_category(self, category_name: str):
        session = db.session
        if self.exists_by_name(category_name):
            return

        session.add(CategoryModel(
            name = category_name,
        ))

        session.commit()
        session.close()
    
    def get_by_name(self, name: str) -> CategoryModel:
        session = db.session
        category = session.query(CategoryModel).filter(CategoryModel.name == name).scalar()
        return category
    
    def get_by_id(self, id: int) -> CategoryModel:
        return db.session.query(
            CategoryModel
        ).filter(
            CategoryModel.id == id
        ).scalar()
    
    def exists_by_id(self, id: int) -> bool:
        return self.get_by_id(id) is not None
    
    def exists_by_name(self, name: str) -> bool:
        return self.get_by_name(name) is not None


    