"""Data exploration module
"""

import os

from loguru import logger
import pandas as pd

from excel.analysis.utils import statistics


class ExploreData:
    def __init__(self, data: pd.DataFrame, experiment: str, exploration: str, out_dir: str) -> None:
        self.data = data
        self.experiment = experiment
        self.exploration = exploration
        self.out_dir = out_dir

    def __call__(self) -> None:
        for expl in self.exploration:
            logger.info(f'Performing {expl} data exploration.')
            
            stats_func = getattr(statistics, expl)
            stats_func(self.data, self.out_dir)

            logger.info(f'{expl} data exploration finished.')
