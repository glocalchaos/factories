from app import db
from typing import Iterable
from ..entities.models import CategoryModel

#   TODO catch ERRORS где надо

class CategoryRepository:
    def upload_categories(self, categories: Iterable[str]):
        session = db.session
    
        # TODO сделать не по корявому
        for category_name in categories:
            if session.query(CategoryModel).filter(CategoryModel.name == category_name).scalar():
                continue

            session.add(CategoryModel(
                name = category_name,
            ))
            
        session.commit()
        session.close()


    def upload_category(self, category_name: str):
        session = db.session
        if session.query(CategoryModel).filter(CategoryModel.name == category_name).scalar():
            return

        session.add(CategoryModel(
            name = category_name,
        ))
        session.commit()
        session.close()
    
    def get_category_id_by_name(self, category_name: str) -> int:
        session = db.session
        category = session.query(CategoryModel).filter(CategoryModel.name == category_name).scalar()
        return category.id


    