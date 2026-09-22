# run_frontend.ps1

# ---------------------------------------------------------------
# 1️⃣  Project root detection
# ---------------------------------------------------------------
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# ---------------------------------------------------------------
# 2️⃣  (Optional) Activate Python virtual environment (backend)
# ---------------------------------------------------------------
$venvPath = Join-Path $projectRoot "venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Virtual environment not found at $venvPath"
}

# ---------------------------------------------------------------
# 3️⃣  Move to the frontend directory
# ---------------------------------------------------------------
$frontendPath = Join-Path $projectRoot "frontend"
Set-Location $frontendPath

# ---------------------------------------------------------------
# 4️⃣  Install node modules if they are missing
# ---------------------------------------------------------------
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..."
    npm install
}

# ---------------------------------------------------------------
# 5️⃣  Ensure .env.local contains the API base URL for the backend
# ---------------------------------------------------------------
$envFile = Join-Path $frontendPath ".env.local"
if (-not (Test-Path $envFile)) {
    $apiUrlLine = "VITE_API_URL=http://127.0.0.1:8000/api"
    Set-Content -Path $envFile -Value $apiUrlLine -Encoding UTF8
    Write-Host "✅ .env.local created with API URL"
}

# ---------------------------------------------------------------
# 6️⃣  Launch the Vite development server (frontend)
# ---------------------------------------------------------------
Write-Host "🚀 Starting Vite dev server on http://localhost:5173/"
npm run dev
