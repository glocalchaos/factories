from flask import Flask, g, request, session
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, swagger_config
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from app.utils.db_utils import upload_regions
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import List
from .config import Config
from .database import user_sessions, create_db_session, cache



app = Flask(__name__)
app.config.from_object(Config)
app.json.sort_keys = False
# factoriesDB = SQLAlchemy(app)
ma = Marshmallow(app)

swagger = Swagger(app, config=swagger_config)

