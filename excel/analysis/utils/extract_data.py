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
        self.relevant = []
        self.table_name = None
        self.tables = {}

    def __call__(self) -> pd.DataFrame:
        # Identify relevant tables w.r.t. input parameters
        self.identify_tables()
        # Parse source directory to read in relevant tables
        subjects = os.listdir(self.src)
        for subject in subjects:
            for table in self.loop_files(subject):
                if self.peak_values:
                    table = self.remove_time(table)
                    self.extract_peak_values(table, subject)
                else:
                    logger.error('peak_values=False is not implemented yet.')

        tables = pd.DataFrame(self.tables)
        logger.debug(tables)

    def identify_tables(self) -> None:
        for locality in self.localities:
            for dim in self.dims:
                for axis in self.axes:
                    for orientation in self.orientations:
                        for metric in self.metrics:
                            self.relevant.append(
                                f'{locality}_{dim}_{axis}_{orientation}_{metric}')
        
    def loop_files(self, subject) -> pd.DataFrame:
            for root, _, files in os.walk(os.path.join(self.src, subject)):            
                for file in files:
                    # Consider only relevant tables
                    for table_name in self.relevant:
                        if file.endswith('.xlsx') and table_name in file:
                            logger.info(f'Relevant table {table_name} found.')
                            self.table_name = table_name
                            file_path = os.path.join(root, file)
                            table = pd.read_excel(file_path)
                            yield table

    def remove_time(self, table) -> None:
        return table[table.columns.drop(list(table.filter(regex='time')))]

    def extract_peak_values(self, table, subject) -> pd.DataFrame:
        # AHA data contain one info col, ROI data contains two info cols
        info_cols = 1 if 'aha' in self.table_name else 2

        # Circumferential and longitudinal strain and strain rate peak at minimum value
        if 'strain' in self.table_name and ('circumf' in self.table_name or 'longit' in self.table_name):
            # Compute peak values over sample cols
            peak = table.iloc[:, info_cols:].min(axis=1)
        
        else:
            peak = table.iloc[:, info_cols:].max(axis=1)

        # Merge info cols with peak values
        # table = pd.concat([table.iloc[:, :info_cols], peak], axis=1)
        # table.rename(columns={0: f'peak_{self.table_name}'}, inplace=True)
        self.tables[subject] = peak
