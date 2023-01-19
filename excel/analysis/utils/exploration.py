"""Data exploration module
"""

import os

from loguru import logger
import pandas as pd

from excel.analysis.utils import statistics
from excel.analysis.utils import variate_analysis


class ExploreData:
    def __init__(self, data: pd.DataFrame, experiment: str, exploration: str, out_dir: str, \
        remove_meta: bool, metadata: list) -> None:
        self.data = data
        self.experiment = experiment
        self.exploration = exploration
        self.out_dir = out_dir
        self.remove_meta = remove_meta
        self.metadata = metadata

    def __call__(self) -> None:
        for expl in self.exploration:
            logger.info(f'Performing {expl} data exploration.')
            # Remove meta data from plots if desired
            if self.remove_meta:
                self.data = self.data.drop(self.metadata[:3], axis=1)
            
            stats_func = getattr(variate_analysis, expl)
            stats_func(self.data, self.out_dir)

            logger.info(f'{expl} data exploration finished.')
