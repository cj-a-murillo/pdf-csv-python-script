# PDF Table Extractor 📊

A Python tool that automatically extracts tables from PDF files and converts them to CSV format. Features smart PDF detection, multiple extraction methods, and a complete virtual environment setup.

## 📑 Table of Contents

- [⚡ Quick Start](#-quick-start-5-commands)
- [🚀 Complete Setup Guide](#-complete-setup-guide-start-to-finish)
- [💡 Real-World Usage Examples](#-real-world-usage-examples)
- [🚨 Common Issues & Quick Fixes](#-common-issues--quick-fixes)
- [📋 Command Reference Card](#-command-reference-card)

## ⚡ Quick Start (5 Commands)

```bash
git clone <your-repo-url> && cd python-pdf-extract
python -m venv pdf_env
.\pdf_env\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt
python pdf-extract.py              # Extract tables!
```

> **Note**: Install Java 11+ for full functionality: `winget install Microsoft.OpenJDK.11`

## ✨ Features

- **🔍 Automatic PDF Detection**: Finds PDF files in the current directory automatically
- **🔄 Multiple Extraction Methods**: Uses both `tabula-py` and `camelot-py` for robust table detection
- **🎯 Smart Method Selection**: Tries different methods if one fails
- **📁 Multiple Output Formats**: Saves single or multiple tables to CSV files
- **👀 Preview Functionality**: Preview tables before saving
- **💻 Command-Line Interface**: Easy to use from command line
- **🖱️ Interactive Mode**: Run without arguments for guided extraction
- **🌐 Virtual Environment**: Complete isolated setup with Java integration

## � TL;DR - Just Want to Extract Tables?

1. **One-time setup**: `git clone repo → python -m venv pdf_env → activate → pip install -r requirements.txt`
2. **Every time**: `activate virtual environment → python pdf-extract.py`
3. **That's it!** CSV files are created automatically from any PDF tables found.

## �🚀 Complete Setup Guide (Start to Finish)

### 📋 **Prerequisites**
- Python 3.6+ installed on your system
- Git (to clone the repository)
- Internet connection (for downloading dependencies)

### 🔧 **Step-by-Step Setup**

#### Step 1: Get the Code
```bash
# Clone the repository
git clone <your-repo-url>
cd python-pdf-extract

# Or download and extract the ZIP file
```

#### Step 2: Create Virtual Environment
```bash
# Create isolated Python environment
python -m venv pdf_env

# Verify creation
ls pdf_env/          # macOS/Linux
dir pdf_env\         # Windows
```

#### Step 3: Activate Virtual Environment
```bash
# Windows PowerShell
.\pdf_env\Scripts\Activate.ps1

# Windows Command Prompt
pdf_env\Scripts\activate.bat

# macOS/Linux
source pdf_env/bin/activate

# You should see (pdf_env) in your terminal prompt
```

#### Step 4: Install Python Dependencies
```bash
# Install all required packages in virtual environment
pip install -r requirements.txt

# Verify installation
pip list
```

#### Step 5: Install Java (Required for PDF Processing)
```bash
# Windows (using Windows Package Manager)
winget install Microsoft.OpenJDK.11

# macOS (using Homebrew)
brew install openjdk@11

# Ubuntu/Debian Linux
sudo apt install openjdk-11-jdk

# Manual installation: Download from https://adoptium.net/
```

#### Step 6: Verify Setup
```bash
# Test the complete environment
python setup_venv.py

# Should show all green checkmarks ✅
```

#### Step 7: Set Up Convenient Activation (Optional)
```bash
# The activation scripts handle both Python and Java setup
# Windows PowerShell users:
.\activate_env.ps1

# Windows Command Prompt users:
activate_env.bat

# macOS/Linux users: Use standard activation + set JAVA_HOME
```

### 🎯 **Daily Usage**

#### Every Time You Want to Use the Tool:
```bash
# 1. Navigate to project directory
cd python-pdf-extract

# 2. Activate environment (choose one)
.\pdf_env\Scripts\Activate.ps1    # Windows PowerShell
pdf_env\Scripts\activate.bat      # Windows Command Prompt
source pdf_env/bin/activate       # macOS/Linux

# 3. Use the tool (see commands below)
```

#### Basic Commands:
```bash
# Auto-detect PDF files in current directory and extract tables
python pdf-extract.py

# Extract from specific PDF file
python pdf-extract.py document.pdf

# Preview tables before saving
python pdf-extract.py --preview

# Extract from specific pages only
python pdf-extract.py document.pdf --pages "1,2,3"

# Use advanced extraction method
python pdf-extract.py --method camelot

# Show all available options
python pdf-extract.py --help
```

#### Test Your Setup:
```bash
# Verify everything is working
python test_environment.py

# Check what packages are installed
pip list
```

## 📋 Requirements

- **Python 3.6+** (system installation)
- **Java 11+** (system installation for tabula-py)
- **All Python packages installed in virtual environment** (isolated from system)
- Windows, macOS, or Linux

## 🏗️ Alternative Setup Methods

### Method 1: Quick Automated Setup
```bash
# After cloning and creating virtual environment
python -m venv pdf_env
.\pdf_env\Scripts\Activate.ps1  # or appropriate activation command
python setup_venv.py            # Handles everything automatically
```

### Method 2: Manual Step-by-Step (Recommended for Learning)
See the "Complete Setup Guide" above for detailed manual steps.

### Method 3: Advanced Setup with Java Detection
```bash
python -m venv pdf_env
.\pdf_env\Scripts\Activate.ps1
python setup_env.py  # More comprehensive setup with Java detection
```

## 📦 What's Included

- `pdf-extract.py` - Main extraction script
- `activate_env.ps1/bat` - Environment activation scripts
- `setup_env.py` - Automated environment setup
- `test_environment.py` - Environment verification
- `requirements.txt` - Python dependencies
- Complete documentation and guides

## 💡 Real-World Usage Examples

### Scenario 1: First Time User
```bash
# Day 1: Setup (one time only)
git clone <your-repo-url>
cd python-pdf-extract
python -m venv pdf_env
.\pdf_env\Scripts\Activate.ps1
pip install -r requirements.txt
winget install Microsoft.OpenJDK.11

# Day 1: First extraction
python pdf-extract.py
# Output: Found PDF file: report.pdf
# Output: Table saved to: report.csv
```

### Scenario 2: Daily Usage
```bash
# Every other day: Quick start
cd python-pdf-extract
.\pdf_env\Scripts\Activate.ps1
python pdf-extract.py --preview
# Preview tables, then save
```

### Scenario 3: Batch Processing
```bash
# Process multiple PDFs
.\pdf_env\Scripts\Activate.ps1
python pdf-extract.py report1.pdf
python pdf-extract.py report2.pdf --pages "2,3"
python pdf-extract.py financial_data.pdf --method camelot
```

### Scenario 4: Troubleshooting
```bash
# When things don't work
.\pdf_env\Scripts\Activate.ps1
python test_environment.py  # Check what's broken
pip install --force-reinstall -r requirements.txt  # Fix packages
java -version  # Check Java
```

## 🔧 Environment Setup Details

This project uses a **completely isolated virtual environment** to avoid conflicts with your system Python installation:

### 🎯 **Virtual Environment Benefits:**
- **No System Pollution**: All packages installed only in project environment
- **Dependency Isolation**: No conflicts with other Python projects  
- **Easy Cleanup**: Delete `pdf_env/` folder to remove everything
- **Reproducible Setup**: Same environment on any machine

### 📦 **What Gets Installed Where:**

**System Level (Required):**
- Python 3.6+ interpreter
- Java 11+ JDK (for tabula-py PDF processing)

**Virtual Environment Only:**
- `pandas` - Data manipulation
- `tabula-py` - PDF table extraction  
- `jpype1` - Java-Python bridge
- `camelot-py[cv]` - Advanced table detection (optional)
- `opencv-python` - Image processing for camelot (optional)

### 🔄 **Environment Activation:**

The activation scripts (`activate_env.ps1` / `activate_env.bat`) automatically:
1. Activate the Python virtual environment  
2. Set `JAVA_HOME` environment variable
3. Add Java to `PATH` for current session
4. Verify all components are working

### ✅ **Verification:**

```bash
# Test your setup
python test_environment.py

# Should show:
# ✅ Python: Virtual Environment  
# ✅ Java: System Installation
# ✅ All packages: Available in virtual environment
```

## 📚 Documentation

- `README.md` - This file
- `JAVA_SETUP.md` - Detailed Java installation guide
- `SUMMARY.md` - Project architecture and features
- `requirements.txt` - Python package dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and practical use.

## � Common Issues & Quick Fixes

### ❌ "Virtual environment not activated"
```bash
# You'll see this error: ModuleNotFoundError: No module named 'pandas'
# Fix: Always activate first
.\pdf_env\Scripts\Activate.ps1  # Windows
source pdf_env/bin/activate     # macOS/Linux
```

### ❌ "Java not found" 
```bash
# Error: java command is not found
# Fix 1: Install Java
winget install Microsoft.OpenJDK.11  # Windows
brew install openjdk@11              # macOS

# Fix 2: Restart terminal after Java installation
# Fix 3: Use activation scripts
.\activate_env.ps1  # Sets JAVA_HOME automatically
```

### ❌ "No PDF files found"
```bash
# Make sure you have PDF files in the project directory
ls *.pdf           # Check for PDF files
# Or specify the file directly
python pdf-extract.py /path/to/your/file.pdf
```

### ❌ "Permission denied" (Windows)
```bash
# PowerShell execution policy issue
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again
.\pdf_env\Scripts\Activate.ps1
```

### ✅ **Verification Commands**
```bash
# Check if virtual environment is active
echo $VIRTUAL_ENV  # Should show path to pdf_env

# Check installed packages
pip list

# Test complete setup
python test_environment.py

# Check Java
java -version
```

## 📋 Command Reference Card

### First Time Setup
```bash
git clone <repo-url> && cd python-pdf-extract
python -m venv pdf_env
.\pdf_env\Scripts\Activate.ps1    # Windows
pip install -r requirements.txt
winget install Microsoft.OpenJDK.11
```

### Daily Usage
```bash
cd python-pdf-extract
.\pdf_env\Scripts\Activate.ps1    # Always activate first!
python pdf-extract.py             # Extract all PDFs
python pdf-extract.py --preview   # Preview before saving
```

### Common Commands
```bash
python pdf-extract.py file.pdf           # Specific file
python pdf-extract.py --pages "1,2"      # Specific pages  
python pdf-extract.py --method camelot   # Advanced extraction
python pdf-extract.py --help            # All options
python test_environment.py              # Verify setup
```

### Troubleshooting
```bash
pip list                                 # Check packages
python test_environment.py              # Full system test
java -version                           # Check Java
pip install --force-reinstall -r requirements.txt  # Fix packages
```

---

**Ready to extract tables from PDFs with ease!** 🚀