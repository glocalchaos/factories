from app import app
from app import db
from os import path
from flask import request, redirect, url_for, jsonify
from .service.shipping_repository import ShippingRepository
from .service.product_repository import ProductRepository
from .service.factory_repository import FactoryRepository
from .service.region_repository import RegionRepository

import os
from pathlib import Path

from . import excel_parser

def get_db_session():
    session = session
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()

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

    product_categories = parser.parse_products_categories()
    for product_name, category_name in product_categories.items():
        ProductRepository().upload_product(product_name, category_name)

    parsed_data = parser.parse_all()
    for record in parsed_data:
        ShippingRepository().upload_shipping(record, cur_datetime)

    os.remove(file_path)

    return redirect(url_for('index'), code=200)

# ! TODO Swagger

# ! TODO фильтрация по дате
@app.route('/factoriesByRegions', methods=['GET'])
def get_regions():
    regions = RegionRepository.get_all_regions()
    result = []

    for region in regions:
        factories = []
        for factory in RegionRepository.get_shipping_points_by_region(region):
            transports = []
            for transport in FactoryRepository.get_used_transports(factory):
                transports.append({
                    "name": transport.name,
                    "monthly_plan": ShippingRepository().monthly_plan_by_factory_and_transport(factory, transport)
                })

            product_categories = []
            for category in FactoryRepository.get_product_categories(factory):
                product_categories.append({
                    "name": category.name,
                    "monthly_plan": ShippingRepository().monthly_plan_by_factory_and_category(factory, category)
                })
            factory_info = {
                "name": factory.name,
                "monthly_plan": ShippingRepository().monthly_plan_by_factory(factory),
                "transport_types": transports,
                "product_categories": product_categories
            }
            factories.append(factory_info)

        result.append({
            'region': region.name,
            "code": region.code,
            'factories': factories
        })

    return jsonify(result)
