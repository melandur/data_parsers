"""Dimensionality reduction module
"""

import os

from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA


def pca(data: pd.DataFrame, out_dir: str, metadata: list):
    """Perform Principal Component Analysis (PCA)

    Args:
        data (pd.DataFrame): DataFrame containing all relevant features and metadata (opt.)
        out_dir (str): directory to store plots
        metadata (list): list of metadata column names
    """
    # Split data and metadata
    mdata = data[metadata]
    to_analyse = data.drop(metadata, axis=1)

    # Perform PCA
    pca = PCA(n_components=2)
    analysis = pca.fit_transform(to_analyse)
    analysis = pd.DataFrame(analysis, columns=['pc_1', 'pc_2'])
    analysis = pd.concat((analysis, mdata['mace']), axis=1)
    data_long = analysis.melt(id_vars=['mace'])
    # logger.debug(data_long)

    # Plot the transformed dataset
    sns.scatterplot(data=data_long, x='pc_1', y='pc_2', hue='mace')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'PCA.pdf'))
    plt.clf()

