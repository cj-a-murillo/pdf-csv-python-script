# Java Installation Guide for PDF Table Extractor

## Option 1: Install Java System-wide (Recommended)

### For Windows:

1. **Download Java:**
   - Go to [Adoptium.net](https://adoptium.net/temurin/releases/)
   - Download "Eclipse Temurin 11 LTS" or "Eclipse Temurin 17 LTS"
   - Choose Windows x64 MSI installer

2. **Install Java:**
   - Run the downloaded MSI file
   - Follow the installation wizard
   - Make sure "Set JAVA_HOME variable" is checked
   - Make sure "Add to PATH" is checked

3. **Verify Installation:**
   ```bash
   java -version
   ```

### Alternative: Using Chocolatey (if you have it)
```bash
choco install openjdk11
```

### Alternative: Using Winget (Windows 10+)
```bash
winget install Microsoft.OpenJDK.11
```

## Option 2: Portable Java Setup (Manual)

If you prefer a portable installation:

1. **Download Portable Java:**
   - Go to [Adoptium.net](https://adoptium.net/temurin/releases/)
   - Download the ZIP version (not MSI)
   - Extract to a folder like `C:\java\jdk-11`

2. **Set Environment Variables:**
   ```batch
   set JAVA_HOME=C:\java\jdk-11
   set PATH=%JAVA_HOME%\bin;%PATH%
   ```

## Option 3: Use Our Environment Scripts

After installing Java (Option 1 or 2), use our activation scripts:

### PowerShell:
```powershell
.\activate_env.ps1
```

### Command Prompt:
```batch
activate_env.bat
```

## Testing Your Setup

After installing Java, test the complete environment:

```bash
# Activate the environment
.\activate_env.ps1

# Test Java
java -version

# Test the PDF extractor
python pdf-extract.py --help

# Test with auto-detection
python pdf-extract.py
```

## Troubleshooting

### "Java not found" error:
- Restart your terminal after installing Java
- Check that `java -version` works
- Verify JAVA_HOME is set: `echo $env:JAVA_HOME`

### Permission errors:
- Run PowerShell as Administrator if needed
- Check antivirus isn't blocking the installation

### tabula-py still not working:
- Try reinstalling tabula-py: `pip uninstall tabula-py && pip install tabula-py`
- Check that jpype is installed: `pip install jpype1`

## Quick Start After Setup

1. Install Java (see above)
2. Activate environment: `.\activate_env.ps1`  
3. Run extractor: `python pdf-extract.py`

The script will automatically find PDF files in the current directory and extract tables from them!