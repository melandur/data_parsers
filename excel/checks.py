import os
import shutil

from loguru import logger

from excel.path_master import CLEANED_PATH, CHECKED_PATH


class SplitByCompleteness:
    def __init__(self, src: str, dst: str) -> None:
        self.src = src
        self.dst = dst
        self.count = 0
        self.memory = {}
        self.complete_files = {}
        self.missing_files = {}

    def __call__(self) -> None:
        for case in self.get_cases():
            self.count_files(case)
            self.memory[case] = self.count
        self.divide_cases()
        self.move_files()

    def get_cases(self) -> str:
        """Get all cases from the cleaned folder"""
        cases = os.listdir(self.src)
        for case in cases:
            self.count = 0
            yield case

    def count_files(self, case: str) -> None:
        """Count the number of files in a case folder"""
        for _, _, files in os.walk(os.path.join(self.src, case)):
            for file in files:
                if file.endswith('.xlsx'):
                    self.count += 1

    def divide_cases(self) -> None:
        """Divide cases into complete and missing"""
        for case, counted_files in self.memory.items():
            if counted_files == 45:  # number of files in a complete case
                self.complete_files[case] = counted_files
            else:
                self.missing_files[case] = counted_files

    def move_files(self) -> None:
        """Move files to their destination folder"""
        logger.info('Copy complete cases')
        for case in self.complete_files:
            complete_file_path = os.path.join(self.dst, 'complete', case)
            os.makedirs(complete_file_path, exist_ok=True)
            shutil.copytree(os.path.join(self.src, case), complete_file_path, dirs_exist_ok=True)
            logger.info(f'-> {case}')

        logger.info('Copy missing cases')
        for case in self.missing_files:
            missing_file_path = os.path.join(self.dst, 'missing', case)
            os.makedirs(missing_file_path, exist_ok=True)
            shutil.copytree(os.path.join(self.src, case), missing_file_path, dirs_exist_ok=True)
            logger.info(f'-> {case}')


if __name__ == '__main__':
    src = CLEANED_PATH
    dst = CHECKED_PATH
    counter = SplitByCompleteness(src, dst)
    counter()
