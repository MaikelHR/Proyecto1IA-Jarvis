# Script para iniciar la API con las variables de entorno configuradas
Write-Host "Cargando variables de entorno..." -ForegroundColor Cyan

# Cargar variables permanentes del usuario
$env:AZURE_FACE_KEY = [System.Environment]::GetEnvironmentVariable('AZURE_FACE_KEY', 'User')
$env:AZURE_FACE_ENDPOINT = [System.Environment]::GetEnvironmentVariable('AZURE_FACE_ENDPOINT', 'User')

# Verificar que se cargaron
if ($env:AZURE_FACE_KEY -and $env:AZURE_FACE_ENDPOINT) {
    Write-Host "AZURE_FACE_KEY cargada" -ForegroundColor Green
    Write-Host "AZURE_FACE_ENDPOINT cargada" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "No se encontraron las variables de entorno" -ForegroundColor Yellow
    Write-Host ""
}

# Iniciar la API
Write-Host "Iniciando Jarvis IA API..." -ForegroundColor Cyan
python start_api.py
