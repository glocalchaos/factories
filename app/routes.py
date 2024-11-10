from app import app
from app import db
from os import path
from app.services.factory_service import FactoryService
from app.services.product_service import ProductService
from flasgger import swag_from
from flask import request, redirect, url_for, jsonify, request, abort
from .repositories.shipping_repository import ShippingRepository
from .repositories.product_repository import ProductRepository
from .entities.models import FactoryModel
from .entities.schemas import PlanVsFactSchema, planfact_schema, planfact_schemas, factory_schema, transport_schema
from .utils import query_utils
import os
from pathlib import Path

from . import excel_parser

# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello world"

factory_service = FactoryService()
product_service = ProductService()
@app.route('/uploadXlsData', methods=['POST'])
@swag_from('swagger/upload_xls.yaml')
def upload_file():
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

'''
# ! TODO фильтрация по дате
@app.route('/factoriesByRegions/', methods=['GET'])
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
'''

@app.route('/factories/get_all/', methods=['GET'])
@swag_from('swagger/factories_get_all.yaml')
def get_all():
    pass

@app.route('/factories/<string:factory_name>/')
@swag_from('swagger/factory.yaml')
def factory(factory_name):
    factory = factory_service.get_by_name(factory_name)
    if factory is None:
        abort(404, description="Пункт отгрузки не найден")
    from_date, to_date = query_utils.get_sum_period(request.args)
    transport_type_name = query_utils.get_transport_type(request.args)
    product_category_name = query_utils.get_product_category(request.args)

    products = None
    transport = None
    if product_category_name is not None:
        products = product_service.get_products_by_category_name(product_category_name)
    if transport_type_name is not None:
        transport = [factory_service.get_transport_by_name(transport_type_name)]

    try:
        daily_data = planfact_schema.load({"plan": factory_service.daily_plan(factory, 
                                                                              to_date, 
                                                                              transport, 
                                                                              products), 
                                            "fact": factory_service.daily_fact(factory, 
                                                                               to_date, 
                                                                               transport, 
                                                                               products)})
        sum_data = planfact_schema.load({"plan": factory_service.sum_plan(factory, to_date, transport, products), 
                                         "fact": factory_service.sum_fact(factory, from_date, to_date, transport, products)})
    except Exception as e:
        abort(404, "Поставки не найдены")

    return factory_schema.dump({"factory_name": factory_name, "daily": daily_data, "sum": sum_data})


@app.route('/factories/<factory_name>/transport/')
@swag_from('swagger/factory_transport.yaml')
def factory_transport(factory_name):    
    factory = factory_service.get_by_name(factory_name)
    if factory is None:
        abort(404, description="Пункт отгрузки не найден")
    
    from_date, to_date = query_utils.get_period(request.args)
    transport_type = query_utils.get_transport_type(request.args)
    product_category_name = query_utils.get_product_category(request.args)

    products = None
    transport = None
    if product_category_name is not None:
        try:
            products = product_service.get_products_by_category_name(product_category_name)    
        except Exception:
            abort(404, description="Отгрузки с данной категорией не найдены")
    if transport_type is not None:
        transport = [factory_service.get_transport_by_name(transport_type)]
    used_transport = factory_service.get_used_transports_by_factory(factory, 
                                                                   from_date, 
                                                                   to_date, 
                                                                   transport,
                                                                   products)

    if len(used_transport) == 0:
        abort(404, description="Поставки не найдены")

    transport_details = []
    for transport in used_transport:
        try:
            transport_details.append(PlanVsFactSchema().load({
                "transport_type": transport.name,
                "plan": factory_service.sum_plan(factory, 
                                                 from_date, 
                                                 [transport], 
                                                 products),
                "fact": factory_service.sum_fact(factory,
                                                 from_date,
                                                 to_date,
                                                 [transport],
                                                 products)
            }))
        except Exception as e:
            print("exc", e)
            continue
    # Не надо??
    if len(transport_details) == 0:
        abort(404, description="Поставки не найдены.")

    
    return transport_schema.dump({"factory_name": factory_name,
                                  "transports": transport_details})

@app.route('/factories/<factory_name>/product_category/')
@swag_from('swagger/factory_product_category.yaml')
def factory_product_category(factory_name):
    # ! TODO fix не работает фильтрация по транспорту!!!!!!
    factory = factory_service.get_by_name(factory_name)
    if factory is None:
        abort(404, description="Пункт отгрузки не найден")

    from_date, to_date = query_utils.get_period(request.args)
    transport_type = query_utils.get_transport_type(request.args)
    product_category_name = query_utils.get_product_category(request.args)

    products = None
    transport = None
    if product_category_name is not None:
        try:
            products = product_service.get_products_by_category_name(product_category_name)    
        except Exception:
            abort(404, description="Отгрузки с данной категорией не найдены")

    if transport_type is not None:
        transport = [factory_service.get_transport_by_name(transport_type)]

    shipped_categories = factory_service.get_shipped_categories_by_factory(factory, 
                                                                   from_date, 
                                                                   to_date, 
                                                                   transport,
                                                                   products)

    if len(shipped_categories) == 0:
        abort(404, description="Поставки не найдены")

    
    category_details = []
    for category in shipped_categories:
        try:
            products = product_service.get_products_by_category(category)
            # print(category.name, products) 
            category_details.append(PlanVsFactSchema().load({
                "product_category":  category.name,
                "plan": factory_service.sum_plan(factory, 
                                                 from_date, 
                                                 [transport], 
                                                 products),
                "fact": factory_service.sum_fact(factory,
                                                 from_date,
                                                 to_date,
                                                 [transport],
                                                 products)
            }))
        except Exception as e:
            print("exc", e.__traceback__.tb_lineno, e.__traceback__.tb_next.tb_next.tb_lineno)
            continue
    # Не надо??
    if len(category_details) == 0:
        abort(404, description="Поставки не найдены.")

    
    return transport_schema.dump({"factory_name": factory_name,
                                  "transports": category_details})