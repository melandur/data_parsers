import os

from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from excel.analysis.utils.helpers import save_tables


def univariate_analysis(data: pd.DataFrame, out_dir: str, metadata: list, whis: float):
    """
    Perform univariate analysis (box plots and distributions)
    """
    # Split data and metadata but keep mace for now
    metadata.remove('mace')
    mdata = data[metadata]
    to_analyse = data.drop(metadata, axis=1)

    # Box plot for each feature w.r.t. MACE
    data_long = to_analyse.melt(id_vars=['mace'])
    sns.boxplot(data=data_long, x='value', y='variable', hue='mace', \
        orient='h', meanline=True, showmeans=True, whis=whis)
    plt.axvline(x=0, alpha=0.7, color='grey', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'box_plot_mace.pdf'))
    plt.clf()

    to_analyse = to_analyse.drop('mace', axis=1) # now remove mace column

    # Box plot for each feature
    sns.boxplot(data=to_analyse, orient='h', meanline=True, showmeans=True, whis=whis)
    plt.axvline(x=0, alpha=0.7, color='grey', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'box_plot.pdf'))
    plt.clf()

    # Plot distribution for each feature
    sns.displot(data=to_analyse, kind='kde')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'dis_plot.pdf'))
    plt.clf()

def bivariate_analysis(to_analyse: pd.DataFrame, out_dir: str, metadata:list):
    """
    Perform bivariate analysis
    """
    pass

def detect_outliers(data: pd.DataFrame, out_dir: str, whis: float=1.5, remove: bool=True, \
    investigate: bool=False, metadata: list=[]):
    """Detect outliers in the data, optionally removing or further investigating them

    Args:
        data (pd.DataFrame): data
        whis (float, optional): determines reach of the whiskers. Defaults to 1.5 (matplotlib default)
        remove (bool, optional): whether to remove outliers. Defaults to True.
        investigate (bool, optional): whether to investigate outliers. Defaults to False.
    """
    # Split data and metadata
    mdata = data[metadata]
    to_analyse = data.drop(metadata, axis=1)

    # Calculate quartiles, interquartile range and limits
    q1, q3 = np.percentile(to_analyse, [25, 75], axis=0)
    iqr = q3 - q1
    lower_limit = q1 - whis*iqr
    upper_limit = q3 + whis*iqr
    # logger.debug(f'\nlower limit: {lower_limit}\nupper limit: {upper_limit}')

    # Investigation
    if investigate:
        high_data = to_analyse.copy(deep=True)
        # Remove rows without outliers
        # high_data = high_data.drop(high_data.between(lower_limit, upper_limit).all(), axis=0)

        # Add metadata again
        high_data = pd.concat((high_data, mdata), axis=1).sort_values('mace')
        
        # Highlight outliers in table
        high_data.style.apply(lambda _: highlight(df=high_data, lower_limit=lower_limit, \
            upper_limit=upper_limit), axis=None)\
            .to_excel(os.path.join(out_dir, 'investigate_outliers.xlsx'), index=True)
        

    # Removal
    if remove:
        to_analyse = to_analyse.mask(to_analyse.le(lower_limit) | to_analyse.ge(upper_limit))
        to_analyse.to_excel(os.path.join(out_dir, 'outliers_removed.xlsx'), index=True)
        
        # Add metadata again
        data = pd.concat((to_analyse, mdata), axis=1)

        # TODO: deal with removed outliers (e.g. remove patient)

    return data


def highlight(df: pd.DataFrame, lower_limit: np.array, upper_limit: np.array):
    style_df = pd.DataFrame('', index=df.index, columns=df.columns)
    mask = pd.concat([~df.iloc[:, i].between(lower_limit[i], upper_limit[i], inclusive='neither')\
        for i in range(lower_limit.size)], axis=1)
    style_df = style_df.mask(mask, 'background-color: red')

    # Uncolor metadata
    style_df.iloc[:, lower_limit.size:] = ''

    return style_df