import os
import pandas as pd
from loguru import logger

# TODO: ON HOLD
class RubiksCube:
    """Generic Table handler"""

    def __init__(self, src, dst, config) -> None:
        self.src = src
        self.dst = dst
        self.config = config
        self.memory = {}
        self.table_name = None

    def __call__(self) -> None:
        self.aggregate_data_frames()
        for _ in self.loop_tables():
            if self.config[self.table_name]['merge']:
                self.go_meta()
            else:
                self.run_sheet_wise()

    def aggregate_data_frames(self):
        logger.info(f'load data frames')
        for root, _, files in os.walk(self.src):
            for file in files:
                if file.endswith('.xlsx') and any(x in file for x in self.config):
                    file_path = os.path.join(root, file)
                    logger.info(f'-> {file}')
                    df = pd.read_excel(file_path)
                    file_name = file.replace('.xlsx', '')
                    self.memory[file_name] = df

    def loop_tables(self):
        for table_name in self.config:
            self.table_name = table_name
            logger.info('loop tables')
            yield table_name

    def run_sheet_wise(self):
        logger.info('run sheet wise')

        for subject, df in self.memory.items():
            for step in range(len(self.config[self.table_name]['row_name'])):
                print(step)

    def go_meta(self):
        logger.info('go meta')


if __name__ == '__main__':
    src = '/home/melandur/Data/Myocarditis/csv/train/newly'
    dst = '/home/melandur/Data/Myocarditis/csv/train/tmp'
    config = {
        'strain_rate': {
            'row_name': {
                '+': [['1']],
                '-': [['1']]},
            'column_name': {
                '+': [['1']],
                '-': [['1']]},
            'transpose': False,
            'name_by': 'row',
            'merge': False,
        }}

    rc = RubiksCube(src, dst, config)
    rc()
