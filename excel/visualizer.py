"""Read excel files and plot distribution of findings"""

import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from loguru import logger


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded on the fly"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self) -> str:
        return repr(dict(self))


class VisualizeTableWise:

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = NestedDefaultDict()

    def __call__(self) -> None:
        """Read excel files and plot distribution of findings"""
        for root, _, files in os.walk(self.src):
            for file in files:
                if 'aha_polarmap' in file:
                    logger.info(f'-> {file}')
                    df = pd.read_excel(os.path.join(root, file))
                    file_name = file.replace('.xlsx', '')
                    self.plot_tables_aha_polarmap(df, file_name)

    def plot_tables_aha_polarmap(self, df, file_name) -> None:
        """Plotting"""
        plt.clf()
        df = df.T
        df = df.replace(r'\s+', np.nan, regex=True)
        sns.set(style="whitegrid")
        sns.boxplot(data=df)
        plt.title(file_name)
        plt.ylabel(file_name)
        plt.xlabel('Aha-Segment')
        # file_path = os.path.join(self.dst, f'{file_name}.png')
        # os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # plt.savefig(file_path)
        # plt.close()
        # plt.show()
        plt.waitforbuttonpress()
        plt.draw()


class VisualizeMergedTable:

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = NestedDefaultDict()

    def __call__(self) -> None:
        """Read excel files and plot distribution of findings"""
        for root, _, files in os.walk(self.src):
            for file in files:
                if 'aha_polarmap' in file:
                    logger.info(f'-> {file}')
                    df = pd.read_excel(os.path.join(root, file))
                    file_name = file.replace('.xlsx', '')
                    self.plot_tables_aha_polarmap(df, file_name)

    def plot_tables_aha_polarmap(self, df, file_name) -> None:
        """Plotting"""
        plt.clf()
        df = df.T
        df = df.replace(r'\s+', np.nan, regex=True)
        sns.set(style="whitegrid")
        sns.boxplot(data=df)
        plt.title(file_name)
        plt.ylabel(file_name)
        plt.xlabel('Aha-Segment')
        # file_path = os.path.join(self.dst, f'{file_name}.png')
        # os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # plt.savefig(file_path)
        # plt.close()
        # plt.show()
        plt.waitforbuttonpress()
        plt.draw()


if __name__ == '__main__':
    src = '/home/melandur/Data/Myocarditis/csv_preprocessing/raw/table_wise_column'
    dst = '/home/melandur/Data/Myocarditis/plotly/'
    # vtw = VisualizeTableWise(src, dst)
    vmt = Visualize(src, dst)
    vmt()
