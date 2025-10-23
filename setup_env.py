#!/usr/bin/env python3
"""
Environment Setup Script for PDF Table Extractor

This script helps set up the complete environment including Java for tabula-py.
"""

import os
import sys
import subprocess
import platform
import zipfile
import urllib.request
from pathlib import Path

def check_java():
    """Check if Java is available."""
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java is already installed and available")
            print(result.stderr.split('\n')[0])  # Java version info goes to stderr
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Java not found in system PATH")
    return False

def download_portable_java():
    """Download and setup portable Java."""
    java_dir = Path("java_portable")
    
    if java_dir.exists():
        print("✅ Portable Java directory already exists")
        return java_dir
    
    print("📥 Downloading portable Java...")
    
    # OpenJDK 11 portable for Windows (you might want to update this URL)
    if platform.system() == "Windows":
        java_url = "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_windows-x64_bin.zip"
        java_file = "openjdk-11.zip"
    else:
        print("❌ Portable Java setup currently only supports Windows")
        return None
    
    try:
        print(f"Downloading from: {java_url}")
        urllib.request.urlretrieve(java_url, java_file)
        
        print("📦 Extracting Java...")
        with zipfile.ZipFile(java_file, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Rename the extracted folder
        extracted_folders = [f for f in os.listdir(".") if f.startswith("jdk")]
        if extracted_folders:
            os.rename(extracted_folders[0], str(java_dir))
            print(f"✅ Java extracted to {java_dir}")
        
        # Clean up zip file
        os.remove(java_file)
        
        return java_dir
        
    except Exception as e:
        print(f"❌ Error downloading Java: {e}")
        return None

def setup_java_environment(java_dir):
    """Setup environment variables for Java."""
    if not java_dir or not java_dir.exists():
        return False
    
    java_home = java_dir.absolute()
    java_bin = java_home / "bin"
    
    # Create activation script for the environment
    activate_script = """@echo off
REM Activate PDF extraction environment with Java

REM Activate Python virtual environment
call "%~dp0pdf_env\\Scripts\\activate.bat"

REM Set Java environment
set JAVA_HOME={java_home}
set PATH={java_bin};%PATH%

echo.
echo ✅ PDF Extraction Environment Activated
echo ✅ Python: Virtual Environment
echo ✅ Java: Portable Installation
echo.
echo Usage:
echo   python pdf-extract.py
echo   python pdf-extract.py --help
echo.
""".format(java_home=java_home, java_bin=java_bin)
    
    with open("activate_env.bat", "w") as f:
        f.write(activate_script)
    
    # Create PowerShell activation script
    ps_activate_script = """# Activate PDF extraction environment with Java

# Activate Python virtual environment
& "$PSScriptRoot\\pdf_env\\Scripts\\Activate.ps1"

# Set Java environment
$env:JAVA_HOME = "{java_home}"
$env:PATH = "{java_bin};$env:PATH"

Write-Host ""
Write-Host "✅ PDF Extraction Environment Activated" -ForegroundColor Green
Write-Host "✅ Python: Virtual Environment" -ForegroundColor Green  
Write-Host "✅ Java: Portable Installation" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:"
Write-Host "  python pdf-extract.py"
Write-Host "  python pdf-extract.py --help"
Write-Host ""
""".format(java_home=java_home, java_bin=java_bin)
    
    with open("activate_env.ps1", "w") as f:
        f.write(ps_activate_script)
    
    print("✅ Environment activation scripts created:")
    print("   - activate_env.bat (Command Prompt)")
    print("   - activate_env.ps1 (PowerShell)")
    
    return True

def test_environment():
    """Test if the environment is working correctly."""
    print("\n🧪 Testing environment...")
    
    # Test Java
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java test passed")
        else:
            print("❌ Java test failed")
            return False
    except FileNotFoundError:
        print("❌ Java not found")
        return False
    
    # Test Python packages
    try:
        import pandas
        import tabula
        print("✅ Python packages test passed")
    except ImportError as e:
        print(f"❌ Python packages test failed: {e}")
        return False
    
    return True

def main():
    print("🔧 PDF Table Extractor - Environment Setup")
    print("=" * 50)
    
    # Check current directory
    if not Path("pdf-extract.py").exists():
        print("❌ Please run this script from the pdf-extract project directory")
        return 1
    
    # Check if virtual environment exists
    if not Path("pdf_env").exists():
        print("❌ Virtual environment not found. Please create it first:")
        print("   python -m venv pdf_env")
        return 1
    
    # Check Java
    java_available = check_java()
    
    if not java_available:
        print("\n🤔 Java is required for tabula-py. Options:")
        print("1. Install Java system-wide (recommended)")
        print("2. Download portable Java for this project")
        
        choice = input("\nChoose option (1 or 2): ").strip()
        
        if choice == "1":
            print("\n📋 To install Java system-wide:")
            print("1. Download from: https://adoptium.net/")
            print("2. Install the MSI/EXE package")
            print("3. Restart your terminal")
            print("4. Run this setup script again")
            return 0
            
        elif choice == "2":
            java_dir = download_portable_java()
            if java_dir:
                setup_java_environment(java_dir)
                print("\n✅ Portable Java setup complete!")
                print("\nTo use the environment:")
                print("  .\\activate_env.ps1    (PowerShell)")
                print("  activate_env.bat       (Command Prompt)")
            else:
                print("❌ Portable Java setup failed")
                return 1
        else:
            print("❌ Invalid choice")
            return 1
    else:
        print("✅ Java is available, creating activation scripts...")
        # Create activation scripts without portable Java
        activate_script = """@echo off
REM Activate PDF extraction environment

REM Activate Python virtual environment
call "%~dp0pdf_env\\Scripts\\activate.bat"

echo.
echo ✅ PDF Extraction Environment Activated
echo ✅ Python: Virtual Environment
echo ✅ Java: System Installation
echo.
echo Usage:
echo   python pdf-extract.py
echo   python pdf-extract.py --help
echo.
"""
        
        with open("activate_env.bat", "w") as f:
            f.write(activate_script)
        
        ps_activate_script = """# Activate PDF extraction environment

# Activate Python virtual environment
& "$PSScriptRoot\\pdf_env\\Scripts\\Activate.ps1"

Write-Host ""
Write-Host "✅ PDF Extraction Environment Activated" -ForegroundColor Green
Write-Host "✅ Python: Virtual Environment" -ForegroundColor Green  
Write-Host "✅ Java: System Installation" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:"
Write-Host "  python pdf-extract.py"
Write-Host "  python pdf-extract.py --help"
Write-Host ""
"""
        
        with open("activate_env.ps1", "w") as f:
            f.write(ps_activate_script)
        
        print("✅ Environment activation scripts created")
    
    print("\n🎉 Setup complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())