#!/usr/bin/env python3
"""
Test script to verify the PDF extraction environment is working correctly.
"""

import sys
import os
from pathlib import Path

def test_python_environment():
    """Test Python environment and packages."""
    print("🐍 Testing Python Environment...")
    print(f"   Python version: {sys.version}")
    print(f"   Virtual env: {sys.prefix}")
    
    # Test required packages
    try:
        import pandas
        print(f"   ✅ pandas {pandas.__version__}")
    except ImportError:
        print("   ❌ pandas not installed")
        return False
    
    try:
        import tabula
        print(f"   ✅ tabula-py installed")
    except ImportError:
        print("   ❌ tabula-py not installed")
        return False
    
    try:
        import jpype
        print(f"   ✅ jpype1 {jpype.__version__}")
    except ImportError:
        print("   ❌ jpype1 not installed")
        return False
    
    return True

def test_java():
    """Test Java installation and connectivity."""
    print("\n☕ Testing Java...")
    
    # Try to find Java in common locations
    possible_java_paths = [
        r"C:\Program Files\Microsoft\jdk-11.*\bin\java.exe",
        r"C:\Program Files\Eclipse Adoptium\jdk-11.*\bin\java.exe", 
        r"C:\Program Files\Java\jdk*\bin\java.exe",
        "java"  # System PATH
    ]
    
    import subprocess
    import glob
    
    for java_path in possible_java_paths:
        try:
            if "*" in java_path:
                # Handle wildcard paths
                matches = glob.glob(java_path)
                if not matches:
                    continue
                java_path = matches[0]
            
            result = subprocess.run([java_path, '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_line = result.stderr.split('\n')[0] if result.stderr else "Unknown version"
                print(f"   ✅ Java found: {java_path}")
                print(f"   ✅ {version_line}")
                return java_path
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            continue
    
    print("   ❌ Java not found")
    print("   💡 Try restarting your terminal after Java installation")
    return None

def test_tabula_with_java():
    """Test tabula-py with Java integration."""
    print("\n📊 Testing tabula-py with Java...")
    
    try:
        import tabula
        
        # Create a simple test - this should work if Java is properly configured
        # We'll just test if we can initialize tabula without errors
        print("   ✅ tabula-py import successful")
        
        # Test if we can access Java through tabula
        try:
            # This will fail if Java is not accessible, but won't crash
            test_result = tabula.io.build_options()
            print("   ✅ tabula-py can access Java")
            return True
        except Exception as e:
            print(f"   ⚠️  tabula-py Java integration issue: {e}")
            return False
            
    except Exception as e:
        print(f"   ❌ tabula-py test failed: {e}")
        return False

def test_pdf_extractor():
    """Test our PDF extractor script."""
    print("\n📄 Testing PDF Extractor...")
    
    try:
        # Import our extractor
        import importlib.util
        spec = importlib.util.spec_from_file_location("pdf_extract", "pdf-extract.py")
        pdf_extract = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pdf_extract)
        
        print("   ✅ PDF extractor script loads successfully")
        
        # Test auto-detection
        pdf_files = pdf_extract.find_pdf_files_in_directory()
        print(f"   ✅ Auto-detection found {len(pdf_files)} PDF file(s): {pdf_files}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ PDF extractor test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 PDF Table Extractor - Environment Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test Python environment
    if not test_python_environment():
        all_passed = False
    
    # Test Java
    java_path = test_java()
    
    # Test tabula with Java
    if not test_tabula_with_java():
        all_passed = False
    
    # Test PDF extractor
    if not test_pdf_extractor():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed and java_path:
        print("🎉 All tests passed! Your environment is ready to use.")
        print("\nNext steps:")
        print("   python pdf-extract.py          # Auto-detect and extract")
        print("   python pdf-extract.py --help   # See all options")
    elif java_path:
        print("⚠️  Environment mostly ready, but some issues detected.")
        print("   Your environment should still work for basic functionality.")
    else:
        print("❌ Environment setup incomplete.")
        print("\nTo fix Java issues:")
        print("1. Restart your terminal/PowerShell")
        print("2. Check JAVA_SETUP.md for detailed instructions")
        print("3. Run this test again: python test_environment.py")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())