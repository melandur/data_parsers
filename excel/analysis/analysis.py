""" Analysis module for all kinds of experiments
"""

import os

import hydra
from loguru import logger
from omegaconf import DictConfig
import pandas as pd

from excel.analysis.utils.merge_data import MergeData
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
    exploration = config.analysis.exploration

    # TODO: train and test paths/sets
    merged_dir = os.path.join(src_dir, '5_merged')

    # Data merging
    if os.path.isdir(merged_dir) and not overwrite:
        logger.info('Merged data available, moving directly to analysis.')
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
    data = pd.read_excel(os.path.join(merged_dir, f'{experiment}.xlsx'))

    # Data exploration
    explorer = ExploreData(
        data=data,
        experiment=experiment,
        exploration=exploration
    )
    explorer()


if __name__ == '__main__':
    analysis()
    
