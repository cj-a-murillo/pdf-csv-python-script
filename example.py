#!/usr/bin/env python3
"""
Example usage of the PDF Table Extractor
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the PDFTableExtractor class from our main script
# Since the filename has a hyphen, we need to import it as a module
import importlib.util
import sys

def load_pdf_extractor():
    """Load the PDFTableExtractor class from pdf-extract.py"""
    spec = importlib.util.spec_from_file_location("pdf_extract", "pdf-extract.py")
    pdf_extract = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pdf_extract)
    return pdf_extract.PDFTableExtractor

# Load the class
PDFTableExtractor = load_pdf_extractor()

def example_usage():
    """Demonstrate various ways to use the PDF table extractor."""
    
    print("PDF Table Extractor - Example Usage")
    print("=" * 40)
    
    # Example 1: Basic extraction
    pdf_file = input("Enter path to a PDF file (or press Enter for demo): ").strip().strip('"')
    
    if not pdf_file:
        print("No PDF file provided. This example shows the code structure.")
        print("\nExample code:")
        print("""
# Basic usage
extractor = PDFTableExtractor("document.pdf")
tables = extractor.extract_tables()

# Preview the tables
extractor.preview_tables(tables)

# Save to CSV
saved_files = extractor.save_tables_to_csv(tables)
print(f"Saved {len(saved_files)} files: {saved_files}")
        """)
        return
    
    if not os.path.exists(pdf_file):
        print(f"File not found: {pdf_file}")
        return
    
    try:
        # Initialize extractor
        print(f"\nInitializing extractor for: {pdf_file}")
        extractor = PDFTableExtractor(pdf_file)
        
        # Example 2: Extract with specific method
        print("\nTrying automatic extraction...")
        tables = extractor.extract_tables(method='auto')
        
        if not tables:
            print("No tables found with automatic method.")
            return
        
        print(f"Found {len(tables)} table(s)")
        
        # Example 3: Preview tables
        print("\nPreviewing tables:")
        extractor.preview_tables(tables, max_rows=3)
        
        # Example 4: Save tables
        save_choice = input("\nSave tables to CSV? (y/n): ").lower().strip()
        if save_choice in ['y', 'yes']:
            saved_files = extractor.save_tables_to_csv(tables)
            print(f"\nSaved {len(saved_files)} file(s):")
            for file_path in saved_files:
                print(f"  - {file_path}")
        
        # Example 5: Extract from specific pages (if applicable)
        if len(tables) > 0:
            page_choice = input("\nTry extracting from page 1 only? (y/n): ").lower().strip()
            if page_choice in ['y', 'yes']:
                print("\nExtracting from page 1 only...")
                page1_tables = extractor.extract_tables(pages=[1])
                print(f"Found {len(page1_tables)} table(s) on page 1")
                if page1_tables:
                    extractor.preview_tables(page1_tables, max_rows=2)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install pandas tabula-py")

if __name__ == "__main__":
    example_usage()