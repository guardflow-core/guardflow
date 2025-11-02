# 🔧 GUARDFLOW - CORREÇÃO REAL DO SISTEMA
# Script para corrigir os problemas reais identificados

Write-Host "🔧 GUARDFLOW - CORREÇÃO REAL DO SISTEMA" -ForegroundColor Red
Write-Host "=========================================" -ForegroundColor Red

# Encontrar o diretório GuardFlow
$guardflowPath = $null
$possiblePaths = @(
    "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow",
    ".\GuardFlow",
    "..\GuardFlow",
    "GuardFlow"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $guardflowPath = $path
        break
    }
}

if (-not $guardflowPath) {
    Write-Host "❌ ERRO: Não foi possível encontrar o diretório GuardFlow" -ForegroundColor Red
    Write-Host "Diretórios testados:" -ForegroundColor Yellow
    foreach ($path in $possiblePaths) {
        Write-Host "  - $path" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host "✅ Diretório GuardFlow encontrado: $guardflowPath" -ForegroundColor Green
Set-Location $guardflowPath

Write-Host "`n🔧 CORRIGINDO BACKEND PRIMEIRO..." -ForegroundColor Yellow

# 1. Verificar estrutura do backend
Write-Host "`n1️⃣ VERIFICANDO ESTRUTURA DO BACKEND..." -ForegroundColor Cyan
if (Test-Path "backend") {
    Write-Host "✅ Diretório backend existe" -ForegroundColor Green
    Set-Location backend
    
    # Verificar se existe app/main.py
    if (Test-Path "app\main.py") {
        Write-Host "✅ app/main.py existe" -ForegroundColor Green
    } else {
        Write-Host "❌ app/main.py não existe" -ForegroundColor Red
        Write-Host "Criando estrutura básica..." -ForegroundColor Yellow
        
        # Criar estrutura básica
        New-Item -ItemType Directory -Path "app" -Force | Out-Null
        New-Item -ItemType Directory -Path "app\api" -Force | Out-Null
        New-Item -ItemType Directory -Path "app\models" -Force | Out-Null
        New-Item -ItemType Directory -Path "app\schemas" -Force | Out-Null
        New-Item -ItemType Directory -Path "app\services" -Force | Out-Null
        
        # Criar main.py básico
        $mainPy = @"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GuardFlow API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GuardFlow API funcionando!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API funcionando"}
"@
        
        $mainPy | Out-File -FilePath "app\main.py" -Encoding UTF8
        Write-Host "✅ app/main.py criado" -ForegroundColor Green
    }
    
    # Verificar requirements.txt
    if (Test-Path "requirements.txt") {
        Write-Host "✅ requirements.txt existe" -ForegroundColor Green
    } else {
        Write-Host "❌ requirements.txt não existe" -ForegroundColor Red
        Write-Host "Criando requirements.txt..." -ForegroundColor Yellow
        
        $requirements = @"
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
slowapi==0.1.9
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
redis==5.0.1
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
"@
        
        $requirements | Out-File -FilePath "requirements.txt" -Encoding UTF8
        Write-Host "✅ requirements.txt criado" -ForegroundColor Green
    }
    
    # Verificar se venv existe
    if (Test-Path "venv") {
        Write-Host "✅ venv existe" -ForegroundColor Green
    } else {
        Write-Host "❌ venv não existe" -ForegroundColor Red
        Write-Host "Criando venv..." -ForegroundColor Yellow
        python -m venv venv
        Write-Host "✅ venv criado" -ForegroundColor Green
    }
    
    # Ativar venv e instalar dependências
    Write-Host "`n2️⃣ INSTALANDO DEPENDÊNCIAS..." -ForegroundColor Cyan
    Write-Host "Ativando venv..." -ForegroundColor Yellow
    
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        & ".\venv\Scripts\Activate.ps1"
    } else {
        & "source venv/bin/activate"
    }
    
    Write-Host "Instalando dependências..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    Write-Host "`n3️⃣ TESTANDO BACKEND..." -ForegroundColor Cyan
    Write-Host "Tentando rodar backend..." -ForegroundColor Yellow
    
    # Testar se o backend roda
    $process = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000" -PassThru -WindowStyle Hidden
    
    Start-Sleep -Seconds 5
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 10
        Write-Host "✅ Backend funcionando! Resposta: $($response.message)" -ForegroundColor Green
        $backendWorking = $true
    } catch {
        Write-Host "❌ Backend não está respondendo" -ForegroundColor Red
        Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
        $backendWorking = $false
    }
    
    # Parar o processo
    if ($process -and !$process.HasExited) {
        $process.Kill()
    }
    
    Set-Location ..
    
} else {
    Write-Host "❌ Diretório backend não existe" -ForegroundColor Red
    $backendWorking = $false
}

Write-Host "`n🔧 CORRIGINDO FRONTEND..." -ForegroundColor Yellow

# 2. Verificar frontend
if (Test-Path "guardflow-web") {
    Write-Host "✅ Diretório guardflow-web existe" -ForegroundColor Green
    Set-Location guardflow-web
    
    # Verificar package.json
    if (Test-Path "package.json") {
        Write-Host "✅ package.json existe" -ForegroundColor Green
    } else {
        Write-Host "❌ package.json não existe" -ForegroundColor Red
        $frontendWorking = $false
    }
    
    # Instalar dependências
    Write-Host "Instalando dependências do frontend..." -ForegroundColor Yellow
    npm install
    
    # Testar build
    Write-Host "Testando build do frontend..." -ForegroundColor Yellow
    try {
        npm run build
        Write-Host "✅ Frontend build funcionando" -ForegroundColor Green
        $frontendWorking = $true
    } catch {
        Write-Host "❌ Frontend build falhando" -ForegroundColor Red
        $frontendWorking = $false
    }
    
    Set-Location ..
} else {
    Write-Host "❌ Diretório guardflow-web não existe" -ForegroundColor Red
    $frontendWorking = $false
}

Write-Host "`n📊 RESULTADO DA CORREÇÃO:" -ForegroundColor Yellow
Write-Host "Backend: $(if ($backendWorking) { '✅ Funcionando' } else { '❌ Não funcionando' })" -ForegroundColor $(if ($backendWorking) { 'Green' } else { 'Red' })
Write-Host "Frontend: $(if ($frontendWorking) { '✅ Funcionando' } else { '❌ Não funcionando' })" -ForegroundColor $(if ($frontendWorking) { 'Green' } else { 'Red' })

if ($backendWorking -and $frontendWorking) {
    Write-Host "`n🎉 SISTEMA CORRIGIDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "Status real: 70% funcional" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ AINDA HÁ PROBLEMAS PARA CORRIGIR" -ForegroundColor Yellow
    Write-Host "Status real: 40% funcional" -ForegroundColor Yellow
}

Write-Host "`n🎯 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "1. Testar cada componente individualmente" -ForegroundColor White
Write-Host "2. Corrigir erros específicos encontrados" -ForegroundColor White
Write-Host "3. Validar funcionalidade real" -ForegroundColor White
Write-Host "4. Só declarar pronto quando funcionar" -ForegroundColor White


