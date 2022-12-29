""" Pre-processing module with the ability to extract excel files ready for data analysis
    from raw civ42 data excel files
"""

import os

import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf

from excel.pre_processing.utils.workbook_2_sheets import ExtractWorkbook2Sheets
from excel.pre_processing.utils.sheets_2_tables import ExtractSheets2Tables
from excel.pre_processing.utils.cleaner import TableCleaner
from excel.pre_processing.utils.checks import SplitByCompleteness


@hydra.main(version_base=None, config_path='../../config', config_name='config')
def pre_processing(config: DictConfig) -> None:
    """Pre-processing pipeline

    Args:
        config (DictConfig): config element containing all config parameters
            check the config files for info on the individual parameters

    Returns:
        None
    """
    # Parse some config parameters
    src_dir = config.dataset.raw_dir
    dst_dir = config.dataset.out_dir
    save_intermediate = config.dataset.save_intermediate
    dims = config.dataset.dims

    if save_intermediate:
        logger.info('Intermediate results will be saved between each pre-processing step.')
        dst = os.path.join(dst_dir, '1_extracted')
    else:
        dst = os.path.join(dst_dir, '9_final')

    # Extract one sheet per patient from the available raw workbooks
    # additionally removes any colour formatting
    sheets = {}
    # for src_file in os.listdir(src_dir):
    for src_file in [os.path.join(src_dir, 'D. Strain_v3b_FlamBer_61-120.xlsx')]:
        if src_file.endswith('.xlsx') and not src_file.startswith('.'):
            logger.info(f'File -> {src_file}')
            workbook_2_sheets = ExtractWorkbook2Sheets(
                src=os.path.join(src_dir, src_file),
                dst=dst,
                save_intermediate=save_intermediate
            )
            sheets = sheets | workbook_2_sheets()

    if save_intermediate: # update paths
        src_dir = dst
        dst = os.path.join(dst_dir, '2_case_wise')

    sheets_2_tables = ExtractSheets2Tables(
        src=src_dir,
        dst=dst,
        save_intermediate=save_intermediate,
        sheets=sheets
    )
    tables = sheets_2_tables()
    # print(tables["31"]['2d']['global_roi_2d_short_axis_radial_strain_(%)'].iloc[:10, :8])

    if save_intermediate:
        src_dir = dst
        dst = os.path.join(dst_dir, '3_cleaned')

    cleaner = TableCleaner(
        src=src_dir,
        dst=dst,
        save_intermediate=save_intermediate,
        dims=dims,
        tables=tables
    )
    clean_tables = cleaner()
    # print(clean_tables["31"]['2d']['global_roi_2d_short_axis_radial_strain_(%)'].iloc[:10, :8])

    if save_intermediate:
        src_dir = dst
        dst = os.path.join(dst_dir, '4_checked')

    checker = SplitByCompleteness(
        src=src_dir,
        dst=dst,
        save_intermediate=save_intermediate,
        dims=dims,
        tables=clean_tables
    )
    complete_tables = checker()
    # print(complete_tables["31"]['2d']['global_roi_2d_short_axis_radial_strain_(%)'].iloc[:10, :8])


if __name__ == '__main__':
    pre_processing()