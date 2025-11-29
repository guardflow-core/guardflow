# GuardFlow - Script de Execução Automática
# Executa todos os componentes do GuardFlow

Write-Host "🚀 Iniciando GuardFlow - Sistema de Checkout Inteligente" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend")) {
    Write-Host "❌ Erro: Execute este script no diretório raiz do GuardFlow" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Verificando estrutura do projeto..." -ForegroundColor Yellow

# Verificar estrutura
$components = @("backend", "guardflow-web", "mobile-app")
foreach ($component in $components) {
    if (Test-Path $component) {
        Write-Host "✅ $component encontrado" -ForegroundColor Green
    } else {
        Write-Host "❌ $component não encontrado" -ForegroundColor Red
    }
}

Write-Host "`n🔧 Iniciando Backend (FastAPI)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload" -WindowStyle Normal

Write-Host "⏳ Aguardando 5 segundos para o backend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`n🌐 Iniciando Frontend (React)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd guardflow-web; npm start" -WindowStyle Normal

Write-Host "⏳ Aguardando 3 segundos para o frontend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "`n📱 Iniciando Mobile (React Native)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd mobile-app; npx expo start" -WindowStyle Normal

Write-Host "`n🎉 GuardFlow iniciado com sucesso!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "🔗 URLs de acesso:" -ForegroundColor White
Write-Host "   Backend API: http://127.0.0.1:8002" -ForegroundColor White
Write-Host "   Frontend Web: http://localhost:3000" -ForegroundColor White
Write-Host "   Mobile Expo: Expo Go app" -ForegroundColor White
Write-Host "   API Docs: http://127.0.0.1:8002/docs" -ForegroundColor White
Write-Host "=================================================" -ForegroundColor Green

Write-Host "`n📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Aguarde todos os serviços inicializarem" -ForegroundColor White
Write-Host "2. Acesse o frontend em http://localhost:3000" -ForegroundColor White
Write-Host "3. Teste as APIs em http://127.0.0.1:8002/docs" -ForegroundColor White
Write-Host "4. Use o Expo Go para testar o mobile" -ForegroundColor White

Write-Host "`n🛑 Para parar todos os serviços, feche as janelas do PowerShell" -ForegroundColor Red


