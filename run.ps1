$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir
Write-Host "Working directory set to script location: $scriptDir"

$scriptHost = Read-Host "Enter host (default: 127.0.0.1)"
if ([string]::IsNullOrWhiteSpace($scriptHost)) { $scriptHost = "127.0.0.1" }

$scriptPort = Read-Host "Enter port (default: 8000)"
if ([string]::IsNullOrWhiteSpace($scriptPort)) { $scriptPort = "8000" }

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python is not installed or not in PATH."
    exit
}

Write-Host "Starting Django server at http://$scriptHost`:$scriptPort..."
python manage.py runserver "$scriptHost`:$scriptPort"