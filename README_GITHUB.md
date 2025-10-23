# PDF Table Extractor 📊

A Python tool that automatically extracts tables from PDF files and converts them to CSV format. Features smart PDF detection, multiple extraction methods, and a complete virtual environment setup.

## ✨ Features

- **🔍 Automatic PDF Detection**: Finds PDF files in the current directory automatically
- **🔄 Multiple Extraction Methods**: Uses both `tabula-py` and `camelot-py` for robust table detection
- **🎯 Smart Method Selection**: Tries different methods if one fails
- **📁 Multiple Output Formats**: Saves single or multiple tables to CSV files
- **👀 Preview Functionality**: Preview tables before saving
- **💻 Command-Line Interface**: Easy to use from command line
- **🖱️ Interactive Mode**: Run without arguments for guided extraction
- **🌐 Virtual Environment**: Complete isolated setup with Java integration

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd python-pdf-extract
   ```

2. **Set up the environment**:
   ```bash
   python -m venv pdf_env
   ```

3. **Activate and install**:
   ```powershell
   # PowerShell
   .\activate_env.ps1
   
   # Command Prompt
   activate_env.bat
   ```

4. **Extract tables**:
   ```bash
   # Auto-detect PDFs in current directory
   python pdf-extract.py
   
   # With preview
   python pdf-extract.py --preview
   ```

## 📋 Requirements

- Python 3.6+
- Java 11+ (automatically guided setup)
- Windows, macOS, or Linux

## 📦 What's Included

- `pdf-extract.py` - Main extraction script
- `activate_env.ps1/bat` - Environment activation scripts
- `setup_env.py` - Automated environment setup
- `test_environment.py` - Environment verification
- `requirements.txt` - Python dependencies
- Complete documentation and guides

## 🎯 Usage Examples

```bash
# Auto-detect and extract
python pdf-extract.py

# Extract specific file
python pdf-extract.py document.pdf

# Extract with preview
python pdf-extract.py --preview

# Extract specific pages
python pdf-extract.py document.pdf --pages "1,2,3"

# Use specific method
python pdf-extract.py --method camelot
```

## 🔧 Environment Setup

The project includes automated environment setup:

1. **Virtual Environment**: Isolated Python environment
2. **Java Integration**: Automatic Java detection and setup
3. **All Dependencies**: pandas, tabula-py, jpype1, and optional camelot-py
4. **Activation Scripts**: One-command environment activation

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

## 🆘 Support

- Check `JAVA_SETUP.md` for Java issues
- Run `python test_environment.py` to verify setup
- See documentation for troubleshooting guides

---

**Ready to extract tables from PDFs with ease!** 🚀