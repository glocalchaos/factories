import openpyxl as pxl
from .utils.parser_utils import set_date
from .models.transport import TransportModel


# TODO тримить строки блин
class Parser:
    def __init__(self, workbook_path='/home/GFKAA3/Projects/factories/src/data.xlsx', placeholder_factory_name='НЕИЗВЕСТЕН'):
        self.workbook = pxl.load_workbook(workbook_path, data_only=True)
        self.placeholder_factory_name = placeholder_factory_name

    # TODO парсь всё, выдавай туда мап
    def parse_transport(self):
        data_sheet = self.workbook['Данные']
        transport_list = set()
        product_list = set()
        product_category_list = set()
        for row in data_sheet.iter_rows(min_row=7, min_col=3, max_row=92, max_col=11):

            cell_shipping_point, cell_product, cell_product_category, cell_transport, cell_monthly_plan, cell_shipping_plan, cell_shipping_done, _, cell_notes = row
            transport_list.add(cell_transport.value.lower())
            product_category_list.add(cell_product_category.value.lower())
            product_list.add(cell_product.value.lower())

        return transport_list, product_category_list, product_list


    def parse_factories(self):
        data_sheet = self.workbook['Отчет']
        agent_points_dict = {}
        cur_agent_name = data_sheet[6][1].value
        for row in data_sheet.iter_rows(min_row=6, max_row=121, min_col=2, max_col=3):
            if row[0].value is not None:
                cur_agent_name = row[0].value
                agent_points_dict[cur_agent_name] = []
            if row[1].value is None:
                continue
            agent_points_dict[cur_agent_name].append(row[1].value)
        return agent_points_dict
        

            