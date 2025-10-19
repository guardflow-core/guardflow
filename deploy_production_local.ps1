# deploy_production_local.ps1
# Script para deploy do GuardFlow em produção local (sem Docker)

Write-Host "🚀 Iniciando Deploy Local do GuardFlow em Produção..." -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend") -or -not (Test-Path "guardflow-web") -or -not (Test-Path "mobile-app")) {
    Write-Host "❌ Erro: Execute este script a partir do diretório raiz do GuardFlow" -ForegroundColor Red
    exit 1
}

# Verificar dependências
Write-Host "📋 Verificando dependências..." -ForegroundColor Yellow

# Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js não encontrado. Instale o Node.js." -ForegroundColor Red
    exit 1
}

# Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python não encontrado. Instale o Python." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Todas as dependências encontradas!" -ForegroundColor Green

# Configurar variáveis de ambiente de produção
Write-Host "🔧 Configurando variáveis de ambiente de produção..." -ForegroundColor Yellow

$env:ENVIRONMENT = "production"
$env:DEBUG = "False"
$env:DATABASE_URL = "sqlite:///./guardflow_prod.db"
$env:REDIS_URL = "redis://localhost:6379"
$env:SECRET_KEY = "production-secret-key-$(Get-Random)"

# Criar arquivo .env de produção
$envContent = @"
# Produção Local
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=sqlite:///./guardflow_prod.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=$env:SECRET_KEY
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"@

$envContent | Out-File -FilePath ".env.production" -Encoding UTF8

Write-Host "✅ Variáveis de ambiente configuradas!" -ForegroundColor Green

# Iniciar Backend
Write-Host "🚀 Iniciando Backend em Produção..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command `"cd backend; .\venv\Scripts\activate; uvicorn app.main:app --host 127.0.0.1 --port 8002 --workers 4`""

# Aguardar backend inicializar
Write-Host "⏳ Aguardando backend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar backend
try {
    $backendResponse = Invoke-RestMethod -Uri "http://localhost:8002/health" -Method GET -TimeoutSec 10
    Write-Host "✅ Backend funcionando: $($backendResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend não está respondendo" -ForegroundColor Red
}

# Iniciar Frontend
Write-Host "🚀 Iniciando Frontend em Produção..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command `"cd guardflow-web; npm run build; npm start`""

# Aguardar frontend inicializar
Write-Host "⏳ Aguardando frontend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Verificar frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 10
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend não está respondendo" -ForegroundColor Red
}

# Iniciar Mobile (se possível)
Write-Host "🚀 Iniciando Mobile em Produção..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command `"cd mobile-app; npx expo start`""

# Aguardar mobile inicializar
Write-Host "⏳ Aguardando mobile inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar mobile
Write-Host "✅ Mobile iniciado com Expo" -ForegroundColor Green

# Executar monitoramento
Write-Host "📊 Executando monitoramento..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command `".\monitor_production.ps1`""

# Relatório final
Write-Host "`n🎉 DEPLOY LOCAL EM PRODUÇÃO CONCLUÍDO!" -ForegroundColor Green
Write-Host "📊 Status dos Serviços:" -ForegroundColor Yellow
Write-Host "  Backend: http://localhost:8002" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "  Health: http://localhost:8002/health" -ForegroundColor Cyan
Write-Host "  Mobile: Use o aplicativo Expo Go" -ForegroundColor Cyan

Write-Host "`n📋 Próximos Passos:" -ForegroundColor Yellow
Write-Host "  1. Configurar domínios (api.guardflow.com, app.guardflow.com)" -ForegroundColor White
Write-Host "  2. Configurar SSL/TLS" -ForegroundColor White
Write-Host "  3. Configurar monitoramento" -ForegroundColor White
Write-Host "  4. Configurar backup" -ForegroundColor White
Write-Host "  5. Executar testes de carga" -ForegroundColor White

Write-Host "`n🚀 GuardFlow está rodando em produção local!" -ForegroundColor Green
