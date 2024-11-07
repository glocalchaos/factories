from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, swagger_config
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from app.utils.db_utils import upload_regions
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import List



app = Flask(__name__)
app.config.from_object(Config)
app.json.sort_keys = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
swagger = Swagger(app, config=swagger_config)

from app import routes

# ! это временное решение (видимо сломало миграции) потом убрать
# ! пока в данных не указаны регионы можно в принципе так же для прототипа сделать с 
# ! таблицей пунктов отгрузок (т е прописать им вручную регионы и области)
with app.app_context():
    db.create_all()
    upload_regions(db)


