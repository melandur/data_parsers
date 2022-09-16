import os

import pandas as pd
import statsmodels.api as sm

import matplotlib.pyplot as plt
import seaborn as sns

"""Load data as data frame"""
src_train = '/home/melandur/Data/Myocarditis/csv/train/7_merged/'
src_test = '/home/melandur/Data/Myocarditis/csv/test/7_merged/'


def load_data(path):
    files = os.listdir(path)
    df_store = {}
    for file in files:
        if 'aha' in file and 'sample' not in file:
            file_path = os.path.join(path, file)
            df = pd.read_excel(file_path, )
            name = f"{file.split('_')[1]}_{file.split('_')[-1]}".split('.xlsx')[0]
            df_store[name] = df.iloc[:, 1:]  # drop first column
    return df_store


def merge_columns(store, idx, threshold):
    lon = store[f'longit_{idx}'].iloc[:, :threshold]
    data = lon.melt()
    rad = store[f'radial_{idx}'].iloc[:, :threshold]
    rad = rad.melt()
    data = pd.concat([data, rad], axis=1)
    cir = store[f'circumf_{idx}'].iloc[:, :threshold]
    cir = cir.melt()
    data = pd.concat([data, cir], axis=1)
    data = data.drop(['variable'], axis=1)
    header = ['longit', 'radial', 'circumf']
    data.columns = header
    return data


def fused_columns(store_1, store_2, idx, strain, threshold):
    value_1 = store_1[f'{strain}_{idx}'].iloc[:, :threshold]
    value_1 = value_1.melt()
    value_2 = store_2[f'{strain}_{idx}'].iloc[:, :threshold]
    value_2 = value_2.melt()

    data = pd.concat([value_1, value_2], axis=1)
    data = data.drop(['variable'], axis=1)
    header = ['affected', 'control']
    data.columns = header
    return data

# df_train = merge_columns(df_train, idx, threshold)
# df_test = merge_columns(df_test, idx, threshold)


def fused_columns_1(store_1, store_2, idx, threshold):
    value_l1 = store_1[f'longit_{idx}'].iloc[:, :threshold]
    value_l1 = value_l1.melt()
    value_l2 = store_2[f'longit_{idx}'].iloc[:, :threshold]
    value_l2 = value_l2.melt()
    value_r1 = store_1[f'radial_{idx}'].iloc[:, :threshold]
    value_r1 = value_r1.melt()
    value_r2 = store_2[f'radial_{idx}'].iloc[:, :threshold]
    value_r2 = value_r2.melt()
    value_c1 = store_1[f'circumf_{idx}'].iloc[:, :threshold]
    value_c1 = value_c1.melt()
    value_c2 = store_2[f'circumf_{idx}'].iloc[:, :threshold]
    value_c2 = value_c2.melt()

    data = pd.concat([value_l1, value_l2, value_r1, value_r2, value_c1, value_c2], axis=1)
    data = data.drop(['variable'], axis=1)
    header = ['longit_affected', 'longit_control', 'radial_affected', 'radial_control', 'circumf_affected', 'circumf_control']
    data.columns = header
    return data


if __name__ == '__main__':

    threshold = 51

    df_train_1 = load_data(src_train)
    df_test_1 = load_data(src_test)


    for idx in range(1, 17):
        df_fused = fused_columns_1(df_train_1, df_test_1, idx, threshold)
        matrix = df_fused.corr().round(2)
        sns.heatmap(matrix, annot=True)
        plt.title(f'Strain rate corr matrix fused\nAHA segment {idx} | cases: {threshold}')
        plt.tight_layout()
        plt.savefig(f'/home/melandur/plot/aha_heatmap_fused_{idx}.png', dpi=300)
        plt.close()
        plt.cla()

        # for strain in ['longit', 'radial', 'circumf']:
        #     df_fused = fused_columns(df_train_1, df_test_1, idx, strain, threshold)
        #
        #     g = sns.jointplot(data=df_fused, x='affected', y='control')
        #     g.plot(sns.scatterplot, sns.histplot)
        #     g.fig.subplots_adjust(top=0.93)  # adjust the Figure in rp
        #     g.fig.suptitle(f'Strain Rates [1/s] | AHA segment {idx} | cases: {threshold}')
        #     plt.savefig(f'/home/melandur/plot/aha_seg_{idx}_{strain}.png', dpi=300)
            # sns.jointplot(data=df_test, x='longit', y='circumf')
            # sns.jointplot(data=df_test, x='radial', y='circumf')


        # df_train = merge_columns(df_train_1, idx, threshold)
        # df_test = merge_columns(df_test_1, idx, threshold)

        # matrix = df_test.corr().round(2)
        # sns.heatmap(matrix, annot=True)
        # plt.title(f'Strain rate correlation matrix\nAHA segment {idx} | cases: {threshold}')
        # plt.savefig(f'/home/melandur/plot/aha_heatmap_{idx}.png', dpi=300)
        # plt.close()
        # plt.cla()
        #
        # g = sns.jointplot(data=df_test, x='longit', y='radial')
        # g.fig.subplots_adjust(top=0.93)
        # g.fig.suptitle(f'Strain Rates [1/s] | AHA segment {idx} | cases: {threshold}')
        # g.ax_joint.set_xlabel('Longitudinal')
        # g.ax_joint.set_ylabel('Radial')
        # plt.savefig(f'/home/melandur/plot/aha_2d_segment_{idx}.png', dpi=300)
        # plt.close()
        # plt.cla()
        #
        # g = sns.jointplot(data=df_test, x='longit', y='radial', hue='circumf')
        # g.fig.subplots_adjust(top=0.93)
        # g.fig.suptitle(f'Strain Rates [1/s] | AHA segment {idx} | cases: {threshold}')
        # g.ax_joint.set_xlabel('Longitudinal')
        # g.ax_joint.set_ylabel('Radial')
        # plt.savefig(f'/home/melandur/plot/aha_3d_segment_{idx}.png', dpi=300)
        # plt.close()
        # plt.cla()
