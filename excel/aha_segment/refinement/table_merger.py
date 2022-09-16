import os

import pandas as pd
from loguru import logger

from excel.path_master import CONDENSED_PATH, MERGED_PATH

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class MergeSegments:
    """Merge table of subjects"""

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = {}

    def __call__(self, name) -> None:
        self.aggregate_data_frames(name)
        self.merge_column_wise(name)
        self.merge_row_wise(name)

    def aggregate_data_frames(self, name: str) -> None:
        """Aggregate data frames"""
        self.memory = {}
        for root, _, files in os.walk(self.src):
            for file in files:
                if file.endswith('.xlsx') and name in file:
                    file_path = os.path.join(root, file)
                    logger.info(f'-> {file}')
                    df = pd.read_excel(file_path)
                    table_name = file.replace('.xlsx', '')
                    self.memory[table_name] = df

    def merge_column_wise(self, table_name) -> None:
        """Merge columns of data frames"""
        columns = self.memory[list(self.memory.keys())[0]].columns  # get column names of first subject
        for column in columns:
            if not 'AHA Segment' in column:
                df = pd.DataFrame(columns=self.memory.keys())
                for subject in self.memory:
                    df[subject] = self.memory[subject][column]

                header = df.columns.tolist()
                header = [f'case_{x.split("_")[0]}' for x in header]
                df.columns = header
                df.rename(index={0: 'global'}, inplace=True)
                self.save(df, f'aha_{table_name}_{column}')

    def merge_row_wise(self, table_name) -> None:
        """Merge columns of data frames"""
        tmp_df = self.memory[list(self.memory.keys())[0]]
        tmp_df = tmp_df.transpose()
        columns = tmp_df.columns.tolist()
        for column in columns:
            df = pd.DataFrame(columns=self.memory.keys())

            for subject in self.memory:
                x = self.memory[subject].transpose()
                df[subject] = x[column]

            header = df.columns.tolist()
            header = [f'case_{x.split("_")[0]}' for x in header]
            df.columns = header
            df.rename(index={0: 'global'}, inplace=True)
            if column == 0:
                column = 'global'
            df = df.iloc[1:]  # remove global row
            self.save(df, f'aha_{table_name}_{column}')

    def save(self, df: pd.DataFrame, name: str) -> None:
        name = name.replace('/', '-')
        file_path = os.path.join(self.dst, f'{name}.xlsx')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_excel(file_path, index=True)


if __name__ == '__main__':
    src = CONDENSED_PATH
    dst = MERGED_PATH
    tm = MergeSegments(src, dst)
    for name in ['longit_strain_rate', 'radial_strain_rate', 'circumf_strain_rate']:
        tm(name)