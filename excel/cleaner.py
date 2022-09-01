import os

import numpy as np
import pandas as pd

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
            subject_path = os.path.join(self.src, subject)
            tables = os.listdir(subject_path)
            for table in tables:
                print(subject, table)
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
                df.to_excel(export_path, index=False)


if __name__ == '__main__':
    src = '/home/melandur/Data/Myocarditis/test_csv_processing'
    dst = '/home/melandur/Data/Myocarditis/test_csv_processing_clean'
    tc = TableCleaner(src, dst)
    tc()
