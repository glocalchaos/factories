from app import app
from app import db
from os import path
from flask import request, redirect, url_for
from .service.transport_repository import TransportRepository

# from flask_api import status
from . import excel_parser

@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

@app.route('/uploadTransport', methods=['POST'])
def upload_file():
    csv_file = request.files['file']
    if csv_file.filename == '':
        return redirect(url_for('index'), code=400)
    file_path = path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
    csv_file.save(file_path)
    parser = excel_parser.Parser(file_path)
    transport_names_set = parser.parseTransport()
    # session = db.session
    # session.add_all(transport_set)
    # session.commit()
    # session.close()
    app.logger.info(transport_names_set)
    TransportRepository().upload_transport(transport_names_set)

    return redirect(url_for('index'), code=200)