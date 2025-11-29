# GuardFlow - Verificação de Dependências
# Verifica se todas as dependências estão instaladas

Write-Host "🔍 Verificando dependências do GuardFlow" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Verificar Python
Write-Host "`n🐍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale Python 3.11+" -ForegroundColor Red
}

# Verificar Node.js
Write-Host "`n📦 Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js não encontrado. Instale Node.js 18+" -ForegroundColor Red
}

# Verificar npm
Write-Host "`n📦 Verificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "✅ npm encontrado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm não encontrado" -ForegroundColor Red
}

# Verificar pip
Write-Host "`n🐍 Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip não encontrado" -ForegroundColor Red
}

# Verificar estrutura do projeto
Write-Host "`n📁 Verificando estrutura do projeto..." -ForegroundColor Yellow
$requiredDirs = @("backend", "guardflow-web", "mobile-app")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "✅ $dir encontrado" -ForegroundColor Green
    } else {
        Write-Host "❌ $dir não encontrado" -ForegroundColor Red
    }
}

# Verificar arquivos de dependências
Write-Host "`n📄 Verificando arquivos de dependências..." -ForegroundColor Yellow
$dependencyFiles = @(
    "backend/requirements.txt",
    "guardflow-web/package.json",
    "mobile-app/package.json"
)

foreach ($file in $dependencyFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file encontrado" -ForegroundColor Green
    } else {
        Write-Host "❌ $file não encontrado" -ForegroundColor Red
    }
}

# Verificar dependências Python
Write-Host "`n🐍 Verificando dependências Python..." -ForegroundColor Yellow
if (Test-Path "backend/requirements.txt") {
    Write-Host "📋 Instalando dependências Python..." -ForegroundColor Cyan
    Set-Location backend
    pip install -r requirements.txt
    Set-Location ..
    Write-Host "✅ Dependências Python instaladas" -ForegroundColor Green
} else {
    Write-Host "❌ requirements.txt não encontrado" -ForegroundColor Red
}

# Verificar dependências Node.js (Frontend)
Write-Host "`n📦 Verificando dependências Frontend..." -ForegroundColor Yellow
if (Test-Path "guardflow-web/package.json") {
    Write-Host "📋 Instalando dependências Frontend..." -ForegroundColor Cyan
    Set-Location guardflow-web
    npm install
    Set-Location ..
    Write-Host "✅ Dependências Frontend instaladas" -ForegroundColor Green
} else {
    Write-Host "❌ package.json do frontend não encontrado" -ForegroundColor Red
}

# Verificar dependências Node.js (Mobile)
Write-Host "`n📱 Verificando dependências Mobile..." -ForegroundColor Yellow
if (Test-Path "mobile-app/package.json") {
    Write-Host "📋 Instalando dependências Mobile..." -ForegroundColor Cyan
    Set-Location mobile-app
    npm install
    Set-Location ..
    Write-Host "✅ Dependências Mobile instaladas" -ForegroundColor Green
} else {
    Write-Host "❌ package.json do mobile não encontrado" -ForegroundColor Red
}

Write-Host "`n🎉 Verificação de dependências concluída!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "🚀 Execute '.\start_guardflow.ps1' para iniciar o sistema" -ForegroundColor Yellow


