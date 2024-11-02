from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, swagger_config
from flasgger import Swagger
from app.utils.db_utils import load_preset_regions
# from app.models.factory import FactoryModel
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import List



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
swagger = Swagger(app, config=swagger_config)

from app import routes
# from app.models import region, product, category, factory, transport, shipping
# from app.models.region import RegionModel
# from app.models.product import ProductModel
# from app.models.category import CategoryModel
# from app.models.factory import FactoryModel
# from app.models.transport import TransportModel
# from app.models.shipping import ShippingModel





# @app.cli.command("seed-db")
# def seed_db():
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


