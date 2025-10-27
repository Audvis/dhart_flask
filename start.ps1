# Script para iniciar el servidor Flask

Write-Host "=== Iniciando Backend Flask ===" -ForegroundColor Green

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv\Scripts\activate.ps1")) {
    Write-Host "Error: Entorno virtual no encontrado" -ForegroundColor Red
    Write-Host "Ejecuta primero: .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Verificar si existe .env
if (-Not (Test-Path ".env")) {
    Write-Host "Advertencia: Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "Copia .env.example a .env y configura tus credenciales" -ForegroundColor Yellow
    Write-Host "`nCreando .env desde .env.example..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "Archivo .env creado. Por favor edítalo con tus credenciales antes de continuar." -ForegroundColor Yellow
    Write-Host "Presiona Enter cuando hayas configurado el archivo .env..."
    Read-Host
}

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Iniciar servidor
Write-Host "`nIniciando servidor Flask..." -ForegroundColor Green
Write-Host "El servidor estará disponible en: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Presiona Ctrl+C para detener el servidor`n" -ForegroundColor Yellow

python app.py
