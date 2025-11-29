# 🔍 GUARDFLOW - ANÁLISE SISTEMÁTICA BACKEND
# Script para analisar o backend de forma sistemática

Write-Host "🔍 GUARDFLOW - ANÁLISE SISTEMÁTICA BACKEND" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

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
    exit 1
}

Write-Host "✅ Diretório GuardFlow encontrado: $guardflowPath" -ForegroundColor Green
Set-Location $guardflowPath

Write-Host "`n🔍 FASE 1 - ANÁLISE DO BACKEND" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

# 1. Verificar estrutura do backend
Write-Host "`n1️⃣ VERIFICANDO ESTRUTURA DO BACKEND..." -ForegroundColor Cyan
if (Test-Path "backend") {
    Write-Host "✅ Diretório backend existe" -ForegroundColor Green
    Set-Location backend
    
    # Verificar estrutura de diretórios
    Write-Host "`n📁 ESTRUTURA DE DIRETÓRIOS:" -ForegroundColor Yellow
    Get-ChildItem -Directory | ForEach-Object {
        Write-Host "  📁 $($_.Name)" -ForegroundColor White
    }
    
    # Verificar arquivos principais
    Write-Host "`n📄 ARQUIVOS PRINCIPAIS:" -ForegroundColor Yellow
    $mainFiles = @("main.py", "app.py", "requirements.txt", "Dockerfile")
    foreach ($file in $mainFiles) {
        if (Test-Path $file) {
            Write-Host "  ✅ $file" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $file" -ForegroundColor Red
        }
    }
    
    # Verificar estrutura app/
    if (Test-Path "app") {
        Write-Host "`n📁 ESTRUTURA APP/:" -ForegroundColor Yellow
        Get-ChildItem -Path "app" -Recurse -File | ForEach-Object {
            Write-Host "  📄 $($_.FullName.Replace((Get-Location).Path + '\', ''))" -ForegroundColor White
        }
    } else {
        Write-Host "❌ Diretório app/ não existe" -ForegroundColor Red
    }
    
    # 2. Verificar dependências
    Write-Host "`n2️⃣ VERIFICANDO DEPENDÊNCIAS..." -ForegroundColor Cyan
    if (Test-Path "requirements.txt") {
        Write-Host "✅ requirements.txt existe" -ForegroundColor Green
        Write-Host "`n📦 DEPENDÊNCIAS:" -ForegroundColor Yellow
        Get-Content "requirements.txt" | ForEach-Object {
            Write-Host "  📦 $_" -ForegroundColor White
        }
    } else {
        Write-Host "❌ requirements.txt não existe" -ForegroundColor Red
    }
    
    # 3. Verificar venv
    Write-Host "`n3️⃣ VERIFICANDO VENV..." -ForegroundColor Cyan
    if (Test-Path "venv") {
        Write-Host "✅ venv existe" -ForegroundColor Green
    } else {
        Write-Host "❌ venv não existe" -ForegroundColor Red
    }
    
    # 4. Testar se roda
    Write-Host "`n4️⃣ TESTANDO SE RODA..." -ForegroundColor Cyan
    
    # Verificar se main.py existe
    if (Test-Path "main.py") {
        Write-Host "✅ main.py existe" -ForegroundColor Green
        Write-Host "Tentando rodar backend..." -ForegroundColor Yellow
        
        # Tentar rodar
        try {
            $process = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--reload", "--port", "8000" -PassThru -WindowStyle Hidden
            Start-Sleep -Seconds 3
            
            # Testar endpoint
            try {
                $response = Invoke-RestMethod -Uri "http://localhost:8000/" -Method GET -TimeoutSec 5
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
        } catch {
            Write-Host "❌ Erro ao tentar rodar backend" -ForegroundColor Red
            Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
            $backendWorking = $false
        }
    } else {
        Write-Host "❌ main.py não existe" -ForegroundColor Red
        $backendWorking = $false
    }
    
    Set-Location ..
    
} else {
    Write-Host "❌ Diretório backend não existe" -ForegroundColor Red
    $backendWorking = $false
}

# 5. Relatório final
Write-Host "`n📊 RELATÓRIO FINAL DO BACKEND:" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

if ($backendWorking) {
    Write-Host "✅ BACKEND FUNCIONANDO" -ForegroundColor Green
    Write-Host "Status: 100% funcional" -ForegroundColor Green
} else {
    Write-Host "❌ BACKEND NÃO FUNCIONANDO" -ForegroundColor Red
    Write-Host "Status: 0% funcional" -ForegroundColor Red
}

Write-Host "`n🎯 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
if (-not $backendWorking) {
    Write-Host "1. Corrigir estrutura de diretórios" -ForegroundColor White
    Write-Host "2. Instalar dependências" -ForegroundColor White
    Write-Host "3. Configurar venv" -ForegroundColor White
    Write-Host "4. Testar APIs" -ForegroundColor White
} else {
    Write-Host "1. Continuar para análise do frontend" -ForegroundColor White
    Write-Host "2. Testar integração" -ForegroundColor White
    Write-Host "3. Validar funcionalidade" -ForegroundColor White
}

Write-Host "`n🎉 ANÁLISE SISTEMÁTICA BACKEND FINALIZADA!" -ForegroundColor Green


