"""Data exploration module
"""

from loguru import logger
import pandas as pd
from omegaconf import DictConfig

from excel.analysis.utils import analyse_variables
from excel.analysis.utils import dim_reduction


class ExploreData:
    def __init__(self, data: pd.DataFrame, config: DictConfig) -> None:
        self.data = data
        self.out_dir = config.dataset.out_dir
        self.exploration = config.analysis.exploration
        self.remove_outliers = config.analysis.remove_outliers
        self.investigate_outliers = config.analysis.investigate_outliers
        self.whis = config.analysis.whis
        self.metadata = config.analysis.metadata
        self.seed = config.analysis.seed

    def __call__(self) -> None:
        # Detect (and optionally remove or investigate) outliers
        if self.remove_outliers or self.investigate_outliers:
            self.data = analyse_variables.detect_outliers(
                self.data,
                out_dir=self.out_dir,
                remove=self.remove_outliers,
                investigate=self.investigate_outliers,
                whis=self.whis,
                metadata=self.metadata,
            )

        for expl in self.exploration:
            logger.info(f'Performing {expl} data exploration for {len(self.data.index)} patients.')

            if expl == 'correlation':
                analyse_variables.correlation(self.data, self.out_dir, self.metadata)
                logger.info(f'{expl} data exploration finished.')
                continue

            try:
                stats_func = getattr(analyse_variables, expl)
                stats_func(self.data, self.out_dir, self.metadata, 'mace', self.whis)
                logger.info(f'{expl} data exploration finished.')
                continue
            except AttributeError:
                pass

            try:
                stats_func = getattr(dim_reduction, expl)
                stats_func(self.data, self.out_dir, self.metadata, 'mace', self.seed)
                logger.info(f'{expl} data exploration finished.')
                continue
            except AttributeError:
                raise NotImplementedError
