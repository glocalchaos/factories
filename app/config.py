import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5431'
    CACHE_TYPE = 'simple'  # You can choose other types like 'redis', 'memcached', etc.
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds
    UPLOAD_FOLDER = 'src/' # '/opt/foresight/cabinet_back/uploads'
    JSON_AS_ASCII = False
    ALLOWED_EXTENSIONS = {'xlsx'}
    DATABASE_MODE = 'DIRECT' # DIRECT OR DOMAIN depending on authentithication mode
    SERVERBASE_MODE = 'PYTHON' # PYTHON OR WSGI depending on server environment
    DATABASE = '@kao-qas-db01.codm.gazprom.loc'
    PORT = '5433'


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'factories_apispec',
            "route": '/factories_apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/swagger/"
}
