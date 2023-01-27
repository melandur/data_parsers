import os

import hydra
from omegaconf import DictConfig
from loguru import logger
import pandas as pd

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

    # Read data (only need first sheet)
    for key, file in files.items():
        data = pd.read_excel(os.path.join(src_dir, file))
        # Clean data
        data = data.drop(index=0, axis=0) # drop first row
        data.iloc[:, 9:] = data.iloc[:, 9:].replace(r'[a-zA-Z%/²]', '', regex=True) # remove units
        
    
        # Write data to new excel file
        data.to_excel(writer, sheet_name=key)
    writer.close()


if __name__ == '__main__':
    cleanup()
