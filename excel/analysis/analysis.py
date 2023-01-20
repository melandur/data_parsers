""" Analysis module for all kinds of experiments
"""

import os

import hydra
from loguru import logger
from omegaconf import DictConfig
import pandas as pd

from excel.analysis.utils.merge_data import MergeData
from excel.analysis.utils.update_metadata import UpdateMetadata
from excel.analysis.utils.exploration import ExploreData


@hydra.main(version_base=None, config_path='../../config', config_name='config')
def analysis(config: DictConfig) -> None:
    """Analysis pipeline

    Args:
        config (DictConfig): config element containing all config parameters
            check the config files for info on the individual parameters

    Returns:
        None
    """    
    # Parse some config parameters
    src_dir = config.dataset.out_dir
    mdata_src = config.dataset.mdata_src
    dims = config.dataset.dims

    segments = config.analysis.segments
    axes = config.analysis.axes
    orientations = config.analysis.orientations
    metrics = config.analysis.metrics
    peak_values = config.analysis.peak_values
    metadata = config.analysis.metadata
    experiment = config.analysis.experiment
    overwrite = config.analysis.overwrite
    update_metadata = config.analysis.update_metadata
    exploration = config.analysis.exploration
    whis = config.analysis.whis

    # TODO: train and test paths/sets
    merged_path = os.path.join(src_dir, '5_merged', f'{experiment}.xlsx')

    # Data merging
    if os.path.isfile(merged_path) and not overwrite:
        logger.info('Merged data available, skipping merge step...')
    else:
        logger.info('Merging data according to config parameters...')
        merger = MergeData(
            src=src_dir,
            mdata_src=mdata_src,
            dims=dims,
            segments=segments,
            axes=axes,
            orientations=orientations,
            metrics=metrics,
            peak_values=peak_values,
            metadata=metadata,
            experiment=experiment
        )
        merger()
        logger.info('Data merging finished.')

    # Read in merged data
    data = pd.read_excel(merged_path)

    # Update metadata if desired (only makes sense if overwrite=False)
    if not overwrite and update_metadata:
        logger.info('Updating metadata as requested...')
        updater = UpdateMetadata(
            src=src_dir,
            data=data,
            mdata_src=mdata_src,
            metadata=metadata,
            experiment=experiment
        )
        data = updater()
        logger.info('Metadata update finished.')

    # Use subject ID as index column
    data = data.set_index('subject')

    # Data exploration
    if exploration:
        expl_dir = os.path.join(src_dir, '6_exploration')
        os.makedirs(expl_dir, exist_ok=True)

        explorer = ExploreData(
            data=data,
            experiment=experiment,
            exploration=exploration,
            out_dir=expl_dir,
            remove_meta=True, # might want to add config param
            metadata=metadata,
            whis=whis
        )   
        explorer()


if __name__ == '__main__':
    analysis()
    
