#!/usr/bin/env python3
"""
PDF Table Extractor

This script extracts tables from PDF files and converts them to CSV format.
It supports multiple methods for table extraction to handle different types of PDFs.

Requirements:
- tabula-py
- pandas
- camelot-py[cv] (optional, for advanced table detection)
- PyPDF2 (fallback option)

Usage:
    python pdf-extract.py input.pdf output.csv
    python pdf-extract.py input.pdf  # Auto-generates output filename
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
        directory: Directory to search (defaults to current directory)
    
    Returns:
        List of PDF file paths
    """
    if directory is None:
        directory = os.getcwd()
    
    pdf_pattern = os.path.join(directory, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    return [os.path.basename(f) for f in pdf_files]


def select_pdf_file_automatically():
    """
    Automatically select a PDF file from the current directory.
    
    Returns:
        Path to selected PDF file or None if no files found
    """
    pdf_files = find_pdf_files_in_directory()
    
    if not pdf_files:
        return None
    elif len(pdf_files) == 1:
        print(f"Found PDF file: {pdf_files[0]}")
        return pdf_files[0]
    else:
        print(f"Found {len(pdf_files)} PDF files:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"  {i}. {pdf_file}")
        
        while True:
            try:
                choice = input(f"\nSelect a file (1-{len(pdf_files)}) or press Enter for first file: ").strip()
                if not choice:
                    selected = pdf_files[0]
                    print(f"Using: {selected}")
                    return selected
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(pdf_files):
                    return pdf_files[choice_idx]
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
    # First try to find PDF files in current directory
    auto_pdf = select_pdf_file_automatically()
    
    if auto_pdf:
        return auto_pdf
    
    # If no PDF files found, ask user for input
    print("No PDF files found in current directory.")
    pdf_file = input("Enter PDF file path: ").strip().strip('"')
    return pdf_file if pdf_file else None


class PDFTableExtractor:
    """Extract tables from PDF files using multiple methods."""
    
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
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
    
    def extract_with_camelot(self, pages='all', flavor='stream'):
        """
        Extract tables using camelot-py.
        
        Args:
            pages: Page numbers to extract from ('all' or '1,2,3')
            flavor: 'stream' or 'lattice' detection method
        
        Returns:
            List of DataFrames containing extracted tables
        """
        if not CAMELOT_AVAILABLE:
            raise ImportError("camelot-py is required for this method")
        
        try:
            print(f"Extracting tables from {self.pdf_path} using camelot ({flavor})...")
            
            # Extract tables from PDF
            tables = camelot.read_pdf(str(self.pdf_path), pages=pages, flavor=flavor)
            
            print(f"Found {len(tables)} table(s)")
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
                tables = self.extract_with_camelot(**kwargs)
                
        elif method == 'tabula':
            tables = self.extract_with_tabula(**kwargs)
            
        elif method == 'camelot':
            tables = self.extract_with_camelot(**kwargs)
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return tables
    
    def save_tables_to_csv(self, tables, output_path=None, prefix="table"):
        """
        Save extracted tables to CSV files.
        
        Args:
            tables: List of DataFrames
            output_path: Output file path (for single table) or directory (for multiple)
            prefix: Prefix for multiple table files
        
        Returns:
            List of saved file paths
        """
        if not tables:
            print("No tables to save")
            return []
        
        saved_files = []
        
        if len(tables) == 1:
            # Single table
            if output_path is None:
                output_path = self.pdf_path.with_suffix('.csv')
            
            output_path = Path(output_path)
            tables[0].to_csv(output_path, index=False)
            saved_files.append(output_path)
            print(f"Table saved to: {output_path}")
            
        else:
            # Multiple tables
            if output_path is None:
                output_dir = self.pdf_path.parent
                base_name = self.pdf_path.stem
            else:
                output_path = Path(output_path)
                if output_path.is_dir():
                    output_dir = output_path
                    base_name = self.pdf_path.stem
                else:
                    output_dir = output_path.parent
                    base_name = output_path.stem
            
            for i, table in enumerate(tables, 1):
                filename = f"{base_name}_{prefix}_{i}.csv"
                file_path = output_dir / filename
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
    
    args = parser.parse_args()
    
    # Get PDF file path - use provided argument or auto-detect
    pdf_file = args.pdf_file
    if not pdf_file:
        print("No PDF file specified. Looking for PDF files in current directory...")
        pdf_file = select_pdf_file_automatically()
        if not pdf_file:
            print("No PDF files found and none specified.")
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
        saved_files = extractor.save_tables_to_csv(tables, args.output)
        
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
                    saved_files = extractor.save_tables_to_csv(tables)
                    print(f"Saved {len(saved_files)} CSV file(s)")
            else:
                print("No tables found in the PDF.")
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)