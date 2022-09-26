## Table of contents

- [quick-start](#quick-start)
- [dicom](#dicom)
- [excel](#excel)


## Quick start

    python = 3.9
    cd /path/to/this/repo
    poetry install

## Dicom

Tag based dicom file converter. 
Tags are not defined yet.


## Excel

#### 1. Pre-processing (to create basic data structure)
- workbook_2_sheets.py
- Sheets_2_tables.py
- cleaner.py
- checks.py

#### 2. Refinement (more specific data arrangement for faster plotting)
- calculate_accelerations.py
- table_condenser.py
- table_merger.py

#### 3. Analyze (ce plots)
- use jupyter notebook