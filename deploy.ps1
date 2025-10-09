# GuardFlow Deploy Script - PowerShell
Write-Host "🚀 Iniciando deploy do GuardFlow..." -ForegroundColor Green

# Verificar se Docker está instalado
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não está instalado. Instale o Docker primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se Docker Compose está instalado
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose não está instalado. Instale o Docker Compose primeiro." -ForegroundColor Red
    exit 1
}

# Parar containers existentes
Write-Host "🛑 Parando containers existentes..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml down

# Remover imagens antigas
Write-Host "🧹 Removendo imagens antigas..." -ForegroundColor Yellow
docker system prune -f

# Build das imagens
Write-Host "🔨 Fazendo build das imagens..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml build --no-cache

# Iniciar serviços
Write-Host "🚀 Iniciando serviços..." -ForegroundColor Green
docker-compose -f docker-compose.prod.yml up -d

# Aguardar serviços iniciarem
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar saúde dos serviços
Write-Host "🔍 Verificando saúde dos serviços..." -ForegroundColor Cyan

# Verificar backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8002/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend está funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend não está respondendo" -ForegroundColor Red
}

# Verificar frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend está funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend não está respondendo" -ForegroundColor Red
}

Write-Host "🎉 Deploy concluído!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:8002" -ForegroundColor Cyan
Write-Host "📊 API Docs: http://localhost:8002/docs" -ForegroundColor Cyan

# Mostrar logs
Write-Host "📋 Logs dos serviços:" -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml logs --tail=20


