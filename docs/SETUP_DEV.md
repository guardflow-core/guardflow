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