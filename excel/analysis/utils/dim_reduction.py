"""Dimensionality reduction module
"""

import os

from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA


def pca(data: pd.DataFrame, out_dir: str, metadata: list, seed: int):
    """Perform Principal Component Analysis (PCA)

    Args:
        data (pd.DataFrame): DataFrame containing all relevant features and metadata (opt.)
        out_dir (str): directory to store plots
        metadata (list): list of metadata column names
        seed (int): random seed
    """
    for remove_mdata in [True, False]:

        to_analyse = data.copy(deep=True)
        to_analyse = to_analyse.dropna(how='any') # drop rows containing any NaN values

        if remove_mdata:
            # Split data and metadata
            mdata = to_analyse[metadata]
            to_analyse = to_analyse.drop(metadata, axis=1)
            suffix = 'no_metadata'
        else: # keep metadata
            mdata = to_analyse[['mace']]
            to_analyse = to_analyse.drop('mace', axis=1)
            suffix = 'with_metadata'

        # Perform PCA
        pca = PCA(n_components=4)
        analysis = pca.fit_transform(to_analyse)
        analysis = pd.DataFrame(analysis, index=to_analyse.index, columns=['pc_1', 'pc_2', 'pc_3', 'pc_4'])
        analysis = pd.concat((analysis, mdata['mace']), axis=1)
        explained_var = pca.explained_variance_ratio_
        logger.info(f'Variance explained: {explained_var} for {len(analysis.index)} subjects ({suffix}).')

        # Plot the transformed dataset
        sns.lmplot(data=analysis, x='pc_1', y='pc_2', hue='mace', \
            fit_reg=False, legend=True, scatter_kws={'s': 20})
        # plt.tight_layout()
        plt.xlabel(f'First PC (explains {int(round(explained_var[0], 2) * 100)}% of variance)')
        plt.ylabel(f'Second PC (explains {int(round(explained_var[1], 2) * 100)}% of variance)')
        plt.title('Principal Component Analysis')
        plt.savefig(os.path.join(out_dir, f'PCA_{suffix}.pdf'), bbox_inches='tight')
        plt.clf()


def tsne(data: pd.DataFrame, out_dir: str, metadata: list, seed: int):
    """Perform t-SNE dimensionality reduction and visualisation

    Args:
        data (pd.DataFrame): DataFrame containing all relevant features and metadata (opt.)
        out_dir (str): directory to store plots
        metadata (list): list of metadata column names
        seed (int): random seed
    """
    pass
