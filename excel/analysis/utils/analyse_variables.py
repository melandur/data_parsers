import os

from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from excel.analysis.utils.helpers import save_tables, split_data


def univariate_analysis(data: pd.DataFrame, out_dir: str, metadata: list, hue: str, whis: float):
    """
    Perform univariate analysis (box plots and distributions)
    """
    # Split data and metadata but keep hue column
    metadata.remove(hue)
    to_analyse, _, _ = split_data(data, metadata, hue, remove_mdata=True, normalise=False)

    # Box plot for each feature w.r.t. MACE
    data_long = to_analyse.melt(id_vars=[hue])
    sns.boxplot(data=data_long, x='value', y='variable', hue=hue, \
        orient='h', meanline=True, showmeans=True, whis=whis)
    plt.axvline(x=0, alpha=0.7, color='grey', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f'box_plot_{hue}.pdf'))
    plt.clf()

    to_analyse = to_analyse.drop(hue, axis=1) # now remove hue column

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

def bivariate_analysis(to_analyse: pd.DataFrame, out_dir: str, metadata: list):
    """
    Perform bivariate analysis
    """
    pass

def correlation(to_analyse: pd.DataFrame, out_dir: str, metadata: list, method: str='pearson', \
    drop_features: bool=True) -> None:
    """
    Compute correlation between features and optionally drop highly correlated ones
    """
    matrix = to_analyse.corr(method=method).round(2)
    
    # Remove features with high correlation
    
    
    # Plot heatmap
    sns.heatmap(matrix, annot=True, xticklabels=True, yticklabels=True)
    plt.xticks(rotation=90)
    plt.savefig(os.path.join(out_dir, 'corr_plot.pdf'))

def detect_outliers(data: pd.DataFrame, out_dir: str, whis: float, remove:bool, \
    investigate: bool, metadata: list=[]):
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
        high_data = pd.concat((high_data, mdata), axis=1).sort_values(by=['subject'])
        
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