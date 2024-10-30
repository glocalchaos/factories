import openpyxl as pxl
import datetime
from flask_sqlalchemy import SQLAlchemy

def set_date(sheet: pxl.worksheet.worksheet):
    year = int(sheet['C1'].value)
    month = int(sheet['C3'].value)
    day = int(sheet['C4'].value)
    return datetime.datetime(year, month, day)