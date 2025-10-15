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


