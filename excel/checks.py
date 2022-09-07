import os
import shutil

from excel.path_master import CLEANED_PATH


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
                if file.endswith('.csv'):
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
        complete_file_path = os.path.join(self.dst, 'complete')
        os.makedirs(complete_file_path, exist_ok=True)
        for case in self.complete_files:
            shutil.move(os.path.join(self.src, case), complete_file_path)

        missing_file_path = os.path.join(self.dst, 'missing')
        os.makedirs(missing_file_path, exist_ok=True)
        for case in self.missing_files:
            shutil.move(os.path.join(self.src, case), missing_file_path)


if __name__ == '__main__':
    src = CLEANED_PATH
    dst = CLEANED_PATH
    counter = SplitByCompleteness(src, dst)
    counter()
