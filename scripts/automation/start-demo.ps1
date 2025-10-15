# GuardFlow Demo - Script de Inicialização
# Este script inicia o ambiente completo do GuardFlow para demonstração

Write-Host "🚀 Iniciando GuardFlow Demo..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Verificar se Docker está instalado
Write-Host "📋 Verificando Docker..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "✅ Docker encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não encontrado. Instale o Docker Desktop primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se Docker Compose está disponível
Write-Host "📋 Verificando Docker Compose..." -ForegroundColor Yellow
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose não encontrado." -ForegroundColor Red
    exit 1
}

# Parar containers existentes
Write-Host "🛑 Parando containers existentes..." -ForegroundColor Yellow
docker-compose down 2>$null

# Construir e iniciar os serviços
Write-Host "🔨 Construindo e iniciando serviços..." -ForegroundColor Yellow
Write-Host "   - Backend FastAPI (Porta 8000)" -ForegroundColor Cyan
Write-Host "   - Frontend React (Porta 3000)" -ForegroundColor Cyan
Write-Host "   - PostgreSQL (Porta 5432)" -ForegroundColor Cyan
Write-Host "   - Redis (Porta 6379)" -ForegroundColor Cyan

docker-compose up --build -d

# Aguardar os serviços iniciarem
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar status dos serviços
Write-Host "🔍 Verificando status dos serviços..." -ForegroundColor Yellow

# Verificar Backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend FastAPI funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Backend ainda inicializando..." -ForegroundColor Yellow
}

# Verificar Frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend React funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Frontend ainda inicializando..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 GuardFlow Demo iniciado com sucesso!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acesse o sistema:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "   Documentação: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📱 Funcionalidades disponíveis:" -ForegroundColor Cyan
Write-Host "   • Escaneamento de produtos (simulado)" -ForegroundColor White
Write-Host "   • Carrinho de compras" -ForegroundColor White
Write-Host "   • Múltiplas formas de pagamento" -ForegroundColor White
Write-Host "   • Sistema GuardPass" -ForegroundColor White
Write-Host "   • Tokens ESG" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Para parar o demo: docker-compose down" -ForegroundColor Yellow
Write-Host "📊 Para ver logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host ""

# Abrir o navegador
Write-Host "🌐 Abrindo navegador..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"
