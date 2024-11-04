import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5431'
    UPLOAD_FOLDER = 'src/'
    JSON_AS_ASCII = False
    # JSON_SORT_KEYS = False # ! removed in flask 2.3


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
