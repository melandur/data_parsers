import os

import hydra
from omegaconf import DictConfig
from loguru import logger
import pandas as pd
import numpy as np
from functools import reduce

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


@hydra.main(version_base=None, config_path='.', config_name='cleanup')
def cleanup(config: DictConfig) -> None:
    """Function for excel sheet cleanup and merging

    Args:
        config (DictConfig): config file for file paths, etc. 
    """
    # Parse config parameters
    src_dir = config.src_dir
    files = config.files
    writer = pd.ExcelWriter(os.path.join(src_dir, 'combined.xlsx'), engine='xlsxwriter')
    dataframes = []
    merge_on = ['record_id']
    colors = ['lightgrey', 'lightcoral', 'lightyellow', 'lightseagreen', 'lightcyan', 'lightblue']

    for key, file in files.items():
        # Read data (only need first sheet)
        data = pd.read_excel(os.path.join(src_dir, file))
        # Clean data
        data = data.drop(index=0, axis=0) # drop first row
        data.iloc[:, 9:] = data.iloc[:, 9:].replace(r'[a-zA-Z%/²]', '', regex=True) # remove units
        data.iloc[:, 9:] = data.iloc[:, 9:].replace(0, np.nan) # set 0 values to NaN      
        data = data.sort_values(by='record_id')

        data.columns = ['{}{}'.format(c, '' if c in merge_on else f'_{key}') for c in data.columns]
        dataframes.append(data)

        # Write data to new excel file
        data.to_excel(writer, sheet_name=key, index=False, float_format='%.0f')

    # Combine all sheets into one
    combined = reduce(lambda left, right: pd.merge(left, right, on=merge_on, how='outer'), dataframes)
    combined.style.apply(lambda col: highlight_cols(col, files.keys(), colors), axis=0).to_excel(writer, \
        sheet_name='combined', index=False, float_format='%.0f')
    writer.close()


def highlight_cols(col: pd.Series, suffixes: list, colors: list) -> str:
    for i, suffix in enumerate(suffixes):
        if suffix in col.name:
            return [f'background-color: {colors[i]}'] * (len(col)-1)

    return [''] * (len(col)-1)

if __name__ == '__main__':
    cleanup()
