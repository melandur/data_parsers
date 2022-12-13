import os

import numpy as np
import pandas as pd
from loguru import logger

from excel.path_master import CASE_WISE_PATH, CLEANED_PATH

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class TableCleaner:
    """Inter-/Extrapolate NaN rows or delete them"""

    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst

    def __call__(self) -> None:
        for subject in self.loop_subjects():
            for dim in ['2d', '3d']:
                for table in self.loop_tables(subject, dim):
                    df = self.clean(subject, dim, table)
                    self.save(df, subject, dim, table)

    def loop_subjects(self) -> str:
        """Loop over subjects"""
        for subject in os.listdir(self.src):
            logger.info(f'-> {subject}')
            yield subject

    def loop_tables(self, subject: str, dim: str) -> str:
        """Loop over tables"""
        if os.path.exists(os.path.join(self.src, subject, dim)):
            for table in os.listdir(os.path.join(self.src, subject, dim)):
                yield table

    def clean(self, subject: str, dim: str, table: str) -> pd.DataFrame:
        """Clean table"""
        table_path = os.path.join(self.src, subject, dim, table)
        df = pd.read_excel(table_path)

        # Standardise missing entries into np.nan
        for x in ['nan ', 'nan', 'NaN', 'NaN ']:
            df = df.replace(x, np.nan)
        if 'peak_strain_rad_%' in df:
            if any(df['peak_strain_rad_%'] == '--'):
                df['peak_strain_rad_%'] = df['peak_strain_rad_%'].replace('--', np.nan)

        # TODO: add inter- or extrapolation functionalities
        # current version drops all rows/cols containing at least one NaN value
        df.dropna(inplace=True)
        df = df.reset_index(drop=True)
        return df

    def save(self, df: pd.DataFrame, subject: str, dim: str, table: str) -> None:
        """Save table"""
        export_path = os.path.join(self.dst, subject, dim, table)
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        df.to_excel(export_path, index=False)
        logger.info(f'-> {table}')


if __name__ == '__main__':
    src = CASE_WISE_PATH
    dst = CLEANED_PATH
    tc = TableCleaner(src, dst)
    tc()
