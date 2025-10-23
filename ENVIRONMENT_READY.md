# PDF Table Extractor - Complete Environment Setup

## ✅ Your Environment is Ready!

You now have a complete, isolated environment for PDF table extraction with:
- **Python Virtual Environment** (`pdf_env/`)
- **Java 11** (Microsoft OpenJDK)
- **All Required Packages** (pandas, tabula-py, jpype1)

## 🚀 Quick Start

### 1. Activate the Environment
```powershell
# PowerShell (recommended)
.\activate_env.ps1

# Or Command Prompt
activate_env.bat
```

### 2. Extract Tables from PDF
```bash
# Auto-detect PDF files in current directory
python pdf-extract.py

# With preview before saving
python pdf-extract.py --preview

# Specify a specific file
python pdf-extract.py your-document.pdf
```

## 📁 What's in Your Directory

```
pdf-extract/
├── pdf_env/              # Virtual environment
├── activate_env.ps1      # PowerShell activation script
├── activate_env.bat      # Command Prompt activation script
├── pdf-extract.py        # Main extraction script
├── table-extract.pdf     # Sample PDF file
├── table-extract.csv     # Extracted data (example)
├── requirements.txt      # Python dependencies
├── README.md            # Main documentation
├── JAVA_SETUP.md        # Java installation guide
└── test_environment.py  # Environment testing script
```

## 🎯 Features

- **Automatic PDF Detection**: Finds PDF files in current directory
- **Smart Table Extraction**: Uses tabula-py with Java integration
- **CSV Output**: Clean, formatted CSV files
- **Preview Mode**: Check tables before saving
- **Multiple Tables**: Handles PDFs with multiple tables
- **Error Handling**: Graceful fallbacks and helpful error messages

## 🧪 Testing Your Setup

Run the test script to verify everything works:
```bash
# Activate environment first
.\activate_env.ps1

# Run tests
python test_environment.py
```

## 💡 Usage Examples

### Basic Extraction
```bash
# Activate environment
.\activate_env.ps1

# Extract from auto-detected PDF
python pdf-extract.py
```

### Advanced Options
```bash
# Preview before saving
python pdf-extract.py --preview

# Extract specific pages
python pdf-extract.py --pages "1,2,3"

# Use specific method
python pdf-extract.py --method tabula

# Get help
python pdf-extract.py --help
```

## 🔧 Environment Details

### Python Environment
- **Type**: Virtual Environment (venv)
- **Location**: `./pdf_env/`
- **Python**: 3.13.2
- **Packages**:
  - pandas 2.3.3
  - tabula-py 2.10.0
  - jpype1 1.6.0

### Java Environment
- **Version**: OpenJDK 11.0.28 LTS
- **Location**: `C:\Program Files\Microsoft\jdk-11.0.28.6-hotspot`
- **Integration**: jpype1 for Python-Java bridge

## 🚨 Troubleshooting

### If you get "Java not found" errors:
1. Make sure you activated the environment: `.\activate_env.ps1`
2. Test Java: `java -version`
3. If still not working, restart your terminal

### If tabula-py fails:
1. Check JAVA_HOME is set: `echo $env:JAVA_HOME`
2. Verify jpype1 is installed: `python -c "import jpype; print(jpype.__version__)"`

### If no tables are found:
1. Try preview mode: `python pdf-extract.py --preview`
2. Check if PDF contains actual tables (not images)
3. Try different pages: `python pdf-extract.py --pages "1"`

## 🎉 Success!

Your environment is ready to extract tables from any PDF file. Just place your PDF files in this directory and run:

```bash
.\activate_env.ps1
python pdf-extract.py
```

The script will automatically find your PDFs and extract any tables to CSV format!