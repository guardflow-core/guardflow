#!/bin/bash

# GuardFlow Deploy Script
echo "🚀 Iniciando deploy do GuardFlow..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose -f docker-compose.prod.yml down

# Remover imagens antigas
echo "🧹 Removendo imagens antigas..."
docker system prune -f

# Build das imagens
echo "🔨 Fazendo build das imagens..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker-compose -f docker-compose.prod.yml up -d

# Aguardar serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 30

# Verificar saúde dos serviços
echo "🔍 Verificando saúde dos serviços..."

# Verificar backend
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ Backend está funcionando"
else
    echo "❌ Backend não está respondendo"
fi

# Verificar frontend
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Frontend está funcionando"
else
    echo "❌ Frontend não está respondendo"
fi

# Verificar banco de dados
if docker-compose -f docker-compose.prod.yml exec -T db pg_isready -U guardflow > /dev/null 2>&1; then
    echo "✅ Banco de dados está funcionando"
else
    echo "❌ Banco de dados não está respondendo"
fi

# Verificar Redis
if docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis está funcionando"
else
    echo "❌ Redis não está respondendo"
fi

echo "🎉 Deploy concluído!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8002"
echo "📊 API Docs: http://localhost:8002/docs"

# Mostrar logs
echo "📋 Logs dos serviços:"
docker-compose -f docker-compose.prod.yml logs --tail=20


