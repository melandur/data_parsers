""" Analysis module for all kinds of experiments
"""

import os

import hydra
from loguru import logger
from omegaconf import DictConfig

from excel.global_helpers import checked_dir
from excel.analysis.utils.extract_data import ExtractData


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
    src_dir = config.dataset.raw_dir
    dst_dir = config.dataset.out_dir
    dims = config.dataset.dims

    localities = config.analysis.localities
    axes = config.analysis.axes
    orientations = config.analysis.orientations
    metrics = config.analysis.metrics
    peak_values = config.analysis.peak_values

    dir_name = checked_dir(dims)

    # TODO: might want to combine locality and dim to avoid polarmaps

    # TODO: train and test paths/sets
    logger.info('Extracting data according to config parameters...')
    extractor = ExtractData(
        src=os.path.join(src_dir, '4_checked', dir_name),
        dims=dims,
        localities=localities,
        axes=axes,
        orientations=orientations,
        metrics=metrics,
        peak_values=peak_values
    )
    data = extractor()
    logger.info('Data extraction finished.')

    
