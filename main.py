import os
from collections import defaultdict

import pydicom


class NestedDefaultDict(defaultdict):
    """Nested dict, which can be dynamically expanded on the fly"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self) -> str:
        return repr(dict(self))


class DicomParser:

    def __init__(self, src: str, dst: str, file_types: list, search_tags: dict) -> None:
        self.src = src
        self.dst = dst
        self.file_types = file_types
        self.search_tags = search_tags
        self.path_memory = NestedDefaultDict()

    def __call__(self):
        self.scan_folder()

    def check_file_search_tag(self, file_name: str) -> bool:
        """True if search tag is in file name"""
        for value in self.search_tags.values():
            if [x for x in [*value] if x in file_name]:
                return True
        return False

    def check_file_type(self, file_name: str) -> bool:
        """True if file ends with defined file type"""
        if [x for x in self.file_types if file_name.endswith(x)]:
            return True
        return False

    def apply_filter(self):
        """Check meta data tags"""
        for modality in self.search_tags:
            for keys, values in self.search_tags[modality].items():
                for key in keys:
                    if ds[key]:
                        if [x for x in values if x in key]:
                            # self.path_memory
                            None

    def scan_folder(self) -> None:
        """Walk through the data set folder and assigns file paths to the nested dict"""
        for root, _, files in os.walk(self.src):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and self.check_file_type(file) and not '':
                    ds = pydicom.filereader.dcmread(file_path, force=True)
                    print(file_path)
                    # print(ds)
                    exit(0)
                    case_name = ds.get('SOPInstanceUID')
                    print(case_name)
                    # print(ds)

            # if self.validate_file(file, self.label_search_tags, self.label_file_type):
            #     found_tag = self.get_file_search_tag(file, self.label_search_tags)
            #     self.data_path_store['label'][self.get_case_name(root, file)][found_tag] = file_path
            # if self.validate_file(file, self.data_search_tags, self.data_file_type):
            #     found_tag = self.get_file_search_tag(file, self.data_search_tags)
            #     self.data_path_store['data'][self.get_case_name(root, file)][found_tag] = file_path


if __name__ == '__main__':
    dp = DicomParser(
        src='/home/melandur/Data/Graenni',
        dst='/home/Downloads/',
        file_types=['dcm', 'dicom', ''],
        search_tags={
            't1': {
                'key': ['adasdasdasda', 'adasdas'],
                'value': ['adasdasdasda', 'adasdas']},
            't1c': {
                'key': ['adasdasdasda', 'adasdas'],
                'value': ['adasdasdasda', 'adasdas']},
            't2': {
                'key': ['adasdasdasda', 'adasdas'],
                'value': ['adasdasdasda', 'adasdas']},
            'flair': {
                'key': ['adasdasdasda', 'adasdas'],
                'value': ['adasdasdasda', 'adasdas']},
        }
    )
    dp()
