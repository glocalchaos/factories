import openpyxl as pxl
import datetime
from flask_sqlalchemy import SQLAlchemy
# months = map()

def set_date(sheet: pxl.worksheet.worksheet):
    year = int(sheet['C1'].value)
    month = int(sheet['C3'].value)
    day = int(sheet['C4'].value)
    return datetime.datetime(year, month, day)


def load_shippings(sheet: pxl.worksheet.worksheet):
    for row in sheet.iter_rows(min_row=7, min_col=3, max_row=92, max_col=10):
        shipping_point, product, product_category, transport, monthly_plan, shipping_plan, shipping_done, _, notes = row
        print(shipping_point, product, product_category, transport, monthly_plan, shipping_plan, shipping_done, notes)

def read_shipping(df):
    pass