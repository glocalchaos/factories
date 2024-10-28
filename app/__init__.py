from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
#from app import models

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#db.init_app(app)
migrate = Migrate(app, db)

from app import routes
from app.models import agent, product, category, factory, transport, shipping