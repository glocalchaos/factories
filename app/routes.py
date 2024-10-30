from app import app
from app import db
from os import path
from flask import request, redirect, url_for
from .service.transport_repository import TransportRepository
from .service.factory_repository import FactoryRepository

# from flask_api import status
from . import excel_parser

@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

@app.route('/uploadTransport', methods=['POST'])
def upload_file():
    xls_file = request.files['file']
    if xls_file.filename == '':
        return redirect(url_for('index'), code=400)
    file_path = path.join(app.config['UPLOAD_FOLDER'], xls_file.filename)
    xls_file.save(file_path)
    parser = excel_parser.Parser(file_path)
    transport_names_set, _, _ = parser.parseTransport()
    TransportRepository().upload_transport(transport_names_set)

    agent_points_dict = parser.parseFactories()
    FactoryRepository().upload_factories(agent_points_dict)

    return redirect(url_for('index'), code=200)