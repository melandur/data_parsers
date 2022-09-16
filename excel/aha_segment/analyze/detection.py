import pandas as pd


def get_mean_and_std(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    mean = df.median(axis=0)
    std = df.std(axis=0)
    return mean, std


df_test = pd.read_excel('/home/melandur/Data/Myocarditis/csv/test/7_merged/z_score/aha_longit_strain_rate_10.xlsx')
df_train = pd.read_excel('/home/melandur/Data/Myocarditis/csv/train/7_merged/z_score/aha_longit_strain_rate_10.xlsx')

df_test = df_test.iloc[:, 1:]
df_test = df_test.transpose()

df_train = df_train.iloc[:, 1:]
df_train = df_train.transpose()

mean_test, std_test = get_mean_and_std(df_test)
mean_train, std_train = get_mean_and_std(df_train)

tot_mean_train = mean_train.median()
tot_std_train = mean_train.std()

tot_mean_test = mean_test.median()
tot_std_test = mean_test.std()


print('test', tot_mean_train, tot_std_train)
print('train', tot_mean_test, tot_std_test)

# get header name of first column
header = df_train.columns.tolist()
print(header)

df_filtered = df_train[df_train.columns[df_train.median(axis=0) < tot_mean_test]]
df_filtered = df_filtered[df_filtered.columns[df_filtered.median(axis=0) > -tot_mean_test]]
print(df_filtered)