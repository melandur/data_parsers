import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
import numpy as np
import os

print(pd.__version__)

from loguru import logger
from excel.path_master import ANALYZE_PATH, CONDENSED_PATH


class StatsRowWise:
    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = {}

    def __call__(self) -> None:
        for subject in self.loop_subjects():
            for _ in self.loop_rows(subject):
                None

    def loop_subjects(self) -> str:
        """Loop over subjects"""
        for subject in os.listdir(self.src):
            logger.info(f'-> {subject}')
            pd = pd.read_excel(os.path.join(self.src, subject))
            yield pd

    @staticmethod
    def normalization(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize table"""
        df = df.apply(zscore)
        return df

    def loop_rows(self, subject: str, dim: str) -> str:
        """Loop over tables"""
        if os.path.exists(os.path.join(self.src, subject, dim)):
            for table in os.listdir(os.path.join(self.src, subject, dim)):
                if 'strain_rate' in table:
                    logger.info(f'-> {table}')
                    yield table

    # def print(self) -> None:
    #     # pd read multiple excel files
    #
    #     corr = df_r.corrwith(df_c)
    #
    #     # df = df.iloc[1:]  # remove first row
    #     # df = df.drop(df.columns[0], axis=1)  # remove first column
    #     #
    #     # # for column in df.columns:
    #     # #     df[column] = zscore(df[column])
    #     #
    #     # # corr = df.corr()
    #     # # print(corr)
    #     #
    #     # corr = np.corrcoef(df, rowvar=False)
    #     # print(corr)
    #     #
    #     print(corr)
    #     sns.heatmap(corr)
    #     plt.show()


if __name__ == '__main__':
    src = CONDENSED_PATH
    dst = '/home/alex/Downloads/CE'
    stats = StatsRowWise(src, dst)
    stats()
