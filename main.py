import os
import random
import sys
import json
from collections import defaultdict

import pydicom
import SimpleITK as sitk
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
            log_level: str,
    ) -> None:

        self.src = src
        self.dst = dst
        self.min_number_of_slices = min_number_of_slices
        self.file_types = file_types
        self.search_tags = search_tags
        self.exclude_tags = exclude_tags
        self.log_level = log_level
        self.path_memory = NestedDefaultDict()

    def __call__(self) -> None:
        logger.remove()
        logger.add(sys.stderr, level=self.log_level)
        self.scan_folder()
        self.convert_to_nifti()

    def export_meta_data_as_json(self, tags=None):
        """Iterate over the whole data and export data as json file"""
        for root, _, files in os.walk(self.src):
            for file in files:
                file_path = os.path.join(root, file)
                if self.check_file(file_path):
                    ds = pydicom.filereader.dcmread(file_path)
                    if tags:
                        print('')
                        for tag in tags:
                            print(ds.get(tag))
                    else:
                        print(ds)
                    break

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
                logger.trace(f'Check -> {key} : {ds.get(key)}')
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
        case_name = str(random.randint(0, 1000))
        for modality in self.search_tags:
            if self.check_tags(ds, modality):
                logger.info(f'found -> {modality} {file_path}')
                self.path_memory[case_name][modality] = file_path

    def check_file(self, file_path: str) -> bool:
        """Check found file for certain criteria"""
        check_1, check_2, check_3 = False, False, False
        if os.path.isfile(file_path) and self.check_file_type(file_path):  # exist and file type
            check_1 = True
        count_slices = len(os.listdir(os.path.dirname(file_path)))
        if not [x for x in self.exclude_tags if x in file_path]:  # exclude tags
            check_2 = True
        if count_slices >= self.min_number_of_slices:  # slice number
            check_3 = True
        return check_1 * check_2 * check_3

    def scan_folder(self) -> None:
        """Walk through the data set folder and assigns file paths to the nested dict"""
        for root, _, files in os.walk(self.src):
            for file in files:
                file_path = os.path.join(root, file)
                if self.check_file(file_path):
                    self.meta_data_search(file_path)
                    break  # no need to check every file in folder, break out of folder
        logger.info(f'Path memory -> {json.dumps(self.path_memory, indent=4)}')

    @staticmethod
    def dicom_sequence_reader(file_path: str) -> sitk.Image:
        """Reads data and meta data of dicom sequences"""
        reader = sitk.ImageSeriesReader()
        file_path = os.path.dirname(file_path)
        series_ids = reader.GetGDCMSeriesIDs(file_path)
        dicom_names = reader.GetGDCMSeriesFileNames(file_path, series_ids[0])
        reader.SetFileNames(dicom_names)
        img = reader.Execute()
        return img

    @logger.catch()
    def convert_to_nifti(self):
        """Convert path memory to nifti"""
        for case_name in self.path_memory:
            for modality in self.path_memory[case_name]:
                img = self.dicom_sequence_reader(self.path_memory[case_name][modality])
                dst_folder = os.path.join(self.dst, case_name)
                dst_folder = self.dst
                os.makedirs(dst_folder, exist_ok=True)
                sitk.WriteImage(img, os.path.join(dst_folder, f'{case_name}_{modality}.nii.gz'))


if __name__ == '__main__':
    dp = DicomParser(
        src='/home/melandur/Data/Myocarditis/M1',
        dst='/home/melandur/Downloads/test_me',
        min_number_of_slices=10,
        file_types=[''],
        search_tags={
            #         # 't1': {
            #         #     'ImageType': [['ORIGINAL'], ['PRIMARY'], ['MOCO']],
            #         #     'SequenceName': [['tf']],
            #         # },
            'flair': {
                'ImageType': [['ORIGINAL'], ['PRIMARY'], ['DIS2D']],
                'Modality': [['MR']],
                '': [['']],
                # 'ScanningSequence': [['SE']],
                # 'SequenceVariant': [['SK']],
                # 'ScanOptions': [['DB']],
                'MRAcquisitionType': [['2D']],
                'SequenceName': [['*tfi2d1_68']],

            }
        },
        exclude_tags=['DICOMDIR'],
        log_level='TRACE'
    )
    # dp()
    dp.export_meta_data_as_json(['ImageType', 'Modality', 'SequenceName'])
