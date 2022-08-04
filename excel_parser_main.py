import os
import pickle
import openpyxl
from openpyxl import load_workbook
from collections import defaultdict
from loguru import logger


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded on the fly"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self) -> str:
        return repr(dict(self))


class ExcelParser:

    def __init__(self, src, dst):
        """"""
        self.src = src
        self.dst = dst
        self.wb = None
        self.sheet = None
        self.sheets_store = NestedDefaultDict()
        self.template = NestedDefaultDict({
            'roi': None,
            'peak_strain_radial_%': None,
            'peak_strain_circumf_%': None,
            'time_to_peak_radial_ms': None,
            'time_to_peak_circumf_ms': None,
        })
        os.makedirs(self.dst, exist_ok=True)

    def __call__(self):
        """"""
        for _ in self.loop_files():
            for _ in self.loop_sheets():
                self.loop_row()

    def load_file(self, file, extension='pkl'):
        """"""
        logger.info(f'Search -> files -> {self.src}')
        if file.endswith(extension) and not file.startswith('.'):
            file_path = os.path.join(self.src, file)
            logger.info(file_path)
            if extension == 'pkl':
                with open(file_path, 'rb') as file_object:
                    return pickle.load(file_object)
            return load_workbook(file_path,
                                 read_only=False,
                                 data_only=True,
                                 keep_vba=False,
                                 keep_links=False)

    def extract_sheets_as_xlsx(self):
        """"""
        # print(os.listdir(self.src))
        # for file in os.listdir(self.src):
        file = self.src
        wb = self.load_file(file, 'xlsx')
        for sheet_name in wb.sheetnames:
            if '_' in sheet_name or '2 ' in sheet_name:
                if '#' not in sheet_name:
                    logger.info(f'Extract -> {sheet_name}')
                    extracted_sheet = wb[sheet_name]
                    new_wb = openpyxl.Workbook()
                    single_sheet = new_wb.active
                    if '_' in sheet_name:
                        new_sheet_name = sheet_name.split('_')[1]
                    else:
                        new_sheet_name = sheet_name[2:]
                    single_sheet.title = new_sheet_name
                    for row in extracted_sheet:
                        for cell in row:
                            single_sheet[cell.coordinate].value = cell.value
                    new_wb.save(f'{os.path.join(self.dst, new_sheet_name)}.xlsx')
                    new_wb.close()
                    del new_wb
                    del single_sheet
        del wb


    def read_and_pickle(self):
        """"""
        for file_path in self.loop_files('xlsx'):
            pickle_file = os.path.join(self.src, file_path.replace('xlsx', 'pkl'))
            logger.info(pickle_file)
            for sheet_name in self.wb.sheetnames:
                if '_' not in sheet_name or '#' in sheet_name:
                    del self.wb[sheet_name]
            with open(pickle_file, 'wb') as file_object:
                pickle.dump(self.wb, file_object)


    def loop_sheets(self):
        """"""
        for sheet_name in self.wb.sheetnames:
            logger.info(f'sheet -> {sheet_name}')
            self.sheet = self.wb[sheet_name]
            yield


    def loop_row(self):
        """"""
        # print(self.sheet.cell(row=1, column=2))
        # for i in range(1, self.sheet.nrows-1):
        #     logger.info(self.sheet.cell_value(0, i))
        max_rows = self.sheet.max_row
        max_columns = self.sheet.max_column
        q = []
        for row_index in range(1, max_rows - 1):
            q.append(self.sheet.cell(row=row_index, column=2).value)

        logger.info(q)

        # x = self.sheet.cell(row=(0, max_rows), column=2)
        # print(x)

        # for row_index in range(max_rows):
        #     if row_index > 200:
        #         if self.sheet.cell(row=row_index, column=2).value:

        # if isinstance(self.sheet.cell(row=row_index, column=2).value, str):
        # if 'Ventricle' in self.sheet.cell(row=row_index, column=2).value:
        #     print(f'Left ventricle -> {self.sheet.cell(row=row_index, column=3).value}')
        # if sheet.cell(row=row_index, column=1).value:
        #     print(sheet.cell(row=row_index, column=1).value)
        # if sheet.cell(row=row_index, column=0).value == name:
        #     print(row_index)


if __name__ == '__main__':
    import time

    x = time.time()


    file = 'h. Myocarditis_strain_Anselm#4.xlsx'

    ep = ExcelParser(
        src=f'/home/melandur/Data/Myocarditis/CSV/{file}',
        dst='/home/melandur/Data/Myocarditis/clean_csv')

    # ep.read_and_pickle()
    ep.extract_sheets_as_xlsx()
    # ep()
    logger.info((time.time() - x))
