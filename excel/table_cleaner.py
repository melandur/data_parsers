import os

import numpy as np
import pandas as pd
from loguru import logger

from excel.path_master import TABLE_WISE_PATH, CLEANED_PATH

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class TableCleaner:
    """Intra-/Extrapolate NaN rows or delete them"""
    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst

    def __call__(self):
        subjects = os.listdir(self.src)
        for subject in subjects:
            logger.info(f'-> {subject}')
            subject_path = os.path.join(self.src, subject)
            tables = os.listdir(subject_path)
            for table in tables:
                logger.info(f'--> {table}')
                table_path = os.path.join(subject_path, table)
                df = pd.read_excel(table_path, index_col=0)
                for x in ['nan ', 'nan', 'NaN', 'NaN ']:
                    df = df.replace(x, np.nan)
                if 'peak_strain_rad_%' in df:
                    if any(df['peak_strain_rad_%'] == '--'):
                        df['peak_strain_rad_%'] = df['peak_strain_rad_%'].replace('--', np.NAN)
                df.dropna(inplace=True)
                df = df.reset_index(drop=True)
                export_path = os.path.join(self.dst, subject, table)
                os.makedirs(os.path.dirname(export_path), exist_ok=True)
                df.to_excel(export_path)


if __name__ == '__main__':
    src = TABLE_WISE_PATH
    dst = CLEANED_PATH
    tc = TableCleaner(src, dst)
    tc()
