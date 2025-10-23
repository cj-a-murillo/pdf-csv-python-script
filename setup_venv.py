#!/usr/bin/env python3
"""
Quick Setup Script for PDF Table Extractor
Ensures all dependencies are installed in virtual environment only.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_virtual_env():
    """Check if we're running in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

def main():
    print("🔧 PDF Table Extractor - Virtual Environment Setup")
    print("=" * 55)
    
    # Check if in virtual environment
    if not check_virtual_env():
        print("❌ ERROR: Not running in virtual environment!")
        print("\n📋 Please run these commands first:")
        print("   python -m venv pdf_env")
        print("   # Windows:")
        print("   .\\pdf_env\\Scripts\\Activate.ps1")
        print("   # macOS/Linux:")
        print("   source pdf_env/bin/activate")
        print("\nThen run this script again.")
        return 1
    
    print("✅ Virtual environment detected")
    print(f"   Environment: {sys.prefix}")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return 1
    
    print("✅ Found requirements.txt")
    
    # Install packages in virtual environment
    try:
        print("\n📦 Installing Python packages in virtual environment...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ All Python packages installed successfully!")
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return 1
    
    # Check Java
    try:
        result = subprocess.run(["java", "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java is available")
        else:
            print("⚠️  Java not found - install Java 11+ for full functionality")
            print("   See JAVA_SETUP.md for installation instructions")
    except FileNotFoundError:
        print("⚠️  Java not found - install Java 11+ for full functionality")
        print("   See JAVA_SETUP.md for installation instructions")
    
    # Test imports
    print("\n🧪 Testing package imports...")
    try:
        import pandas
        print(f"✅ pandas {pandas.__version__}")
    except ImportError:
        print("❌ pandas import failed")
        return 1
    
    try:
        import tabula
        print("✅ tabula-py")
    except ImportError:
        print("❌ tabula-py import failed")
        return 1
    
    try:
        import jpype
        print(f"✅ jpype1 {jpype.__version__}")
    except ImportError:
        print("❌ jpype1 import failed")
        return 1
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("   1. Make sure Java is installed (if not already)")
    print("   2. Use activation scripts for convenience:")
    print("      .\\activate_env.ps1    (PowerShell)")
    print("      activate_env.bat       (Command Prompt)")
    print("   3. Run: python pdf-extract.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())