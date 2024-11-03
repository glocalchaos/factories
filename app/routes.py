from app import app
from app import db
from os import path
from flask import request, redirect, url_for, Response
from .service.shipping_repository import ShippingRepository
from .service.product_repository import ProductRepository
from .service.factory_repository import FactoryRepository
import os
from pathlib import Path

from . import excel_parser


@app.route('/')
@app.route('/index')
def index():
    return "Hello world"


@app.route('/uploadXlsData', methods=['POST'])
def upload_file():
    """Upload .xls file to database
    ---
    parameters:
        - name: file
          required: true
          in: formData
          type: file

    responses:
        200:
            description: Data from file fully uploaded
        400:
            description: File not provided
    """
    xls_file = request.files['file']
    if xls_file.filename == '':
        return redirect(url_for('index'), code=400)

    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

    file_path = path.join(app.config['UPLOAD_FOLDER'], xls_file.filename)
    xls_file.save(file_path)

    parser = excel_parser.Parser(file_path)

    cur_datetime = parser.get_datetime()

    # agent_points_dict = parser.parse_factories()
    # FactoryRepository().upload_factories(agent_points_dict)

    product_categories = parser.parse_products_categories()
    for product_name, category_name in product_categories.items():
        ProductRepository().upload_product(product_name, category_name)

    parsed_data = parser.parse_all()
    for record in parsed_data:
        ShippingRepository().upload_shipping(record, cur_datetime)

    os.remove(file_path)

    return redirect(url_for('index'), code=200)
