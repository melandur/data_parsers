import os

from loguru import logger
import pandas as pd

def merge_metadata(data, mdata_src, metadata) -> pd.DataFrame:
    # Always want patient ID
    metadata = ['pat_id'] + metadata
    mdata = pd.read_excel(mdata_src)
    mdata = mdata[metadata]
    mdata = mdata[mdata['pat_id'].notna()] # remove rows without pat_id
    mdata = mdata.rename(columns={'pat_id': 'subject'})
    mdata['subject'] = mdata['subject'].astype(int)
    data['subject'] = data['subject'].astype(int)

    # Merge the cvi42 data with available metadata
    data = data.merge(mdata, how='left', on='subject')

    return data

def save_tables(src, experiment, tables) -> None:
        file_path = os.path.join(src, '5_merged', f'{experiment}.xlsx')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tables.to_excel(file_path, index=False)