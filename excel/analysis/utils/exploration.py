"""Data exploration module
"""

import os

from loguru import logger
import pandas as pd

from excel.analysis.utils import statistics
from excel.analysis.utils import analyse_variables


class ExploreData:
    def __init__(self, data: pd.DataFrame, experiment: str, exploration: str, out_dir: str, \
        remove_meta: bool, metadata: list, whis: float=1.5) -> None:
        data[data['mace'] == 999] = 0
        self.data = data
        self.experiment = experiment
        self.exploration = exploration
        self.out_dir = out_dir
        self.remove_meta = remove_meta
        self.metadata = metadata
        self.whis = whis

    def __call__(self) -> None:
        # Remove meta data from plots if desired
        # if self.remove_meta:
        #     self.data = self.data.drop(self.metadata[:3], axis=1)
        
        # Detect (and optionally remove or investigate) outliers
        self.data = analyse_variables.detect_outliers(self.data, \
            out_dir=self.out_dir, investigate=True, whis=self.whis, metadata=self.metadata)

        for expl in self.exploration:
            logger.info(f'Performing {expl} data exploration.')
            
            stats_func = getattr(analyse_variables, expl)
            stats_func(self.data, self.out_dir, self.metadata, self.whis)

            logger.info(f'{expl} data exploration finished.')
