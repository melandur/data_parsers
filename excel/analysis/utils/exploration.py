"""Data exploration module
"""

import os

from loguru import logger
import pandas as pd

from excel.analysis.utils import statistics
from excel.analysis.utils import analyse_variables
from excel.analysis.utils import dim_reduction


class ExploreData:
    def __init__(self, data: pd.DataFrame, experiment: str, exploration: str, out_dir: str, \
        metadata: list, remove_outliers: bool=False, investigate_outliers: bool=False, \
        whis: float=1.5, seed: int=0) -> None:
        # Correct some mace entries
        data[data['mace'] == 999] = 0

        self.data = data
        self.experiment = experiment
        self.exploration = exploration
        self.out_dir = out_dir
        self.metadata = metadata
        self.remove_outliers = remove_outliers
        self.investigate_outliers = investigate_outliers
        self.whis = whis
        self.seed = seed

    def __call__(self) -> None:        
        # Detect (and optionally remove or investigate) outliers
        self.data = analyse_variables.detect_outliers(self.data, \
            out_dir=self.out_dir, remove=self.remove_outliers, \
            investigate=self.investigate_outliers, whis=self.whis, \
            metadata=self.metadata)

        for expl in self.exploration:
            logger.info(f'Performing {expl} data exploration.')
            
            try:
                stats_func = getattr(analyse_variables, expl)
                stats_func(self.data, self.out_dir, self.metadata, self.whis)
                logger.info(f'{expl} data exploration finished.')
                continue
            except AttributeError:
                pass

            try:
                stats_func = getattr(dim_reduction, expl)
                stats_func(self.data, self.out_dir, self.metadata, self.seed)
                logger.info(f'{expl} data exploration finished.')
                continue
            except AttributeError:
                raise NotImplementedError