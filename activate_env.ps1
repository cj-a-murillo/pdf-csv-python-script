# Activate PDF extraction environment

# Activate Python virtual environment
& "$PSScriptRoot\pdf_env\Scripts\Activate.ps1"

# Set Java environment variables
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-11.0.28.6-hotspot"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

Write-Host ""
Write-Host "✅ PDF Extraction Environment Activated" -ForegroundColor Green
Write-Host "✅ Python: Virtual Environment" -ForegroundColor Green
Write-Host "✅ Java: $env:JAVA_HOME" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:"
Write-Host "  python pdf-extract.py"
Write-Host "  python pdf-extract.py --help"
Write-Host "  java -version  (to test Java)"
Write-Host ""