from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, swagger_config
from flasgger import Swagger
from app.utils.db_utils import load_preset_regions
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import List



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app, config=swagger_config)

from app import routes

# ! это временное решение (видимо сломало миграции) потом убрать
# пока в данных не указаны регионы можно в принципе так же для прототипа сделать с 
# таблицей пунктов отгрузок (т е прописать им вручную регионы и области)
with app.app_context():
    db.create_all()
    from app.models.region import RegionModel
    regions = load_preset_regions()
    session = db.session
    
    for name, code in regions.items():
        if session.query(RegionModel).filter(RegionModel.code == code).scalar():
            continue

        session.add(RegionModel(
            name = name,
            code = code
        ))
        
    session.commit()
    session.close()


