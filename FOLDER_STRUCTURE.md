# PDF Table Extractor - Folder Structure

## Overview
The script has been modified to use dedicated input and output folders for better organization.

## Folder Structure
```
pdf-csv-python-script/
├── pdf_input/          # Place your PDF files here
├── csv_output/         # CSV files will be saved here
├── pdf-extract.py      # Main script
├── requirements.txt    # Dependencies
└── FOLDER_STRUCTURE.md # This file
```

## How to Use

### 1. Prepare Your Files
- Place your PDF files in the `pdf_input/` folder
- The script will automatically detect PDF files in this folder

### 2. Run the Script

**Interactive Mode (Recommended):**
```bash
python pdf-extract.py
```
- Automatically searches `pdf_input/` folder
- Shows available PDF files for selection
- Saves CSV files to `csv_output/` folder

**Command Line Mode:**
```bash
python pdf-extract.py path/to/your/file.pdf
```
- Can specify PDF file path directly
- Still saves output to `csv_output/` folder

### 3. Find Your Results
- All CSV files will be saved in the `csv_output/` folder
- Files are named based on the original PDF filename
- Multiple tables get numbered suffixes (e.g., `document_table_1.csv`, `document_table_2.csv`)

## Benefits of This Structure
- ✅ Clean separation of input and output files
- ✅ Easy to organize multiple PDF processing tasks
- ✅ Prevents clutter in the main script directory
- ✅ Clear workflow: input → process → output