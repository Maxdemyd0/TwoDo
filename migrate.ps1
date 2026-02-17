$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir
Write-Host "Working directory set to script location: $scriptDir"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python is not installed or not in PATH."
    exit
}

Write-Host "Running: python manage.py makemigrations..."
python manage.py makemigrations

Write-Host "Running: python manage.py migrate..."
python manage.py migrate

Write-Host "Migrations complete!"

Read-Host "`nPress Enter to exit..."