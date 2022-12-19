import os

DATA_PATH = '/home/sebalzer/Documents/Mike_init/tests/train'

# Prepare data
RAW_PATH = os.path.join(DATA_PATH, '0_raw')
# Path suffix for testing purposes
SUFFIX = ''
EXTRACTED_PATH = os.path.join(DATA_PATH, '1_extracted' + SUFFIX)
CASE_WISE_PATH = os.path.join(DATA_PATH, '2_case_wise' + SUFFIX)
CLEANED_PATH = os.path.join(DATA_PATH, '3_cleaned' + SUFFIX)
CHECKED_PATH = os.path.join(DATA_PATH, '4_checked' + SUFFIX)
TABLE_WISE_PATH = os.path.join(DATA_PATH, '5_table_wise' + SUFFIX)

# Refine data
CONDENSED_PATH = os.path.join(DATA_PATH, '6_condensed' + SUFFIX)
MERGED_PATH = os.path.join(DATA_PATH, '7_merged' + SUFFIX)
AHA_SEGMENT_PATH = os.path.join(DATA_PATH, '8_aha_segment' + SUFFIX)

# Analyze data
ANALYZE_PATH = os.path.join(DATA_PATH, '16_analyze' + SUFFIX)
TMP_PATH = os.path.join(DATA_PATH, '17_tmp' + SUFFIX)
