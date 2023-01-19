import os

from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def univariate_analysis(data: pd.DataFrame, out_dir: str):
    """
    Perform univariate analysis (box plots and distributions)
    """
    # Box plot for each feature w.r.t. MACE
    data[data['mace'] == 999] = 0
    # data = remove_outliers(data, n_std=3)
    data_long = data.melt(id_vars=['mace'])
    sns.boxplot(data=data_long, x='value', y='variable', hue='mace', \
        orient='h', meanline=True, showmeans=True)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'box_plot_mace.pdf'))

    # Box plot for each feature
    sns.boxplot(data=data, orient='h', meanline=True, showmeans=True)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'box_plot.pdf'))
    # plt.show()

    # Plot distribution for each feature
    sns.displot(data=data, kind='kde')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'dis_plot.pdf'))
    # plt.show()

def bivariate_analysis(data: pd.DataFrame, out_dir: str):
    """
    Perform bivariate analysis
    """
    pass

def remove_outliers(df, n_std=3):
    for _, values in df.iteritems():
        mean = values.mean()
        sd = values.std()
        df = df[(values <= mean + (n_std * sd))]
    return df