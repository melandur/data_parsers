"""Extracts data for desired experiment
"""

import os

from loguru import logger
import pandas as pd


class ExtractData:
    """Extracts data for given localities, dims, axes, orientations and metrics
    """

    def __init__(self, src: str, dims: list, localities: list, axes: list, \
        orientations: list, metrics: list, peak_values: bool=True) -> None:
        self.src = src
        self.dims = dims
        self.localities = localities
        self.axes = axes
        self.orientations = orientations
        self.metrics = metrics
        self.peak_values = peak_values

    def __call__(self) -> pd.DataFrame:
        pass