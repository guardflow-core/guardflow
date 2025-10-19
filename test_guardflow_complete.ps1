# GuardFlow - Teste Completo do Sistema
# Testa todos os componentes do GuardFlow

Write-Host "🧪 TESTE COMPLETO DO GUARDFLOW" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend")) {
    Write-Host "❌ Erro: Execute este script no diretório raiz do GuardFlow" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔧 TESTE 1: Backend (FastAPI)" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

# Testar import do backend
Write-Host "📋 Testando import do backend..."
cd backend
$importTest = python -c "try: import app.main; print('✅ Backend import OK') except Exception as e: print(f'❌ Backend import ERROR: {e}')" 2>&1
Write-Host $importTest

if ($importTest -like "*✅*") {
    Write-Host "✅ Backend import funcionando" -ForegroundColor Green
    
    # Iniciar backend em background
    Write-Host "🚀 Iniciando backend..."
    Start-Process powershell -ArgumentList "-NoExit -Command `"cd backend; python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload`""
    
    # Aguardar inicialização
    Write-Host "⏳ Aguardando 10 segundos para backend inicializar..."
    Start-Sleep -Seconds 10
    
    # Testar endpoint
    Write-Host "🔍 Testando endpoint /health..."
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8002/health" -Method GET -TimeoutSec 5
        Write-Host "✅ Backend respondendo: $($response.status)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Backend não está respondendo: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Backend com problemas de import" -ForegroundColor Red
}

cd ..

Write-Host "`n🌐 TESTE 2: Frontend (React)" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

# Verificar se guardflow-web existe
if (Test-Path "guardflow-web") {
    Write-Host "📋 Testando frontend..."
    cd guardflow-web
    
    # Verificar package.json
    if (Test-Path "package.json") {
        Write-Host "✅ package.json encontrado" -ForegroundColor Green
        
        # Verificar node_modules
        if (Test-Path "node_modules") {
            Write-Host "✅ node_modules encontrado" -ForegroundColor Green
            
            # Iniciar frontend em background
            Write-Host "🚀 Iniciando frontend..."
            Start-Process powershell -ArgumentList "-NoExit -Command `"cd guardflow-web; npm start`""
            
            # Aguardar inicialização
            Write-Host "⏳ Aguardando 15 segundos para frontend inicializar..."
            Start-Sleep -Seconds 15
            
            # Testar se está rodando
            Write-Host "🔍 Testando se frontend está rodando..."
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 5
                if ($response.StatusCode -eq 200) {
                    Write-Host "✅ Frontend respondendo na porta 3000" -ForegroundColor Green
                }
            } catch {
                Write-Host "❌ Frontend não está respondendo: $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ node_modules não encontrado - execute 'npm install'" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ package.json não encontrado" -ForegroundColor Red
    }
    cd ..
} else {
    Write-Host "❌ Diretório guardflow-web não encontrado" -ForegroundColor Red
}

Write-Host "`n📱 TESTE 3: Mobile (Expo)" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

# Verificar se mobile-app existe
if (Test-Path "mobile-app") {
    Write-Host "📋 Testando mobile..."
    cd mobile-app
    
    # Verificar package.json
    if (Test-Path "package.json") {
        Write-Host "✅ package.json encontrado" -ForegroundColor Green
        
        # Verificar se expo está instalado
        $expoCheck = npm list expo 2>$null
        if ($expoCheck -like "*expo*") {
            Write-Host "✅ Expo instalado" -ForegroundColor Green
            
            # Iniciar mobile em background
            Write-Host "🚀 Iniciando mobile..."
            Start-Process powershell -ArgumentList "-NoExit -Command `"cd mobile-app; npx expo start`""
            
            Write-Host "✅ Mobile iniciado - use Expo Go para testar" -ForegroundColor Green
        } else {
            Write-Host "❌ Expo não instalado - instalando..." -ForegroundColor Yellow
            npm install expo
            Write-Host "✅ Expo instalado" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ package.json não encontrado" -ForegroundColor Red
    }
    cd ..
} else {
    Write-Host "❌ Diretório mobile-app não encontrado" -ForegroundColor Red
}

Write-Host "`n📊 RESUMO DOS TESTES" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan

# Verificar portas em uso
Write-Host "`n🔍 Verificando portas em uso:"
$ports = @(8002, 3000, 19006)
foreach ($port in $ports) {
    $connection = netstat -an | findstr ":$port"
    if ($connection) {
        Write-Host "✅ Porta $port está em uso" -ForegroundColor Green
    } else {
        Write-Host "❌ Porta $port não está em uso" -ForegroundColor Red
    }
}

Write-Host "`n🎯 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "1. Acesse http://localhost:3000 para testar o frontend" -ForegroundColor White
Write-Host "2. Acesse http://127.0.0.1:8002/docs para testar a API" -ForegroundColor White
Write-Host "3. Use Expo Go no celular para testar o mobile" -ForegroundColor White
Write-Host "4. Verifique os logs nos terminais abertos" -ForegroundColor White

Write-Host "`n🛑 Para parar todos os serviços, feche as janelas do PowerShell" -ForegroundColor Red


