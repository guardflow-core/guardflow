# deploy_production.ps1
# Script para deploy do GuardFlow em produção

Write-Host "🚀 Iniciando Deploy do GuardFlow em Produção..." -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend") -or -not (Test-Path "guardflow-web") -or -not (Test-Path "mobile-app")) {
    Write-Host "❌ Erro: Execute este script a partir do diretório raiz do GuardFlow" -ForegroundColor Red
    exit 1
}

# Verificar dependências
Write-Host "📋 Verificando dependências..." -ForegroundColor Yellow

# Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não encontrado. Instale o Docker Desktop." -ForegroundColor Red
    exit 1
}

# Docker Compose
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose não encontrado. Instale o Docker Compose." -ForegroundColor Red
    exit 1
}

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
$env:DATABASE_URL = "postgresql://user:pass@prod-db:5432/guardflow"
$env:REDIS_URL = "redis://prod-redis:6379"
$env:SECRET_KEY = "production-secret-key-$(Get-Random)"

# Criar arquivo .env de produção
$envContent = @"
# Produção
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@prod-db:5432/guardflow
REDIS_URL=redis://prod-redis:6379
SECRET_KEY=$env:SECRET_KEY
ALLOWED_HOSTS=api.guardflow.com,app.guardflow.com
CORS_ORIGINS=https://app.guardflow.com,https://mobile.guardflow.com
"@

$envContent | Out-File -FilePath ".env.production" -Encoding UTF8

Write-Host "✅ Variáveis de ambiente configuradas!" -ForegroundColor Green

# Build das imagens Docker
Write-Host "🐳 Construindo imagens Docker..." -ForegroundColor Yellow

# Backend
Write-Host "📦 Construindo imagem do Backend..." -ForegroundColor Cyan
docker build -t guardflow-backend:latest ./backend

# Frontend
Write-Host "📦 Construindo imagem do Frontend..." -ForegroundColor Cyan
docker build -t guardflow-frontend:latest ./guardflow-web

# Mobile (se necessário)
Write-Host "📦 Construindo imagem do Mobile..." -ForegroundColor Cyan
docker build -t guardflow-mobile:latest ./mobile-app

Write-Host "✅ Imagens Docker construídas!" -ForegroundColor Green

# Deploy com Docker Compose
Write-Host "🚀 Iniciando deploy com Docker Compose..." -ForegroundColor Yellow

# Criar docker-compose.prod.yml
$dockerComposeContent = @"
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: guardflow
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d guardflow"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: ./backend
    image: guardflow-backend:latest
    environment:
      - ENVIRONMENT=production
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@postgres:5432/guardflow
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=production-secret-key
    ports:
      - "8002:8002"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./guardflow-web
    image: guardflow-frontend:latest
    ports:
      - "3000:3000"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
"@

$dockerComposeContent | Out-File -FilePath "docker-compose.prod.yml" -Encoding UTF8

# Criar nginx.conf
$nginxContent = @"
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8002;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name api.guardflow.com;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    server {
        listen 80;
        server_name app.guardflow.com;

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"@

$nginxContent | Out-File -FilePath "nginx.conf" -Encoding UTF8

# Iniciar serviços
Write-Host "🚀 Iniciando serviços de produção..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml up -d

# Aguardar serviços ficarem prontos
Write-Host "⏳ Aguardando serviços ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar status dos serviços
Write-Host "🔍 Verificando status dos serviços..." -ForegroundColor Yellow

# Verificar backend
try {
    $backendResponse = Invoke-RestMethod -Uri "http://localhost:8002/health" -Method GET
    Write-Host "✅ Backend funcionando: $($backendResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend não está respondendo" -ForegroundColor Red
}

# Verificar frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend funcionando" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend não está respondendo" -ForegroundColor Red
}

# Verificar banco de dados
try {
    $dbResponse = Invoke-RestMethod -Uri "http://localhost:8002/health/database" -Method GET
    Write-Host "✅ Banco de dados funcionando" -ForegroundColor Green
} catch {
    Write-Host "❌ Banco de dados não está respondendo" -ForegroundColor Red
}

# Verificar Redis
try {
    $redisResponse = Invoke-RestMethod -Uri "http://localhost:8002/health/redis" -Method GET
    Write-Host "✅ Redis funcionando" -ForegroundColor Green
} catch {
    Write-Host "❌ Redis não está respondendo" -ForegroundColor Red
}

# Relatório final
Write-Host "`n🎉 DEPLOY EM PRODUÇÃO CONCLUÍDO!" -ForegroundColor Green
Write-Host "📊 Status dos Serviços:" -ForegroundColor Yellow
Write-Host "  Backend: http://localhost:8002" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "  Health: http://localhost:8002/health" -ForegroundColor Cyan

Write-Host "`n📋 Próximos Passos:" -ForegroundColor Yellow
Write-Host "  1. Configurar domínios (api.guardflow.com, app.guardflow.com)" -ForegroundColor White
Write-Host "  2. Configurar SSL/TLS" -ForegroundColor White
Write-Host "  3. Configurar monitoramento" -ForegroundColor White
Write-Host "  4. Configurar backup" -ForegroundColor White
Write-Host "  5. Executar testes de carga" -ForegroundColor White

Write-Host "`n🚀 GuardFlow está rodando em produção!" -ForegroundColor Green
