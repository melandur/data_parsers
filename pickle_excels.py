"""Class iterating over excel files and stores them in memory"""
"""Stores memory in nested dict"""

import os
import pandas as pd
import pickle


class Excels2Pickle:
    """Class iterating over excel files and stores them in memory"""
    """Stores memory in nested dict"""

    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.memory = {}

    def __call__(self) -> None:
        subjects = os.listdir(self.src)
        for subject in subjects:
            self.memory[subject] = {}
            for table in os.listdir(os.path.join(self.src, subject)):
                df = pd.read_excel(os.path.join(self.src, subject, table))
                self.memory[subject][table.replace('.xlsx', '')] = df

        with open(os.path.join(self.dst, 'clean_data.pkl'), 'wb') as f:
            pickle.dump(self.memory, f)

    def read_pickle(self) -> None:
        with open(os.path.join(self.dst, 'clean_data.pkl'), 'rb') as f:
            memory = pickle.load(f)

        print(memory)


if __name__ == '__main__':
    src = '/home/melandur/Data/Myocarditis/test_csv_processing_clean'
    dst = '/home/melandur/Data/Myocarditis/test_csv_processing_parquet'
    ep = Excels2Pickle(src, dst)
    # ep()
    ep.read_pickle()

