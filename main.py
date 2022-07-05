import os
from collections import defaultdict

import pydicom
from loguru import logger


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded on the fly"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self) -> str:
        return repr(dict(self))


class DicomParser:
    def __init__(
        self,
        src: str,
        dst: str,
        min_number_of_slices: int,
        file_types: list,
        search_tags: dict,
        exclude_tags: list,
    ) -> None:

        self.src = src
        self.dst = dst
        self.min_number_of_slices = min_number_of_slices
        self.file_types = file_types
        self.search_tags = search_tags
        self.exclude_tags = exclude_tags
        self.path_memory = NestedDefaultDict()

    def __call__(self) -> None:
        self.scan_folder()
        logger.info(self.path_memory)

    def check_file_type(self, file_name: str) -> bool:
        """True if file ends with defined file type"""
        if [x for x in self.file_types if file_name.endswith(x)]:
            return True
        return False

    def check_tags(self, ds: pydicom.filereader, modality: str) -> bool:
        """Return true in case one of each values for each key has a match"""
        counter = 0
        count_values = 0
        for key in self.search_tags[modality].keys():
            if ds.get(key):
                values = self.search_tags[modality][key]
                count_values += len(values)  # sum up multi tag statements
                for value in values:
                    if [x for x in value if x in ds.get(key)]:
                        counter += 1
        if counter == count_values and counter != 0:
            return True
        return False

    def meta_data_search(self, file_path: str) -> None:
        """Check meta data tags"""
        ds = pydicom.filereader.dcmread(file_path, force=True)
        case_name = ds.get('SOPClassUID')
        for modality in self.search_tags:
            if self.check_tags(ds, modality):
                logger.info(file_path)
                self.path_memory[case_name][modality] = file_path

    def check_file(self, file_path: str) -> bool:
        """Check found file for certain criteria"""
        check_1, check_2 = False, False
        if os.path.isfile(file_path) and self.check_file_type(file_path):
            check_1 = True
        count_slices = len(os.listdir(os.path.dirname(file_path)))
        if file_path not in self.exclude_tags and count_slices >= self.min_number_of_slices:
            check_2 = True
        return check_1 * check_2

    def scan_folder(self) -> None:
        """Walk through the data set folder and assigns file paths to the nested dict"""
        for root, _, files in os.walk(self.src):
            for file in files:
                file_path = os.path.join(root, file)
                if self.check_file(file_path):
                    self.meta_data_search(file_path)


if __name__ == '__main__':
    dp = DicomParser(
        src='/home/melandur/Data/Myocarditis/M1',
        dst='/home/Downloads/test_me',
        min_number_of_slices=0,
        file_types=[''],
        search_tags={
            't1': {
                'ImageType': [['MOCO']],
                'SequenceName': [['t']],
            }
            # 't2': {
            #     'key': {
            #         'tag_1': 'ImageType',
            #         'tag_2': 'SequenceName',
            #     },
            #     'value': {
            #         'tag_1': [['T2 MAP'], ['MOCO']],
            #         'tag_2': [['tfi']],
            #     },
            # },
        },
        exclude_tags=['DICOMDIR'],
    )
    dp()
