# Script para iniciar el servidor con el entorno virtual correcto
# ============================================================

Write-Host "Activando entorno virtual..." -ForegroundColor Cyan

# Activar entorno virtual
& "D:\TEC\IA\Proyecto1IA-Jarvis\.venv\Scripts\Activate.ps1"

Write-Host "Entorno virtual activado" -ForegroundColor Green
Write-Host "Python: $((Get-Command python).Source)" -ForegroundColor Yellow

Write-Host "`nIniciando servidor..." -ForegroundColor Cyan

# Cambiar al directorio backend
Set-Location "D:\TEC\IA\Proyecto1IA-Jarvis\backend"

# Ejecutar el servidor
python start_api.py
