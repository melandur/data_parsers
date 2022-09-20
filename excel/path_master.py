import os

DATA_PATH = '/home/melandur/Data/Myocarditis/csv/test/'

# Prepare data
RAW_PATH = os.path.join(DATA_PATH, '0_raw')
EXTRACTED_PATH = os.path.join(DATA_PATH, '1_extracted')
CASE_WISE_PATH = os.path.join(DATA_PATH, '2_case_wise')
CLEANED_PATH = os.path.join(DATA_PATH, '3_cleaned')
CHECKED_PATH = os.path.join(DATA_PATH, '4_checked')
TABLE_WISE_PATH = os.path.join(DATA_PATH, '5_table_wise')

# Analyze data
CONDENSED_PATH = os.path.join(DATA_PATH, '6_condensed')
MERGED_PATH = os.path.join(DATA_PATH, '7_merged')
AHA_SEGMENT_PATH = os.path.join(DATA_PATH, '8_aha_segment')

ANALYZE_PATH = os.path.join(DATA_PATH, '16_analyze')
TMP_PATH = os.path.join(DATA_PATH, '17_tmp')
