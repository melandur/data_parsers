"""Extracts data for desired experiment
"""

import os

from loguru import logger
import pandas as pd
import numpy as np


class MergeData:
    """Extracts data for given localities, dims, axes, orientations and metrics
    """

    def __init__(self, src: str, dims: list, segments: list, axes: list, \
        orientations: list, metrics: list, peak_values: bool=True) -> None:
        self.src = src
        self.dims = dims
        self.segments = segments
        self.axes = axes
        self.orientations = orientations
        self.metrics = metrics
        self.peak_values = peak_values
        self.relevant = []
        self.table_name = None

    def __call__(self) -> pd.DataFrame:
        tables_list = []
        # Identify relevant tables w.r.t. input parameters
        self.identify_tables()
        # Parse source directory to read in relevant tables
        subjects = os.listdir(self.src)
        for subject in subjects:
            self.col_names = [] # TODO: not necessary for each patient
            self.subject_data = []
            for table in self.loop_files(subject):
                if self.peak_values:
                    table = self.remove_time(table)
                    self.extract_peak_values(table)
                else:
                    logger.error('peak_values=False is not implemented yet.')
            tables_list.append(self.subject_data)

        tables = pd.DataFrame(tables_list, index=subjects, columns=self.col_names)
        return tables

    def identify_tables(self) -> None:
        for segment in self.segments:
            for dim in self.dims:
                for axis in self.axes:
                    for orientation in self.orientations:
                        # Skip impossible and imprecise combinations
                        if axis == 'short_axis' and orientation == 'longit' or \
                            axis == 'long_axis' and orientation == 'circumf' or \
                            axis == 'long_axis' and orientation == 'radial':
                            continue

                        for metric in self.metrics:
                            self.relevant.append(
                                f'{segment}_{dim}_{axis}_{orientation}_{metric}')
        
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

    def extract_peak_values(self, table) -> None:
        # AHA data contain one info col, ROI data contains two info cols
        info_cols = 1 if 'aha' in self.table_name else 2

        if 'roi' in self.table_name:
            # Ensure consistent naming between short and long axis
            if 'long_axis' in self.table_name:
                table = table.rename(columns={'series, slice': 'slice'})
            # Remove slice-wise global rows
            table.drop(table[(table.roi == 'global') & (table.slice != 'all slices')].index, inplace=True)
            # Keep only global, endo, epi ROI
            to_keep = ['global', 'endo', 'epi']
            table = table[table.roi.str.contains('global|endo|epi')==True]

        # Circumferential and longitudinal strain and strain rate peak at minimum value
        if 'strain' in self.table_name and ('circumf' in self.table_name or 'longit' in self.table_name):
            # Compute peak values over sample cols
            peak = table.iloc[:, info_cols:].min(axis=1)
        
        else:
            peak = table.iloc[:, info_cols:].max(axis=1)

        # Concat peak values to info cols
        table = pd.concat([table.iloc[:, :info_cols], peak], axis=1)

        # ROI analysis -> group by global/endo/epi
        if 'roi' in self.table_name:
            # Remove slice-wise global rows
            table = table.groupby(by='roi', sort=False).agg('mean', numeric_only=True)

        # Store column names for later
        for segment in to_keep:
            self.col_names.append(f'peak_{segment}_{self.table_name}')

        self.subject_data += list(table.iloc[:, 0])
