# PDF Table Extractor

A Python script to extract tables from PDF files and convert them to CSV format.

## Features

- **Automatic PDF detection**: Automatically finds PDF files in the current directory
- **Multiple extraction methods**: Uses both `tabula-py` and `camelot-py` for robust table detection
- **Automatic method selection**: Tries different methods if one fails
- **Multiple output formats**: Saves single or multiple tables to CSV files
- **Preview functionality**: Preview tables before saving
- **Command-line interface**: Easy to use from command line
- **Interactive mode**: Run without arguments for guided extraction

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. **For Windows users**: You may also need to install Java for `tabula-py`:
   - Download and install Java from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.org/)
   - Make sure Java is in your PATH

3. **Optional**: For advanced table detection with `camelot-py`, uncomment the camelot lines in `requirements.txt` and install:
```bash
pip install camelot-py[cv] opencv-python
```

## Usage

### Command Line Usage

```bash
# Auto-detect PDF in current directory
python pdf-extract.py

# Auto-detect with preview
python pdf-extract.py --preview

# Specify a specific PDF file
python pdf-extract.py input.pdf

# Specify output file
python pdf-extract.py input.pdf output.csv

# Extract from specific pages
python pdf-extract.py input.pdf --pages "1,2,3"

# Preview tables before saving
python pdf-extract.py input.pdf --preview

# Use specific extraction method
python pdf-extract.py input.pdf --method tabula
python pdf-extract.py input.pdf --method camelot

# For camelot, specify detection flavor
python pdf-extract.py input.pdf --method camelot --flavor lattice
```

### Interactive Mode

Run without arguments for guided extraction with automatic PDF detection:
```bash
python pdf-extract.py
```

The script will:
1. Automatically find PDF files in the current directory
2. If multiple PDFs are found, let you choose which one to process
3. If only one PDF is found, use it automatically
4. If no PDFs are found, prompt you to enter a file path

### Programmatic Usage

```python
from pdf_extract import PDFTableExtractor

# Initialize extractor
extractor = PDFTableExtractor("document.pdf")

# Extract tables
tables = extractor.extract_tables()

# Preview tables
extractor.preview_tables(tables)

# Save to CSV
saved_files = extractor.save_tables_to_csv(tables, "output.csv")
```

## Automatic PDF Detection

The script now includes smart PDF file detection:

- **Single PDF**: Automatically uses the only PDF file in the current directory
- **Multiple PDFs**: Shows a list and lets you choose which one to process
- **No PDFs**: Falls back to asking for a file path
- **Manual override**: You can still specify a PDF file explicitly

### Examples

```bash
# Let the script find PDFs automatically
python pdf-extract.py

# Still works with explicit file paths
python pdf-extract.py my-document.pdf
```

## Extraction Methods

### Tabula-py
- Good for: Simple tables with clear structure
- Pros: Fast, reliable for well-formatted tables
- Cons: May miss complex or poorly formatted tables

### Camelot-py
- Good for: Complex tables, tables with merged cells
- Flavors:
  - `stream`: For tables without clear borders
  - `lattice`: For tables with clear borders and grid lines
- Pros: More accurate for complex layouts
- Cons: Slower, requires additional dependencies

## Output

- **Single table**: Saved as specified filename or `input_filename.csv`
- **Multiple tables**: Saved as `input_filename_table_1.csv`, `input_filename_table_2.csv`, etc.
- **CSV format**: Standard comma-separated values with headers

## Troubleshooting

### Common Issues

1. **"Java not found" error**:
   - Install Java and ensure it's in your PATH
   - Restart your terminal/command prompt

2. **No tables detected**:
   - Try different extraction methods (`--method tabula` or `--method camelot`)
   - Check if the PDF contains actual tables (not images of tables)
   - Try different pages (`--pages "1"` for first page only)

3. **Poor extraction quality**:
   - For camelot, try switching between `stream` and `lattice` flavors
   - The PDF might contain tables as images (requires OCR)

4. **Installation issues**:
   - Make sure you have Python 3.6+ installed
   - Try installing dependencies one by one
   - For camelot issues, check [their documentation](https://camelot-py.readthedocs.io/)

### Performance Tips

- For large PDFs, extract specific pages rather than all pages
- Use preview mode to check extraction quality before processing large files
- Start with tabula method as it's faster

## Examples

### Extract all tables from a PDF:
```bash
python pdf-extract.py report.pdf
```

### Extract tables from specific pages with preview:
```bash
python pdf-extract.py report.pdf --pages "2,3,4" --preview
```

### Use camelot for complex tables:
```bash
python pdf-extract.py complex_table.pdf --method camelot --flavor lattice
```

## Requirements

- Python 3.6+
- pandas
- tabula-py
- Java (for tabula-py)
- camelot-py[cv] (optional, for advanced detection)
- opencv-python (optional, for camelot)

## License

This script is provided as-is for educational and practical use.