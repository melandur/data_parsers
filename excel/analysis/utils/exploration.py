"""Data exploration module
"""

import os

from loguru import logger


class ExploreData:
    def __init__(self, src: str, experiment: str, exploration: str) -> None:
        self.src = src
        self.experiment = experiment
        self.exploration = exploration

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass