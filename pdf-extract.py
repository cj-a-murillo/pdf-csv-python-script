#!/usr/bin/env python3
"""
PDF Table Extractor

This script extracts tables from PDF files and converts them to CSV format.
It supports multiple methods for table extraction to handle different types of PDFs.

Folder Structure:
- pdf_input/  - Place your PDF files here
- csv_output/ - CSV files will be saved here

Requirements:
- tabula-py
- pandas
- camelot-py[cv] (optional, for advanced table detection)
- PyPDF2 (fallback option)

Usage:
    python pdf-extract.py input.pdf output.csv
    python pdf-extract.py input.pdf  # Auto-generates output filename
    python pdf-extract.py            # Interactive mode - searches pdf_input folder
"""

import sys
import os
import argparse
import pandas as pd
from pathlib import Path
import glob

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False
    print("Warning: tabula-py not installed. Install with: pip install tabula-py")

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False
    print("Warning: camelot-py not installed. Install with: pip install camelot-py[cv]")


def find_pdf_files_in_directory(directory=None):
    """
    Find all PDF files in the specified directory.
    
    Args:
        directory: Directory to search (defaults to pdf_input folder)
    
    Returns:
        List of PDF file paths
    """
    if directory is None:
        # Default to pdf_input folder in the script's directory
        script_dir = Path(__file__).parent
        directory = script_dir / "pdf_input"
    
    pdf_pattern = os.path.join(directory, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    return [os.path.basename(f) for f in pdf_files]


def select_pdf_file_automatically():
    """
    Automatically select a PDF file from the pdf_input directory.
    
    Returns:
        Path to selected PDF file or None if no files found
    """
    pdf_files = find_pdf_files_in_directory()
    
    if not pdf_files:
        return None
    elif len(pdf_files) == 1:
        print(f"Found PDF file: {pdf_files[0]}")
        # Return full path to the file in pdf_input directory
        script_dir = Path(__file__).parent
        return str(script_dir / "pdf_input" / pdf_files[0])
    else:
        print(f"Found {len(pdf_files)} PDF files in pdf_input folder:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"  {i}. {pdf_file}")
        
        while True:
            try:
                choice = input(f"\nSelect a file (1-{len(pdf_files)}) or press Enter for first file: ").strip()
                if not choice:
                    selected = pdf_files[0]
                    print(f"Using: {selected}")
                    script_dir = Path(__file__).parent
                    return str(script_dir / "pdf_input" / selected)
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(pdf_files):
                    script_dir = Path(__file__).parent
                    return str(script_dir / "pdf_input" / pdf_files[choice_idx])
                else:
                    print(f"Please enter a number between 1 and {len(pdf_files)}")
            except ValueError:
                print("Please enter a valid number")


def get_pdf_file_path():
    """
    Get PDF file path with automatic detection fallback.
    
    Returns:
        Path to PDF file
    """
    # First try to find PDF files in pdf_input directory
    auto_pdf = select_pdf_file_automatically()
    
    if auto_pdf:
        return auto_pdf
    
    # If no PDF files found, ask user for input
    print("No PDF files found in pdf_input directory.")
    pdf_file = input("Enter PDF file path: ").strip().strip('"')
    return pdf_file if pdf_file else None


class PDFTableExtractor:
    """Extract tables from PDF files using multiple methods."""
    
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        
        # If the file doesn't exist, try looking in the pdf_input folder
        if not self.pdf_path.exists():
            script_dir = Path(__file__).parent
            pdf_input_path = script_dir / "pdf_input" / Path(pdf_path).name
            
            if pdf_input_path.exists():
                print(f"PDF file found in pdf_input folder: {pdf_input_path}")
                self.pdf_path = pdf_input_path
            else:
                raise FileNotFoundError(f"PDF file not found: {pdf_path}\nAlso checked: {pdf_input_path}")
    
    def extract_with_tabula(self, pages='all', multiple_tables=True):
        """
        Extract tables using tabula-py.
        
        Args:
            pages: Page numbers to extract from ('all' or list of page numbers)
            multiple_tables: Whether to extract multiple tables per page
        
        Returns:
            List of DataFrames containing extracted tables
        """
        if not TABULA_AVAILABLE:
            raise ImportError("tabula-py is required for this method")
        
        try:
            print(f"Extracting tables from {self.pdf_path} using tabula...")
            
            # Extract tables from PDF
            tables = tabula.read_pdf(
                str(self.pdf_path),
                pages=pages,
                multiple_tables=multiple_tables,
                pandas_options={'header': 0}
            )
            
            print(f"Found {len(tables)} table(s)")
            return tables
            
        except Exception as e:
            print(f"Error extracting with tabula: {e}")
            return []
    
    def extract_with_camelot(self, pages='all', flavor='stream', **camelot_kwargs):
        """
        Extract tables using camelot-py with enhanced column detection.
        
        Args:
            pages: Page numbers to extract from ('all' or '1,2,3')
            flavor: 'stream' or 'lattice' detection method
            **camelot_kwargs: Additional camelot parameters for fine-tuning
        
        Returns:
            List of DataFrames containing extracted tables
        """
        if not CAMELOT_AVAILABLE:
            raise ImportError("camelot-py is required for this method")
        
        try:
            print(f"Extracting tables from {self.pdf_path} using camelot ({flavor})...")
            
            # Enhanced parameters for better column detection
            default_params = {
                'pages': pages,
                'flavor': flavor
            }
            
            # Stream-specific optimizations for column detection
            if flavor == 'stream':
                stream_defaults = {
                    'table_areas': None,  # Let camelot auto-detect
                    'columns': None,      # Let camelot auto-detect columns
                    'split_text': False,  # Don't split text within cells
                    'strip_text': '\n',   # Remove newlines from cells
                    'row_tol': 2,        # Tolerance for row detection
                    'column_tol': 0      # Tolerance for column detection (0 = strict)
                }
                default_params.update(stream_defaults)
            
            # Lattice-specific optimizations
            elif flavor == 'lattice':
                lattice_defaults = {
                    'table_areas': None,     # Let camelot auto-detect
                    'process_background': False,  # Don't process background
                    'line_scale': 15,        # Line detection sensitivity
                    'copy_text': None,       # Text extraction method
                    'shift_text': [''],      # Text shifting rules
                    'split_text': False,     # Don't split text within cells
                    'strip_text': '\n'       # Remove newlines from cells
                }
                default_params.update(lattice_defaults)
            
            # Override with user-provided parameters
            default_params.update(camelot_kwargs)
            
            # Extract tables from PDF
            tables = camelot.read_pdf(str(self.pdf_path), **default_params)
            
            print(f"Found {len(tables)} table(s)")
            
            # Display detection confidence for debugging
            for i, table in enumerate(tables, 1):
                if hasattr(table, 'accuracy'):
                    print(f"  Table {i}: {table.shape[0]} rows × {table.shape[1]} columns (accuracy: {table.accuracy:.1f}%)")
                else:
                    print(f"  Table {i}: {table.df.shape[0]} rows × {table.df.shape[1]} columns")
            
            return [table.df for table in tables]
            
        except Exception as e:
            print(f"Error extracting with camelot: {e}")
            return []
    
    def extract_tables(self, method='auto', **kwargs):
        """
        Extract tables using the specified method.
        
        Args:
            method: 'tabula', 'camelot', or 'auto' to try both
            **kwargs: Additional arguments for extraction methods
        
        Returns:
            List of DataFrames containing extracted tables
        """
        tables = []
        
        if method == 'auto':
            # Try tabula first, then camelot
            if TABULA_AVAILABLE:
                tables = self.extract_with_tabula(**kwargs)
            
            if not tables and CAMELOT_AVAILABLE:
                print("Tabula didn't find tables, trying camelot...")
                # Try stream flavor first
                tables = self.extract_with_camelot(flavor='stream', **kwargs)
                
                # If stream didn't work well, try lattice
                if not tables:
                    print("Stream flavor didn't find tables, trying lattice...")
                    tables = self.extract_with_camelot(flavor='lattice', **kwargs)
                
        elif method == 'tabula':
            tables = self.extract_with_tabula(**kwargs)
            
        elif method == 'camelot':
            # Enhanced camelot extraction with both flavors if needed
            flavor = kwargs.get('flavor', 'stream')
            tables = self.extract_with_camelot(**kwargs)
            
            # If we got tables but they seem to have too few columns, try the other flavor
            if tables and flavor == 'stream':
                # Check if tables might be missing columns (heuristic)
                max_cols = max(table.shape[1] for table in tables)
                if max_cols <= 2:  # Suspiciously few columns
                    print(f"Only found {max_cols} column(s) with stream flavor, trying lattice...")
                    lattice_kwargs = kwargs.copy()
                    lattice_kwargs['flavor'] = 'lattice'
                    lattice_tables = self.extract_with_camelot(**lattice_kwargs)
                    
                    if lattice_tables:
                        lattice_max_cols = max(table.shape[1] for table in lattice_tables)
                        if lattice_max_cols > max_cols:
                            print(f"Lattice found {lattice_max_cols} column(s), using lattice results")
                            tables = lattice_tables
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return tables
    
    def generate_custom_filename(self, table_number, custom_suffix=None):
        """
        Generate custom filename for appropriations-donations tables.
        
        Args:
            table_number: Table number (1, 2, 3, etc.)
            custom_suffix: Optional custom suffix to add after the base name
        
        Returns:
            String filename in format: coa-2023--appropriations-donations_table<number>.csv
        """
        base_name = self.pdf_path.stem  # Gets 'coa-2023' from 'coa-2023.pdf'
        
        if custom_suffix:
            filename = f"{base_name}--{custom_suffix}_table{table_number}.csv"
        else:
            # Default naming for appropriations-donations
            filename = f"{base_name}--appropriations-donations_table{table_number}.csv"
            
        return filename
    
    def save_tables_to_csv(self, tables, output_path=None, prefix="table", custom_naming=False, custom_suffix=None):
        """
        Save extracted tables to CSV files in the csv_output folder.
        
        Args:
            tables: List of DataFrames
            output_path: Output file path (for single table) or directory (for multiple)
            prefix: Prefix for multiple table files (used when custom_naming=False)
            custom_naming: Use custom naming pattern (coa-2023--appropriations-donations_table<number>)
            custom_suffix: Custom suffix for naming pattern
        
        Returns:
            List of saved file paths
        """
        if not tables:
            print("No tables to save")
            return []
        
        # Get the script directory and csv_output folder
        script_dir = Path(__file__).parent
        csv_output_dir = script_dir / "csv_output"
        
        # Ensure csv_output directory exists
        csv_output_dir.mkdir(exist_ok=True)
        
        saved_files = []
        
        if len(tables) == 1:
            # Single table
            if output_path is None:
                if custom_naming:
                    output_filename = self.generate_custom_filename(1, custom_suffix)
                else:
                    output_filename = self.pdf_path.stem + '.csv'
                output_path = csv_output_dir / output_filename
            else:
                # If output_path is provided, put it in csv_output folder
                output_path = csv_output_dir / Path(output_path).name
            
            output_path = Path(output_path)
            tables[0].to_csv(output_path, index=False)
            saved_files.append(output_path)
            print(f"Table saved to: {output_path}")
            
        else:
            # Multiple tables - save to csv_output folder
            for i, table in enumerate(tables, 1):
                if custom_naming:
                    filename = self.generate_custom_filename(i, custom_suffix)
                else:
                    base_name = self.pdf_path.stem
                    filename = f"{base_name}_{prefix}_{i}.csv"
                    
                file_path = csv_output_dir / filename
                table.to_csv(file_path, index=False)
                saved_files.append(file_path)
                print(f"Table {i} saved to: {file_path}")
        
        return saved_files
    
    def preview_tables(self, tables, max_rows=5):
        """Preview extracted tables."""
        for i, table in enumerate(tables, 1):
            print(f"\n--- Table {i} Preview ---")
            print(f"Shape: {table.shape}")
            print(table.head(max_rows))
            if len(table) > max_rows:
                print(f"... ({len(table) - max_rows} more rows)")


def main():
    parser = argparse.ArgumentParser(description='Extract tables from PDF files to CSV')
    parser.add_argument('pdf_file', nargs='?', help='Input PDF file path (auto-detected if not provided)')
    parser.add_argument('output', nargs='?', help='Output CSV file or directory path')
    parser.add_argument('--method', choices=['tabula', 'camelot', 'auto'], 
                       default='auto', help='Extraction method to use')
    parser.add_argument('--pages', default='all', 
                       help='Pages to extract (e.g., "all", "1", "1,2,3")')
    parser.add_argument('--preview', action='store_true', 
                       help='Preview extracted tables before saving')
    parser.add_argument('--flavor', choices=['stream', 'lattice'], 
                       default='stream', help='Camelot detection flavor')
    parser.add_argument('--column-tol', type=int, default=0,
                       help='Camelot column tolerance (0=strict, higher=more lenient)')
    parser.add_argument('--row-tol', type=int, default=2,
                       help='Camelot row tolerance for stream flavor')
    parser.add_argument('--try-both-flavors', action='store_true',
                       help='Try both camelot flavors and use the one with more columns')
    
    # Custom naming options
    parser.add_argument('--custom-naming', action='store_true',
                       help='Use custom naming pattern: filename--appropriations-donations_table<number>')
    parser.add_argument('--custom-suffix', type=str, default='appropriations-donations',
                       help='Custom suffix for naming (default: appropriations-donations)')
    
    args = parser.parse_args()
    
    # Handle case where pages might be passed as second positional argument
    # This happens when users do: python script.py file.pdf "144,145,..."
    if args.output and args.pages == 'all':
        # Check if output looks like page numbers
        if ',' in args.output and args.output.replace(',', '').replace(' ', '').isdigit():
            print(f"Interpreting '{args.output}' as pages parameter")
            args.pages = args.output
            args.output = None
    
    # Get PDF file path - use provided argument or auto-detect
    pdf_file = args.pdf_file
    if not pdf_file:
        print("No PDF file specified. Looking for PDF files in pdf_input directory...")
        pdf_file = select_pdf_file_automatically()
        if not pdf_file:
            print("No PDF files found in pdf_input directory and none specified.")
            return 1
    
    try:
        # Initialize extractor
        extractor = PDFTableExtractor(pdf_file)
        
        # Prepare extraction parameters
        extract_params = {}
        if args.pages != 'all':
            if args.method in ['tabula', 'auto']:
                if ',' in args.pages:
                    extract_params['pages'] = [int(p.strip()) for p in args.pages.split(',')]
                else:
                    extract_params['pages'] = [int(args.pages)]
            else:  # camelot
                extract_params['pages'] = args.pages
        
        if args.method == 'camelot':
            extract_params['flavor'] = args.flavor
            extract_params['column_tol'] = args.column_tol
            extract_params['row_tol'] = args.row_tol
            
            if args.try_both_flavors:
                print("Trying both camelot flavors to maximize column detection...")
                # Try both flavors and pick the one with more columns
                stream_params = extract_params.copy()
                stream_params['flavor'] = 'stream'
                lattice_params = extract_params.copy()
                lattice_params['flavor'] = 'lattice'
                
                stream_tables = extractor.extract_with_camelot(**stream_params)
                lattice_tables = extractor.extract_with_camelot(**lattice_params)
                
                # Compare results
                stream_cols = max((t.shape[1] for t in stream_tables), default=0)
                lattice_cols = max((t.shape[1] for t in lattice_tables), default=0)
                
                if stream_cols >= lattice_cols:
                    print(f"Stream flavor found more columns ({stream_cols} vs {lattice_cols})")
                    tables = stream_tables
                else:
                    print(f"Lattice flavor found more columns ({lattice_cols} vs {stream_cols})")
                    tables = lattice_tables
            else:
                tables = extractor.extract_tables(method=args.method, **extract_params)
        else:
            # Extract tables
            tables = extractor.extract_tables(method=args.method, **extract_params)
        
        if not tables:
            print("No tables found in the PDF file.")
            return 1
        
        # Preview tables if requested
        if args.preview:
            extractor.preview_tables(tables)
            
            response = input("\nProceed with saving? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                print("Operation cancelled.")
                return 0
        
        # Save tables to CSV
        saved_files = extractor.save_tables_to_csv(
            tables, 
            args.output, 
            custom_naming=args.custom_naming, 
            custom_suffix=args.custom_suffix
        )
        
        print(f"\nSuccessfully extracted {len(tables)} table(s) to {len(saved_files)} CSV file(s)")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    # Check if running with arguments
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        # Interactive mode with auto-detection
        print("PDF Table Extractor")
        print("==================")
        print("Looking for PDF files in pdf_input folder...")
        print("CSV files will be saved to csv_output folder...")
        
        # Try to auto-detect PDF files first
        pdf_file = get_pdf_file_path()
        
        if not pdf_file:
            print("No file specified. Exiting.")
            sys.exit(1)
        
        try:
            extractor = PDFTableExtractor(pdf_file)
            tables = extractor.extract_tables()
            
            if tables:
                extractor.preview_tables(tables)
                
                save = input("\nSave tables to CSV? (y/n): ").lower().strip()
                if save in ['y', 'yes']:
                    # In interactive mode, default to custom naming for appropriations-donations
                    saved_files = extractor.save_tables_to_csv(
                        tables, 
                        custom_naming=True, 
                        custom_suffix='appropriations-donations'
                    )
                    print(f"Saved {len(saved_files)} CSV file(s)")
            else:
                print("No tables found in the PDF.")
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
