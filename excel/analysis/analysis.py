""" Analysis module for all kinds of experiments
"""

import os

import hydra
from loguru import logger
from omegaconf import DictConfig

from excel.global_helpers import checked_dir
from excel.analysis.utils.merge_data import MergeData


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

    dir_name = checked_dir(dims)

    # TODO: train and test paths/sets
    logger.info('Extracting data according to config parameters...')
    merger = MergeData(
        src=os.path.join(src_dir, '4_checked', dir_name),
        mdata_src=mdata_src,
        dims=dims,
        segments=segments,
        axes=axes,
        orientations=orientations,
        metrics=metrics,
        peak_values=peak_values,
        metadata=metadata
    )
    data = merger()
    logger.info('Data extraction finished.')


if __name__ == '__main__':
    analysis()
    
