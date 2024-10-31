from openpyxl import workbook, worksheet
from openpyxl.cell.cell import Cell
import datetime
from flask_sqlalchemy import SQLAlchemy


# TODO Hardcode!!
def set_date(sheet: worksheet.worksheet):
    year = int(sheet['C1'].value)
    month = int(sheet['C3'].value)
    day = int(sheet['C4'].value)
    return datetime.datetime(year, month, day)


class ShippingRecordType:
    def __init__(self, cell_shipping_point: Cell, 
                 cell_product: Cell, 
                 cell_product_category: Cell, 
                 cell_transport: Cell, 
                 cell_monthly_plan: Cell, 
                 cell_shipping_plan: Cell, 
                 cell_shipping_done: Cell, 
                 cell_notes: Cell):
        self._shipping_point = cell_shipping_point
        self._product = cell_product
        self._product_category = cell_product_category
        self._transport = cell_transport
        self._monthly_plan = cell_monthly_plan
        self._shipping_plan = cell_shipping_plan
        self._shipping_done = cell_shipping_done
        self._notes = cell_notes

    @property
    def shipping_point(self) -> str:
        return self._shipping_point
    
    @shipping_point.setter
    def shipping_point(self, cell: Cell):
        self._shipping_point = cell.value.trim()

    
    @property
    def product(self) -> str:
        return self._product
    
    @product.setter
    def product(self, cell: Cell):
        self._product = cell.value.lower().trim()
    
    @property
    def product_category(self) -> str:
        return self._product_category

    @product_category.setter
    def product_category(self, cell: Cell):
        self._product_category = cell.value.lower().trim()

    @property
    def transport(self) -> str:
        return self._transport
    
    @transport.setter
    def transport(self, cell: Cell):
        self._transport = cell.value.lower().trim() 

    @property
    def monthly_plan(self) -> int:
        return self._monthly_plan
    
    @monthly_plan.setter
    def monthly_plan(self, cell: Cell):
        self._monthly_plan = cell_to_int(cell)
        
    @property
    def shipping_plan(self) -> int:
        return self._shipping_plan
            
    @shipping_plan.setter
    def shipping_plan(self, cell: Cell):
        self._shipping_plan = cell_to_int(cell)

    @property
    def shipping_done(self) -> int:
        return self._shipping_done
            
    @shipping_plan.setter
    def shipping_done(self, cell: Cell):
        self._shipping_done = cell_to_int(cell)
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @shipping_point.setter
    def notes(self, cell: Cell):
        self._notes = cell.value



def cell_to_int(cell: Cell) -> int:
    try:
        value = int(cell.value)
    except ValueError:
            raise NumberNeededInCell(cell)
    except Exception as ex:
        raise ex


class NumberNeededInCell(Exception):
    def __init__(self, cell: Cell):
        super.__init__(self, "Tried to parse number from cell {}".format(cell.coordinate))