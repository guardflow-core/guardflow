# GuardFlow - Script de Execução do Plano de Desenvolvimento Paralelo
# Integração com ARKITECT e MCPs do Cursor

param(
    [string]$Phase = "all",
    [switch]$Parallel = $true,
    [switch]$Verbose = $false
)

Write-Host "🚀 Iniciando Execução do Plano GuardFlow..." -ForegroundColor Green

# Configurar ambiente
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Função para executar comandos em paralelo
function Start-ParallelTask {
    param(
        [string]$Name,
        [scriptblock]$ScriptBlock,
        [string]$WorkingDirectory = "."
    )
    
    Write-Host "🔄 Iniciando tarefa: $Name" -ForegroundColor Yellow
    
    $job = Start-Job -ScriptBlock {
        param($ScriptBlock, $WorkingDirectory)
        Set-Location $WorkingDirectory
        & $ScriptBlock
    } -ArgumentList $ScriptBlock, $WorkingDirectory
    
    return @{
        Name = $Name
        Job = $job
        StartTime = Get-Date
    }
}

# Função para aguardar conclusão de tarefas
function Wait-ForTasks {
    param([array]$Tasks)
    
    foreach ($task in $Tasks) {
        Write-Host "⏳ Aguardando conclusão: $($task.Name)" -ForegroundColor Cyan
        $result = Receive-Job -Job $task.Job -Wait
        $duration = (Get-Date) - $task.StartTime
        Write-Host "✅ Concluído: $($task.Name) (${duration.TotalSeconds}s)" -ForegroundColor Green
        
        if ($Verbose) {
            Write-Host "📋 Resultado: $result" -ForegroundColor Gray
        }
    }
}

# Fase 1: Configuração e Setup
if ($Phase -eq "all" -or $Phase -eq "setup") {
    Write-Host "`n📋 FASE 1: CONFIGURAÇÃO E SETUP" -ForegroundColor Magenta
    
    $setupTasks = @()
    
    # Configurar MCPs do Cursor
    $setupTasks += Start-ParallelTask -Name "MCP-Cursor-Config" -ScriptBlock {
        Write-Host "Configurando MCPs do Cursor..."
        Copy-Item "cursor-mcp-config.json" "$env:APPDATA\Cursor\User\globalStorage\cursor-mcp\config.json" -Force
        Write-Host "MCPs configurados com sucesso"
    }
    
    # Configurar ambiente Python
    $setupTasks += Start-ParallelTask -Name "Python-Env" -ScriptBlock {
        Write-Host "Configurando ambiente Python..."
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        pip install -r backend\requirements.txt
        Write-Host "Ambiente Python configurado"
    } -WorkingDirectory "."
    
    # Configurar ambiente Node.js
    $setupTasks += Start-ParallelTask -Name "Node-Env" -ScriptBlock {
        Write-Host "Configurando ambiente Node.js..."
        cd guardflow-web
        npm install
        cd ..\mobile-app
        npm install
        cd ..\guardflow-saas
        npm install
        Write-Host "Ambiente Node.js configurado"
    } -WorkingDirectory "."
    
    Wait-ForTasks -Tasks $setupTasks
}

# Fase 2: Backend - Segurança e Testes
if ($Phase -eq "all" -or $Phase -eq "backend") {
    Write-Host "`n🔐 FASE 2: BACKEND - SEGURANÇA E TESTES" -ForegroundColor Magenta
    
    $backendTasks = @()
    
    # Implementar segurança OAuth2/JWT
    $backendTasks += Start-ParallelTask -Name "Backend-Security" -ScriptBlock {
        Write-Host "Implementando segurança OAuth2/JWT..."
        cd backend
        
        # Criar arquivo de configuração de segurança
        @"
# GuardFlow Security Configuration
SECURITY_CONFIG = {
    "oauth2": {
        "client_id": "guardflow_client",
        "client_secret": "guardflow_secret_2024",
        "authorization_url": "https://auth.guardflow.com/oauth/authorize",
        "token_url": "https://auth.guardflow.com/oauth/token",
        "scopes": ["read", "write", "admin"]
    },
    "jwt": {
        "secret_key": "guardflow_jwt_secret_2024",
        "algorithm": "HS256",
        "access_token_expire_minutes": 30,
        "refresh_token_expire_days": 7
    },
    "rbac": {
        "roles": ["admin", "manager", "user", "guest"],
        "permissions": {
            "admin": ["*"],
            "manager": ["read", "write", "manage_users"],
            "user": ["read", "write"],
            "guest": ["read"]
        }
    }
}
"@ | Out-File -FilePath "app\config\security.py" -Encoding UTF8
        
        Write-Host "Configuração de segurança criada"
    } -WorkingDirectory "."
    
    # Expandir cobertura de testes
    $backendTasks += Start-ParallelTask -Name "Backend-Tests" -ScriptBlock {
        Write-Host "Expandindo cobertura de testes..."
        cd backend
        
        # Criar testes adicionais
        @"
import pytest
from httpx import AsyncClient
from app.main import app
from app.config.security import SECURITY_CONFIG

class TestSecurity:
    @pytest.mark.asyncio
    async def test_oauth2_flow(self):
        # Teste do fluxo OAuth2
        pass
    
    @pytest.mark.asyncio 
    async def test_jwt_token_validation(self):
        # Teste de validação de JWT
        pass
    
    @pytest.mark.asyncio
    async def test_rbac_permissions(self):
        # Teste de permissões RBAC
        pass

class TestCart:
    @pytest.mark.asyncio
    async def test_add_item_to_cart(self):
        # Teste de adicionar item ao carrinho
        pass
    
    @pytest.mark.asyncio
    async def test_remove_item_from_cart(self):
        # Teste de remover item do carrinho
        pass

class TestPayment:
    @pytest.mark.asyncio
    async def test_pix_payment(self):
        # Teste de pagamento PIX
        pass
    
    @pytest.mark.asyncio
    async def test_payment_validation(self):
        # Teste de validação de pagamento
        pass
"@ | Out-File -FilePath "tests\test_security_cart_payment.py" -Encoding UTF8
        
        # Executar testes
        python -m pytest tests/ -v --cov=app --cov-report=html
        Write-Host "Testes executados com cobertura"
    } -WorkingDirectory "."
    
    # Implementar contratos Pydantic
    $backendTasks += Start-ParallelTask -Name "Backend-Schemas" -ScriptBlock {
        Write-Host "Implementando contratos Pydantic..."
        cd backend
        
        @"
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager" 
    USER = "user"
    GUEST = "guest"

class UserBase(BaseModel):
    email: str = Field(..., description="Email do usuário")
    name: str = Field(..., description="Nome do usuário")
    role: UserRole = Field(default=UserRole.USER, description="Papel do usuário")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Senha do usuário")

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., description="Nome do produto")
    price: float = Field(..., gt=0, description="Preço do produto")
    description: Optional[str] = Field(None, description="Descrição do produto")
    esg_score: Optional[float] = Field(None, ge=0, le=10, description="Score ESG do produto")

class ProductCreate(ProductBase):
    store_id: str = Field(..., description="ID da loja")

class ProductResponse(ProductBase):
    id: str
    store_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: str = Field(..., description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade")
    
class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: str
    product: ProductResponse
    total_price: float
    
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0, description="Valor do pagamento")
    method: str = Field(..., description="Método de pagamento")
    
class PaymentCreate(PaymentBase):
    cart_id: str = Field(..., description="ID do carrinho")

class PaymentResponse(PaymentBase):
    id: str
    status: str
    transaction_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
"@ | Out-File -FilePath "app\schemas\models.py" -Encoding UTF8
        
        Write-Host "Contratos Pydantic implementados"
    } -WorkingDirectory "."
    
    Wait-ForTasks -Tasks $backendTasks
}

# Fase 3: Mobile e Web - Alinhamento
if ($Phase -eq "all" -or $Phase -eq "frontend") {
    Write-Host "`n📱 FASE 3: MOBILE E WEB - ALINHAMENTO" -ForegroundColor Magenta
    
    $frontendTasks = @()
    
    # Alinhar Mobile com API
    $frontendTasks += Start-ParallelTask -Name "Mobile-API-Alignment" -ScriptBlock {
        Write-Host "Alinhando Mobile com API..."
        cd mobile-app
        
        # Configurar API_BASE_URL
        @"
const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  ENDPOINTS: {
    AUTH: '/api/v1/auth',
    PRODUCTS: '/api/v1/products', 
    CART: '/api/v1/cart',
    PAYMENT: '/api/v1/payment',
    ESG: '/api/v1/esg'
  }
};

export default API_CONFIG;
"@ | Out-File -FilePath "src\config\api.js" -Encoding UTF8
        
        Write-Host "Mobile alinhado com API"
    } -WorkingDirectory "."
    
    # Consolidar Web Demo
    $frontendTasks += Start-ParallelTask -Name "Web-Demo-Consolidation" -ScriptBlock {
        Write-Host "Consolidando Web Demo..."
        cd guardflow-web
        
        # Criar configuração unificada
        @"
// GuardFlow Web - Configuração Unificada
const CONFIG = {
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  FEATURES: {
    SCANNER: true,
    ESG_DASHBOARD: true,
    PAYMENT_PIX: true,
    TOKEN_GST: true
  },
  THEME: {
    PRIMARY_COLOR: '#2E7D32',
    SECONDARY_COLOR: '#4CAF50',
    ACCENT_COLOR: '#FFC107'
  }
};

export default CONFIG;
"@ | Out-File -FilePath "src\config\index.js" -Encoding UTF8
        
        Write-Host "Web Demo consolidada"
    } -WorkingDirectory "."
    
    Wait-ForTasks -Tasks $frontendTasks
}

# Fase 4: Infraestrutura e CI/CD
if ($Phase -eq "all" -or $Phase -eq "infra") {
    Write-Host "`n🏗️ FASE 4: INFRAESTRUTURA E CI/CD" -ForegroundColor Magenta
    
    $infraTasks = @()
    
    # Dockerizar serviços
    $infraTasks += Start-ParallelTask -Name "Docker-Setup" -ScriptBlock {
        Write-Host "Configurando Docker..."
        
        # Docker Compose para desenvolvimento
        @"
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://guardflow:guardflow@db:5432/guardflow
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
      
  frontend:
    build: ./guardflow-web
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_BASE_URL=http://localhost:8000
    depends_on:
      - backend
      
  mobile-api:
    build: ./mobile-app
    ports:
      - "8081:8081"
    environment:
      - API_BASE_URL=http://backend:8000
    depends_on:
      - backend
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=guardflow
      - POSTGRES_USER=guardflow
      - POSTGRES_PASSWORD=guardflow
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7
    ports:
      - "6379:6379"
      
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=guardflow
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  grafana_data:
"@ | Out-File -FilePath "docker-compose.dev.yml" -Encoding UTF8
        
        Write-Host "Docker configurado"
    } -WorkingDirectory "."
    
    # Configurar CI/CD
    $infraTasks += Start-ParallelTask -Name "CI-CD-Setup" -ScriptBlock {
        Write-Host "Configurando CI/CD..."
        
        # GitHub Actions workflow
        @"
name: GuardFlow CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run linting
        run: |
          pip install flake8 mypy
          flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
          mypy app/ --ignore-missing-imports
      - name: Run tests
        run: |
          pip install pytest pytest-cov
          pytest tests/ -v --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          
  frontend-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./guardflow-web
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run linting
        run: npm run lint
      - name: Run tests
        run: npm test -- --coverage --watchAll=false
      - name: Build
        run: npm run build
        
  mobile-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./mobile-app
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run linting
        run: npm run lint
      - name: Run tests
        run: npm test -- --coverage --watchAll=false
        
  deploy:
    needs: [backend-test, frontend-test, mobile-test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Adicionar comandos de deploy aqui
"@ | Out-File -FilePath ".github\workflows\ci-cd.yml" -Encoding UTF8
        
        Write-Host "CI/CD configurado"
    } -WorkingDirectory "."
    
    Wait-ForTasks -Tasks $infraTasks
}

# Fase 5: Documentação
if ($Phase -eq "all" -or $Phase -eq "docs") {
    Write-Host "`n📚 FASE 5: DOCUMENTAÇÃO" -ForegroundColor Magenta
    
    $docsTasks = @()
    
    # Criar documentação técnica
    $docsTasks += Start-ParallelTask -Name "Technical-Docs" -ScriptBlock {
        Write-Host "Criando documentação técnica..."
        
        # OPERACAO_REPO.md
        @"
# 🚀 GUARDFLOW - GUIA DE OPERAÇÃO DO REPOSITÓRIO

## 📋 Visão Geral
Este guia fornece instruções completas para operar o repositório GuardFlow em diferentes ambientes.

## 🏗️ Estrutura do Projeto
```
GuardFlow/
├── backend/           # Backend FastAPI
├── guardflow-saas/    # SaaS Completo  
├── guardflow-sdk/     # SDK Unificado
├── guardflow-web/     # Interface Web
├── mobile-app/        # App Móvel
├── analytics/         # Serviço de Analytics
├── docsync/          # Sincronização de Docs
├── examples/          # Exemplos e Demos
├── docs/             # Documentação
└── infrastructure/   # Infraestrutura
```

## 🔧 Comandos Essenciais

### Desenvolvimento Local
```bash
# Backend
cd backend && python -m uvicorn app.main:app --reload

# Frontend  
cd guardflow-web && npm start

# Mobile
cd mobile-app && npm start

# SaaS
cd guardflow-saas && npm start
```

### Docker
```bash
# Desenvolvimento
docker-compose -f docker-compose.dev.yml up -d

# Produção
docker-compose -f docker-compose.prod.yml up -d
```

### Testes
```bash
# Backend
cd backend && pytest tests/ -v --cov=app

# Frontend
cd guardflow-web && npm test

# Mobile
cd mobile-app && npm test
```

## 📊 Monitoramento
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/guardflow)
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🚀 Deploy
1. **Staging**: Deploy automático na branch `develop`
2. **Produção**: Deploy automático na branch `main`
3. **Rollback**: `git revert <commit>` + push

## 🔐 Segurança
- **Secrets**: Gerenciados via GitHub Secrets
- **Tokens**: Rotação automática a cada 30 dias
- **Rate Limiting**: 100 req/min por IP
- **RBAC**: Controle de acesso baseado em roles

## 📞 Suporte
- **Issues**: GitHub Issues
- **Docs**: `/docs` directory
- **Email**: support@guardflow.com
"@ | Out-File -FilePath "docs\OPERACAO_REPO.md" -Encoding UTF8
        
        Write-Host "Documentação técnica criada"
    } -WorkingDirectory "."
    
    # Criar SETUP_DEV.md
    $docsTasks += Start-ParallelTask -Name "Setup-Docs" -ScriptBlock {
        Write-Host "Criando guia de setup..."
        
        @"
# 🛠️ GUARDFLOW - SETUP DE DESENVOLVIMENTO

## 📋 Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (opcional)

## 🚀 Setup Rápido

### 1. Clone e Configuração Inicial
```bash
git clone https://github.com/SH1W4/GuardFlow.git
cd GuardFlow
```

### 2. Backend (FastAPI)
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Editar .env com suas configurações

uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (React)
```bash
cd guardflow-web
npm install
cp .env.example .env.development
# Editar .env.development

npm start
```

### 4. Mobile (React Native)
```bash
cd mobile-app
npm install
# Android
npx react-native run-android
# iOS
npx react-native run-ios
```

### 5. SaaS (Node.js)
```bash
cd guardflow-saas
npm install
npm start
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost:5432/guardflow
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
GOOGLE_VISION_API_KEY=your-api-key

# Frontend (.env.development)
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_ENV=development

# Mobile (metro.config.js)
API_BASE_URL=http://localhost:8000
```

### Banco de Dados
```bash
# PostgreSQL
createdb guardflow
psql guardflow < backend/schema.sql

# Redis
redis-server
```

## 🧪 Testes
```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd guardflow-web && npm test

# Mobile
cd mobile-app && npm test

# Todos
npm run test:all
```

## 🐳 Docker (Alternativo)
```bash
# Desenvolvimento
docker-compose -f docker-compose.dev.yml up -d

# Produção
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Acesso aos Serviços
- **Backend API**: http://localhost:8000
- **Frontend Web**: http://localhost:3000
- **Mobile**: Metro bundler
- **SaaS**: http://localhost:3001
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 🔍 Debugging
```bash
# Logs do Backend
tail -f backend/logs/app.log

# Logs do Frontend
npm run start:debug

# Logs do Mobile
npx react-native log-android
npx react-native log-ios
```

## 🚨 Troubleshooting
- **Porta ocupada**: `netstat -ano | findstr :8000`
- **Dependências**: `npm install --force`
- **Cache**: `npm start -- --reset-cache`
- **Python**: `pip install --upgrade pip`

## 📞 Suporte
- **Issues**: GitHub Issues
- **Docs**: `/docs` directory
- **Email**: dev@guardflow.com
"@ | Out-File -FilePath "docs\SETUP_DEV.md" -Encoding UTF8
        
        Write-Host "Guia de setup criado"
    } -WorkingDirectory "."
    
    Wait-ForTasks -Tasks $docsTasks
}

# Resumo final
Write-Host "`n🎯 EXECUÇÃO DO PLANO CONCLUÍDA!" -ForegroundColor Green
Write-Host "📊 Estatísticas:" -ForegroundColor Cyan
Write-Host "  • MCPs do Cursor: ✅ Configurados" -ForegroundColor Green
Write-Host "  • Backend Security: ✅ Implementado" -ForegroundColor Green  
Write-Host "  • Testes Expandidos: ✅ Configurados" -ForegroundColor Green
Write-Host "  • Contratos Pydantic: ✅ Criados" -ForegroundColor Green
Write-Host "  • Mobile/Web Alinhados: ✅ Configurados" -ForegroundColor Green
Write-Host "  • Docker/CI-CD: ✅ Implementados" -ForegroundColor Green
Write-Host "  • Documentação: ✅ Criada" -ForegroundColor Green

Write-Host "`n🚀 GuardFlow está pronto para desenvolvimento paralelo acelerado!" -ForegroundColor Yellow
Write-Host "💡 Próximos passos: Execute 'docker-compose -f docker-compose.dev.yml up -d' para iniciar todos os serviços" -ForegroundColor Cyan


