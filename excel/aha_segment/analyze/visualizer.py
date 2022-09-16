"""Read excel files and plot distribution of findings"""

import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from loguru import logger
from scipy.stats import zscore

from excel.path_master import ANALYZE_PATH, MERGED_PATH


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded on the fly"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self) -> str:
        return repr(dict(self))


class VisualizeTable:
    """Visualize table"""

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst

    def __call__(self) -> None:
        logger.info(f'Run: {self.__class__.__name__}')
        df = pd.read_excel(self.src)

        df = df.iloc[:, 1:30]
        # df = df.T
        # create 2 violin plots
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

        # violin plot on left

        sns.violinplot(ax=axes[0], data=df)
        # show outliers
        sns.swarmplot(ax=axes[0], data=df, color="black", alpha=0.75)
        # turn x tick labels 90 degrees
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=60)
        axes[0].set_title('Violin plot')

        # violin plot on left
        # for column in df.columns:
        #     df[column] = zscore(df[column])
        #
        # sns.violinplot(ax=axes[1], data=df)
        # axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=60)
        # axes[1].set_title('Violin plot Zscore')

        plt.show()

        # matplot create subplots
        # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
        # axes[0].plot(df['A'], df['B'], 'o')







        # sns.violinplot(data=df)
        # c
        # plt.show()





        # sns.violinplot(data=df)
        # plt.show()

    def ce_plot(self) -> None:
        pass


# pandas get firs column
# df = pd.read_excel('/home/alex/Downloads/aha_1.xlsx')
# df = df.iloc[:, 1:30]

class VisualizeTableWise:
    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = NestedDefaultDict()

    def __call__(self) -> None:
        """Read excel files and plot distribution of findings"""
        for root, _, files in os.walk(self.src):
            for file in files:
                if 'aha_3d_longit_strain_rate' in file:
                    logger.info(f'-> {file}')
                    df = pd.read_excel(os.path.join(root, file))
                    file_name = file.replace('.xlsx', '')
                    self.plot_tables_aha_polarmap(df, file_name)

    def plot_tables_aha_polarmap(self, df, file_name) -> None:
        """Plotting"""
        if not df.empty:
            plt.clf()
            df = df.T
            df = df[[1]]
            df = df.T
            df = df[[col for col in df.columns if 'sample' in col]]
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


# class VisualizeMergedTable:
#     def __init__(self, src: str, dst: str) -> None:
#         self.src = src
#         self.dst = dst
#         self.memory = NestedDefaultDict()
#
#     def __call__(self) -> None:
#         """Read excel files and plot distribution of findings"""
#         for root, _, files in os.walk(self.src):
#             for file in files:
#                 if 'aha_polarmap' in file:
#                     logger.info(f'-> {file}')
#                     df = pd.read_excel(os.path.join(root, file))
#                     file_name = file.replace('.xlsx', '')
#                     self.plot_tables_aha_polarmap(df, file_name)
#
#     def plot_tables_aha_polarmap(self, df, file_name) -> None:
#         """Plotting"""
#         plt.clf()
#         df = df.T
#         df = df.replace(r'\s+', np.nan, regex=True)
#         sns.set(style="whitegrid")
#         sns.boxplot(data=df)
#         plt.title(file_name)
#         plt.ylabel(file_name)
#         plt.xlabel('Aha-Segment')
#         # file_path = os.path.join(self.dst, f'{file_name}.png')
#         # os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         # plt.savefig(file_path)
#         # plt.close()
#         # plt.show()
#         plt.waitforbuttonpress()
#         plt.draw()


if __name__ == '__main__':
    src = MERGED_PATH
    dst = ANALYZE_PATH
    # vmt = VisualizeTableWise(src, dst)
    # vmt()

    vt = VisualizeTable(f'{src}/z_score/aha_longit_strain_rate_1.xlsx', dst)
    vt()
