# Script de configuración para Windows PowerShell

Write-Host "=== Configuración del Backend Flask ===" -ForegroundColor Green

# Verificar Python
Write-Host "`nVerificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Error: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Descarga Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Crear entorno virtual
Write-Host "`nCreando entorno virtual..." -ForegroundColor Yellow
python -m venv venv

if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "Entorno virtual creado exitosamente" -ForegroundColor Green
} else {
    Write-Host "Error al crear el entorno virtual" -ForegroundColor Red
    exit 1
}

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "`nActualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependencias
Write-Host "`nInstalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Instalación completada exitosamente ===" -ForegroundColor Green
    Write-Host "`nPara activar el entorno virtual en el futuro, ejecuta:" -ForegroundColor Cyan
    Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "`nPara ejecutar la aplicación:" -ForegroundColor Cyan
    Write-Host "python app.py" -ForegroundColor White
} else {
    Write-Host "`nError durante la instalación de dependencias" -ForegroundColor Red
    exit 1
}
