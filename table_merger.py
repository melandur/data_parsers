"""Merge table of subjects"""

import os

import numpy as np
import pandas as pd
from loguru import logger

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class TableMergerColumnBased:
    """Merge table of subjects"""

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = {}

    def __call__(self) -> None:
        subjects = os.listdir(self.src)
        tables = os.listdir(os.path.join(self.src, subjects[0]))

        for table in tables:
            logger.info(f'-> {table}')
            table_name = table.replace('.xlsx', '')
            self.memory = {}
            for subject in subjects:
                logger.info(f'-> {subject}')
                df = pd.read_excel(os.path.join(self.src, subject, table))
                self.memory[subject] = df
            self.merge_column_wise(table_name)

    def merge_column_wise(self, table_name) -> None:
        columns = self.memory[list(self.memory.keys())[0]].columns
        for column in columns:
            df = pd.DataFrame(columns=self.memory.keys())
            for subject in self.memory:
                df[subject] = self.memory[subject][column]
            table_name = table_name.replace('/', '-')
            column = column.replace('/', '-')
            file_path = os.path.join(self.dst, table_name, f'{table_name}_{column}.xlsx')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_excel(file_path, index=False)


class MergeAhaPolarmap:

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = {}

    def __call__(self) -> None:
        df_store = pd.DataFrame()
        for root, _, files in os.walk(self.src):
            for file in files:
                if 'aha_polarmap' in file:
                    if 'mm' in file:
                        print(file)
                        # df = pd.read_excel(os.path.join(root, file))
                        for segment in range(0, 16):




                    # df = pd.read_excel(os.path.join(root, file)).T
                    # for segment in range(0, 16):
                    #
                    #
                    #
                    # # print(df)
                    # df = df.replace(r'\s+', np.nan, regex=True)
                    # print(df.corr())
                    # # self.memory[file] = pd.read_excel(os.path.join(root, file))
                    # logger.info(f'-> {file}')




if __name__ == '__main__':
    src = '/home/melandur/Data/Myocarditis/small_test/table_wise_column'
    dst = '/home/melandur/Data/Myocarditis/merge_test'
    # tm = TableMergerColumnBased(src, dst)
    tm = MergeAhaPolarmap(src, dst)
    tm()
