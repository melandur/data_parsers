import os
from collections import defaultdict

import numpy as np
import pandas as pd
from loguru import logger

# from excel.path_master import CASE_WISE_PATH, CLEANED_PATH

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded on the fly"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self) -> str:
        return repr(dict(self))

class TableCleaner:
    """Inter-/Extrapolate NaN rows or delete them"""

    def __init__(self, src: str, dst: str, save_intermediate: bool=True, \
        dims: list=['2d'], tables: NestedDefaultDict=None) -> None:
        self.src = src
        self.dst = dst
        self.save_intermediate = save_intermediate
        self.dims = dims
        self.tables = tables

    def __call__(self) -> NestedDefaultDict:
        for subject in self.loop_subjects():
            for dim in self.dims:

                if self.save_intermediate:
                    for table in self.loop_tables(subject, dim):
                        df = self.clean(subject, dim, table)
                        self.save(df, subject, dim, table)

                else: # use dict of DataFrames
                    for table in self.tables[subject][dim]:
                        self.tables[subject][dim][table] = self.clean(subject, dim, table)

        return self.tables


    def loop_subjects(self) -> str:
        """Loop over subjects"""
        if self.save_intermediate:
            for subject in os.listdir(self.src):
                logger.info(f'-> {subject}')
                yield subject
        else:
            for subject in self.tables.keys():
                logger.info(f'-> {subject}')
                yield subject

    def loop_tables(self, subject: str, dim: str) -> str:
        """Loop over tables"""
        if os.path.exists(os.path.join(self.src, subject, dim)):
            for table in os.listdir(os.path.join(self.src, subject, dim)):
                yield table

    def clean(self, subject: str, dim: str, table: str) -> pd.DataFrame:
        """Clean table"""
        if self.save_intermediate:
            path = os.path.join(self.src, subject, dim, table)
            df = pd.read_excel(path)

        else:
            df = self.tables[subject][dim][table]

        if df is None:
            return None

        # Standardise missing entries into np.nan
        for x in ['nan ', 'nan', 'NaN', 'NaN ']:
            df = df.replace(x, np.nan)
        if 'peak_strain_rad_%' in df:
            if any(df['peak_strain_rad_%'] == '--'):
                df['peak_strain_rad_%'] = df['peak_strain_rad_%'].replace('--', np.nan)

        # TODO: add inter- or extrapolation functionalities
        # current version drops all rows/cols containing at least one NaN value
        # might want to introduce flag to show whether any NaN values were present
        # or how much data was removed
        # nans = df.isna().sum()
        df.dropna(inplace=True)
        df = df.reset_index(drop=True)
        return df

    def save(self, df: pd.DataFrame, subject: str, dim: str, table: str) -> None:
        """Save table"""
        export_path = os.path.join(self.dst, subject, dim, table)
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        df.to_excel(export_path, index=False)
        logger.info(f'-> {table}')


# if __name__ == '__main__':
#     # src = CASE_WISE_PATH
#     # dst = CLEANED_PATH
#     src = '/home/sebalzer/Documents/Mike_init/tests/train/2_case_wise'
#     dst = '/home/sebalzer/Documents/Mike_init/tests/train/3_cleaned'
#     tc = TableCleaner(src, dst)
#     tc()
