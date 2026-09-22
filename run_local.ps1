# Run both backend and frontend for local development

# 1️⃣ Activate virtual environment
$venvPath = "${PSScriptRoot}\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Virtual environment not found at $venvPath"
    exit 1
}

# 2️⃣ Start Django backend in a new PowerShell window
$backendPath = "${PSScriptRoot}\backend"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "python manage.py runserver" -WorkingDirectory $backendPath

# 3️⃣ Start React/Vite frontend in another new PowerShell window
$frontendPath = "${PSScriptRoot}\frontend"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "npm run dev" -WorkingDirectory $frontendPath

Write-Host "✅ Both backend and frontend have been launched in separate windows."
