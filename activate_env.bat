@echo off
REM Activate PDF extraction environment

REM Activate Python virtual environment
call "%~dp0pdf_env\Scripts\activate.bat"

REM Set Java environment variables
set JAVA_HOME=C:\Program Files\Microsoft\jdk-11.0.28.6-hotspot
set PATH=%JAVA_HOME%\bin;%PATH%

echo.
echo ✅ PDF Extraction Environment Activated
echo ✅ Python: Virtual Environment  
echo ✅ Java: %JAVA_HOME%
echo.
echo Usage:
echo   python pdf-extract.py
echo   python pdf-extract.py --help
echo   java -version  (to test Java)
echo.