## GuardFlow - Desenvolvimento (MVP)

## 📋 Visão Geral do Projeto

O GuardFlow é um sistema de checkout inteligente integrado ao GuardPass. Este documento foca no MVP executável localmente e nos passos para teste rápido no navegador.

1. **Rail A**: Sistema de pagamentos instantâneos (entrada "inocente")
2. **Rail B**: Infraestrutura GuardPass (domínio estratégico)

## ⚙️ Execução rápida (local)

Pré‑requisitos
- Python 3.11
- Windows PowerShell

Passos
1) Iniciar backend (porta 8002)
```
cd GuardFlow\backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8002 --reload
```

2) Abrir Swagger (dev)
- Acesse: http://127.0.0.1:8002/docs

3) Login e autenticação
- Endpoint: POST /api/v1/auth/login
- Body exemplo:
```
{
  "email": "teste@guardpass.com",
  "password": "senha123"
}
```
- Copie o access_token retornado e clique em "Authorize" no Swagger: `Bearer SEU_TOKEN`

4) Popular dados de demonstração
- Produtos: POST /api/v1/scanner/populate-products
- Lojas:    POST /api/v1/stores/populate-stores

5) Fluxo de compra (end‑to‑end)
- Listar lojas: GET /api/v1/stores/
  - copie `id` da loja
- Criar/obter carrinho: GET /api/v1/cart/?store_id=ID_DA_LOJA
  - copie `data.cart.id`
- Listar produtos da loja: GET /api/v1/stores/{store_id}/products
- Adicionar item: POST /api/v1/cart/add?product_id=ID_DO_PRODUTO&quantity=1&store_id=ID_DA_LOJA
- Criar PIX: POST /api/v1/payment/create-pix?cart_id=ID_DO_CARRINHO
- Status PIX: GET /api/v1/payment/status/{transaction_id}
- (Opcional) Confirmar: POST /api/v1/payment/confirm/{transaction_id}

Observações
- Banco local SQLite: `backend/guardflow_dev.db`
- UUID no SQLite: ajustado para string (ex.: `Product.id`) para evitar erro de bind
- Porta padrão dev: 8002

## 🏗️ Arquitetura Técnica

### Frontend (Interface do Usuário)
- **HTML5**: Estrutura semântica moderna
- **CSS3**: Design responsivo e acessível
- **JavaScript ES6+**: Lógica de negócio e interações
- **PWA**: Capacidades de aplicativo web

### Backend (Infraestrutura)
- **FastAPI**: API assíncrona de alta performance
- **PostgreSQL**: Banco de dados principal
- **Redis**: Cache e sessões
- **Docker**: Containerização

### Blockchain & Tokenização
- **Ethereum/Polygon**: Rede principal
- **Smart Contracts**: Lógica de tokenização
- **IPFS**: Armazenamento descentralizado
- **Web3.js**: Integração blockchain

## 🔧 Stack Tecnológica Recomendada

### Core Framework
```python
# FastAPI - API assíncrona
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from redis import Redis
```

### Banco de Dados
```sql
-- PostgreSQL - Estrutura principal
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    amount DECIMAL(18,2),
    tokenized_nfe_id UUID,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Cache e Sessões
```python
# Redis - Cache distribuído
import redis
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)
```

## 🎯 Funcionalidades Principais

### 1. Sistema de Pagamentos (Rail A)
- **QR Code Generation**: Geração dinâmica de QR codes
- **Multi-payment**: Suporte a múltiplas formas de pagamento
- **Real-time**: Processamento em tempo real
- **Cashback**: Sistema de recompensas

### 2. Tokenização (Rail B)
- **NFe NFTs**: Tokenização de notas fiscais
- **ESG Data**: Integração de dados de sustentabilidade
- **Smart Contracts**: Automação de processos
- **Marketplace**: Troca de tokens

### 3. Integração GuardPass
- **API Gateway**: Ponto único de entrada
- **Authentication**: Sistema de autenticação
- **Rate Limiting**: Controle de taxa
- **Monitoring**: Monitoramento em tempo real

## 🔐 Segurança e Compliance

### Autenticação
- **OAuth 2.0**: Padrão de autenticação
- **JWT Tokens**: Tokens seguros
- **2FA**: Autenticação de dois fatores
- **Biometric**: Integração biométrica

### Compliance
- **LGPD**: Conformidade com lei brasileira
- **PCI DSS**: Segurança de dados de pagamento
- **GDPR**: Proteção de dados europeia
- **Audit Logs**: Logs de auditoria

## 📊 Monitoramento e Métricas

### Métricas de Negócio
- **Transaction Volume**: Volume de transações
- **User Adoption**: Taxa de adoção
- **Revenue**: Receita gerada
- **ESG Impact**: Impacto ESG

### Métricas Técnicas
- **API Response Time**: Tempo de resposta
- **Error Rate**: Taxa de erro
- **Uptime**: Tempo de atividade
- **Throughput**: Taxa de processamento

## 🚀 Estratégia de Implementação

### Fase 1: MVP (3 meses)
- [ ] Interface básica
- [ ] Sistema de pagamentos
- [ ] Integração com bancos
- [ ] Testes iniciais

### Fase 2: Tokenização (6 meses)
- [ ] Smart contracts
- [ ] NFT de NFe
- [ ] Marketplace básico
- [ ] Integração ESG

### Fase 3: Domínio (12 meses)
- [ ] Infraestrutura GuardPass
- [ ] Integração municipal
- [ ] Expansão geográfica
- [ ] Monetização completa

## 🔗 Integração com Ecossistema

### GUARDRIVE Core
- **Shared Services**: Serviços compartilhados
- **Common Auth**: Autenticação unificada
- **Data Sync**: Sincronização de dados
- **Event Bus**: Sistema de eventos

### GUARDRIVE-SDK
- **SDK Integration**: Integração com SDK
- **API Wrappers**: Wrappers de API
- **Testing Tools**: Ferramentas de teste
- **Documentation**: Documentação

### GUARDRIVE-MCP
- **Model Context**: Protocolo de contexto
- **Agent Integration**: Integração com agentes
- **Workflow Automation**: Automação de fluxos
- **Knowledge Base**: Base de conhecimento

## 📈 Roadmap de Desenvolvimento

### Q1 2024
- [ ] Arquitetura base
- [ ] Interface MVP
- [ ] Integração bancária
- [ ] Testes iniciais

### Q2 2024
- [ ] Sistema de tokenização
- [ ] Smart contracts
- [ ] Integração ESG
- [ ] Beta testing

### Q3 2024
- [ ] Infraestrutura GuardPass
- [ ] Integração municipal
- [ ] Expansão geográfica
- [ ] Monetização

### Q4 2024
- [ ] Domínio completo
- [ ] Expansão internacional
- [ ] Otimizações
- [ ] Escalabilidade

## 🧪 Estratégia de Testes

### Testes Unitários
- **Coverage**: 90%+ de cobertura
- **Frameworks**: pytest, jest
- **CI/CD**: Integração contínua
- **Quality Gates**: Portões de qualidade

### Testes de Integração
- **API Testing**: Testes de API
- **Database Testing**: Testes de banco
- **External Services**: Serviços externos
- **Performance**: Testes de performance

### Testes de Segurança
- **Penetration Testing**: Testes de penetração
- **Vulnerability Scanning**: Varredura de vulnerabilidades
- **Code Analysis**: Análise de código
- **Dependency Check**: Verificação de dependências

## 📚 Documentação

### Técnica
- **API Documentation**: Documentação de API
- **Architecture**: Documentação de arquitetura
- **Deployment**: Guias de deploy
- **Troubleshooting**: Solução de problemas

### Usuário
- **User Guide**: Guia do usuário
- **FAQ**: Perguntas frequentes
- **Video Tutorials**: Tutoriais em vídeo
- **Support**: Suporte técnico

---

*Documentação técnica do GuardFlow - Sistema de Economia Urbana Tokenizada*
