import json
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
        self.mode = None
        self.sheet = None
        self.data_name = None
        self.subject_name = None
        self.template = NestedDefaultDict({
            'roi': None,
            'peak_strain_radial_%': None,
            'peak_strain_circumf_%': None,
            'time_to_peak_radial_ms': None,
            'time_to_peak_circumf_ms': None,
        })
        self.subject = NestedDefaultDict()
        os.makedirs(self.dst, exist_ok=True)

    def __call__(self):
        """"""
        for _ in self.loop_files():
            self.get_meta()
            for row in self.loop_row():
                # logger.info(row)
                self.extract_name(row)
                self.extract_data(row)
            logger.info(self.count)

    def load_file(self, file, extension='pkl'):
        """"""
        if file.endswith(extension) and not file.startswith('.'):
            file_path = os.path.join(self.src, file)
            if extension == 'pkl':
                with open(file_path, 'rb') as file_object:
                    return pickle.load(file_object)
            self.subject_name = file.strip('.xlsx')
            return load_workbook(file_path,
                                 read_only=False,
                                 data_only=True,
                                 keep_vba=False,
                                 keep_links=False)

    # def extract_sheets_as_xlsx(self):
    #     """"""
    #     # print(os.listdir(self.src))
    #     # for file in os.listdir(self.src):
    #     file = self.src
    #     wb = self.load_file(file, 'xlsx')
    #     for sheet_name in wb.sheetnames:
    #         if '_' in sheet_name or '2 ' in sheet_name:
    #             if '#' not in sheet_name:
    #                 logger.info(f'Extract -> {sheet_name}')
    #                 extracted_sheet = wb[sheet_name]
    #                 new_wb = openpyxl.Workbook()
    #                 single_sheet = new_wb.active
    #                 if '_' in sheet_name:
    #                     new_sheet_name = sheet_name.split('_')[1]
    #                 else:
    #                     new_sheet_name = sheet_name[2:]
    #                 single_sheet.title = new_sheet_name
    #                 for row in extracted_sheet:
    #                     for cell in row:
    #                         single_sheet[cell.coordinate].value = cell.value
    #                 new_wb.save(f'{os.path.join(self.dst, new_sheet_name)}.xlsx')
    #                 new_wb.close()
    #                 del new_wb
    #                 del single_sheet
    #     del wb

    # def read_and_pickle(self):
    #     """"""
    #     for file_path in self.loop_files('xlsx'):
    #         pickle_file = os.path.join(self.src, file_path.replace('xlsx', 'pkl'))
    #         logger.info(pickle_file)
    #         for sheet_name in self.wb.sheetnames:
    #             if '_' not in sheet_name or '#' in sheet_name:
    #                 del self.wb[sheet_name]
    #         with open(pickle_file, 'wb') as file_object:
    #             pickle.dump(self.wb, file_object)

    def loop_files(self):
        """Iterate over files"""
        for file in os.listdir(self.src):
            logger.info(f'File -> {file}')
            self.wb = self.load_file(file, extension='xlsx')
            sheet_names = self.wb.sheetnames
            self.sheet = self.wb[sheet_names[0]]
            yield

    def loop_row(self):
        """"""
        # print(self.sheet.cell(row=1, column=2))
        # for i in range(1, self.sheet.nrows-1):
        #     logger.info(self.sheet.cell_value(0, i))
        start_row = 229
        max_rows = self.sheet.max_row
        max_columns = self.sheet.max_column
        self.count = 0
        for row_index in range(start_row, max_rows - 1):
            if 'left' in f'{self.sheet.cell(row=row_index, column=2).value}'.lower():
                yield row_index
            # q[0].append(self.sheet.cell(row=row_index, column=2).value)
            # q[1].append(self.sheet.cell(row=row_index, column=3).value)

        # logger.info(q[1])

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

    def get_meta(self):
        self.subject[self.subject_name] = NestedDefaultDict()
        self.subject[self.subject_name]['meta']['study_date'] = self.sheet.cell(row=212, column=3).value
        self.subject[self.subject_name]['meta']['modality'] = self.sheet.cell(row=219, column=3).value
        self.subject[self.subject_name]['meta']['sequence_name'] = self.sheet.cell(row=223, column=3).value
        self.subject[self.subject_name]['meta']['protocol_name'] = self.sheet.cell(row=224, column=3).value

    def extract_name(self, row):
        data_name = f'{self.sheet.cell(row=row, column=2).value}{self.sheet.cell(row=row, column=3).value}'
        data_name_split = data_name.split('-')

        if len(data_name_split) == 3:
            if '2D' in data_name_split[1]:
                sub_name_1 = data_name_split[1].replace('Results', '').strip()
                sub_name_1 = sub_name_1.replace(' ', '_').lower()
                sub_name_2 = data_name_split[2].replace('None', '').strip()
                sub_name_2 = sub_name_2.replace(' ', '_').lower()
                if 'AHA Diagram Data' in data_name_split[0]:
                    self.count += 1
                    self.data_name = f'AHA_{sub_name_1}_{sub_name_2}'
                    self.mode = 'aha_diagram'
                elif 'Global and ROI Diagram Data' in data_name_split[0]:
                    self.count += 1
                    self.data_name = f'Global_ROI_{sub_name_1}_{sub_name_2}'
                    self.mode = 'global_roi'
                else:
                    self.data_name = None
                    self.mode = None
        elif len(data_name_split) == 2:
            sub_name_1 = data_name_split[1].replace('Results', '').strip()
            sub_name_1 = sub_name_1.replace(' ', '_').lower()
            if '2D' in data_name_split[1]:
                if 'ROI Polarmap Data' in data_name_split[0] or 'ROI Polarmap Data' in data_name_split[1]:
                    self.count += 1
                    self.data_name = f'ROI_Polarmap_{sub_name_1}'
                    self.mode = 'roi_polarmap'
                elif 'AHA Polarmap Data' in data_name_split[0]:
                    self.count += 1
                    self.data_name = f'AHA_Polarmap_{sub_name_1}'
                    self.mode = 'aha_polarmap'
                else:
                    self.data_name = None
                    self.mode = None

    def extract_data(self, row):
        """"""
        logger.info(f'{row} {self.mode} {self.data_name}')
        # logger.info(f'{self.sheet.cell(row=row, column=2).value} <-> {self.sheet.cell(row=row, column=3).value}')
    #     if self.sheet.cell(row=row+2, column=4).value == 'time (ms)' and self.sheet.cell(row=row+2, column=2).value == 'slice':
    #         logger.info(self.sheet.cell(row=row, column=2).value)

        message = ''
        # self.sheet.cell(row=row, column=3).value


if __name__ == '__main__':
    import time

    x = time.time()

    ep = ExcelParser(
        src='/home/melandur/Data/extracted',
        dst='/home/melandur/Data/Myocarditis/test_csv_processing')

    ep()
    logger.info(round((time.time() - x)))
