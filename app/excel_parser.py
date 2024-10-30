import openpyxl as pxl
from .utils.parser_utils import set_date
from .models.transport import TransportModel

class Parser:
    def __init__(self, workbook_path='/home/GFKAA3/Projects/factories/src/data.xlsx'):
        self.workbook = pxl.load_workbook(workbook_path, data_only=True)

    def parseTransport(self):
        data_sheet = self.workbook['Данные']
        date = set_date(data_sheet)
        transport_list = set()
        for row in data_sheet.iter_rows(min_row=7, min_col=3, max_row=92, max_col=11):

            cell_shipping_point, cell_product, cell_product_category, cell_transport, cell_monthly_plan, cell_shipping_plan, cell_shipping_done, _, cell_notes = row
            transport_list.add(cell_transport.value.lower())
        transport_models = []
        for item in transport_list:
            model_transport = TransportModel(
                name = item
            )
            transport_models.append(model_transport)
        return transport_models

            