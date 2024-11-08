from openpyxl import workbook, worksheet
from openpyxl.cell.cell import Cell
import datetime
from flask_sqlalchemy import SQLAlchemy


# TODO Hardcode!!
def get_date(sheet: worksheet.worksheet):
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

        self.shipping_point : str = cell_shipping_point
        self.product : str = cell_product
        self.product_category : str = cell_product_category
        self.transport : str  = cell_transport
        self.monthly_plan : float  = cell_monthly_plan
        self.shipping_plan : float  = cell_shipping_plan
        self.shipping_done : float  = cell_shipping_done
        self.notes : str  = cell_notes

    @property
    def shipping_point(self) -> str:
        return self._shipping_point
    
    @shipping_point.setter
    def shipping_point(self, cell: Cell):
        self._shipping_point = cell.value.strip()

    
    @property
    def product(self) -> str:
        return self._product
    
    @product.setter
    def product(self, cell: Cell):
        self._product = cell.value.strip()
    
    @property
    def product_category(self) -> str:
        return self._product_category

    @product_category.setter
    def product_category(self, cell: Cell):
        self._product_category = cell.value.strip()

    @property
    def transport(self) -> str:
        return self._transport
    
    @transport.setter
    def transport(self, cell: Cell):
        self._transport = cell.value.lower().strip() 

    @property
    def monthly_plan(self) -> float:
        return self._monthly_plan
    
    @monthly_plan.setter
    def monthly_plan(self, cell: Cell):
        self._monthly_plan = cell_to_float(cell)
        
    @property
    def shipping_plan(self) -> float:
        return self._shipping_plan
            
    @shipping_plan.setter
    def shipping_plan(self, cell: Cell):
        self._shipping_plan = cell_to_float(cell)

    @property
    def shipping_done(self) -> float:
        return self._shipping_done
            
    @shipping_plan.setter
    def shipping_done(self, cell: Cell):
        self._shipping_done = cell_to_float(cell)
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @notes.setter
    def notes(self, cell: Cell):
        self._notes = cell.value



def cell_to_float(cell: Cell) -> float:
    if cell.value is None:
        return None
    try:
        value = float(cell.value)
    except ValueError:
        raise NumberNeededInCell(cell)
    except Exception as ex:
        raise ex
    return value


class NumberNeededInCell(Exception):
    def __init__(self, cell: Cell):
        super.__init__(self, "Tried to parse number from cell {}".format(cell.coordinate))
