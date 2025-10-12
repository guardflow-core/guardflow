# 🛒 **GUARDFLOW**
## **Sistema de Checkout Inteligente para Varejo**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python-lang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![React Native](https://img.shields.io/badge/React%20Native-0.72.6-blue.svg)](https://reactnative.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-green.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-85%25%20Implemented-orange.svg)](https://github.com/SH1W4/GuardFlow)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](https://github.com/SH1W4/GuardFlow/releases)

---

## 🎯 **VISÃO GERAL**

O **GuardFlow** é um sistema de checkout inteligente para varejo que transforma a experiência de compras através de scanner de produtos com IA, pagamentos PIX instantâneos, sistema ESG integrado e tokenização de transações. Projetado para "agilizar suas compras!" com tecnologia de ponta.

### **Características Principais:**
- 📱 **Scanner com IA** - Reconhecimento de produtos via Google Vision API
- 💳 **Checkout Inteligente** - Processamento rápido e sem filas
- 🌱 **Sistema ESG** - Integração de métricas de sustentabilidade
- 🪙 **Tokenização** - Conversão de transações em tokens digitais
- 📊 **Analytics ESG** - Dashboards e insights de sustentabilidade
- 🔐 **Segurança Enterprise** - Autenticação biométrica e JWT
- 🚀 **Multiplataforma** - Web, Mobile (iOS/Android) e API
- 🏛️ **Monetização Governamental** - Créditos fiscais e incentivos

---

## 🏗️ **ARQUITETURA**

### **GuardFlow Checkout System Architecture:**

```mermaid
graph TB
    subgraph "📱 Client Layer"
        A[Web Dashboard] --> B[Mobile App]
        B --> C[Scanner Interface]
    end
    
    subgraph "🔌 API Layer"
        D[FastAPI Backend] --> E[JWT Authentication]
        E --> F[GuardPass Integration]
    end
    
    subgraph "🧠 AI/ML Layer"
        G[Google Vision API] --> H[Product Recognition]
        H --> I[ESG Analytics]
    end
    
    subgraph "💳 Payment Layer"
        J[PIX Processing] --> K[Mercado Pago]
        K --> L[Tokenization]
    end
    
    subgraph "📊 Data Layer"
        M[PostgreSQL] --> N[Redis Cache]
        N --> O[Blockchain Storage]
    end
    
    A --> D
    D --> G
    G --> J
    J --> M
```

---

## 🚀 **INSTALAÇÃO E CONFIGURAÇÃO**

### **Pré-requisitos:**
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (opcional)

### **Quick Start:**

1. **Clone o repositório**
   ```bash
   git clone https://github.com/SH1W4/GuardFlow.git
   cd GuardFlow
   ```

2. **Backend (FastAPI)**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
   ```

3. **Frontend (React)**
   ```bash
   cd guardflow-web
   npm install
   npm start
   ```

4. **Mobile (React Native)**
   ```bash
   cd mobile-app
   npm install
   npx react-native run-android
   # ou
   npx react-native run-ios
   ```

5. **Testar sistema**
   ```bash
   # Backend API
   curl http://localhost:8002/health
   
   # Frontend Web
   http://localhost:3000
   
   # API Documentation
   http://localhost:8002/docs
   ```

---

## 🔌 **INTEGRAÇÃO**

### **Integração com Scanner de Produtos:**

```python
# Exemplo de integração com scanner
from guardflow import GuardFlowClient

client = GuardFlowClient(api_key="your-api-key")

# Escanear produto
result = client.scan_product({
    "image": "base64_encoded_image",
    "store_id": "STORE-123",
    "user_id": "USER-456"
})
```

### **Integração com Monetização Governamental + GST:**

```python
# Exemplo de integração com monetização governamental + tokens GST
result = client.authorize_government_monetization({
    "invoice_id": "INV-789",
    "customer_id": "CUST-123",
    "store_id": "STORE-456",
    "incentives": ["ICMS", "IPI", "PIS_COFINS"],
    "gst_tokens": True,  # Cliente recebe 30% em tokens GST
    "token_conversion": "automatic"  # Conversão automática
})
```

### **Integração com Sistema ESG:**

```python
# Exemplo de integração ESG
result = client.calculate_esg_score({
    "transaction_id": "TXN-123",
    "products": [
        {"id": "PROD-123", "esg_rating": 8.5}
    ],
    "store_id": "STORE-456"
})
```

---

## 📊 **API ENDPOINTS**

### **Scanner Endpoints:**
- `POST /api/v1/scanner/scan` - Escanear produto
- `GET /api/v1/scanner/products` - Listar produtos escaneados
- `POST /api/v1/scanner/populate-products` - Popular dados de teste

### **Monetization Endpoints:**
- `POST /api/v1/monetization/authorize-government-monetization` - Autorizar monetização governamental
- `GET /api/v1/monetization/available-incentives` - Incentivos fiscais disponíveis
- `POST /api/v1/monetization/authorize-service-payment` - Pagamento por serviço
- `GET /api/v1/monetization/monetization-potential` - Potencial de monetização
- `POST /api/v1/gst/convert-to-tokens` - Converter valor em tokens GST
- `GET /api/v1/gst/token-balance/{user_id}` - Saldo de tokens GST do usuário

### **Cart Endpoints:**
- `GET /api/v1/cart/` - Obter carrinho
- `POST /api/v1/cart/add` - Adicionar item ao carrinho
- `DELETE /api/v1/cart/remove` - Remover item do carrinho

### **ESG Endpoints:**
- `GET /api/v1/esg/dashboard` - Dashboard ESG
- `POST /api/v1/esg/calculate` - Calcular score ESG
- `GET /api/v1/esg/gamification` - Sistema de gamificação

### **Store Endpoints:**
- `GET /api/v1/stores/` - Listar lojas
- `GET /api/v1/stores/{id}/products` - Produtos da loja
- `POST /api/v1/stores/populate-stores` - Popular lojas de teste

---

## 🧪 **TESTING**

### **Testes Automatizados:**
```bash
# Executar todos os testes do backend
cd backend
pytest
```

### **Testes Manuais:**
```bash
# Health check
curl http://localhost:8002/health

# Listar produtos
curl http://localhost:8002/api/v1/retail/products
```

---

## 🛣️ **ROADMAP**

### **Fase 1: MVP (✅ 85% Concluída)**
- [x] Backend FastAPI (90% funcional)
- [x] Mobile React Native (85% funcional)
- [x] Frontend React (70% funcional)
- [x] Sistema de autenticação JWT
- [x] Scanner com Google Vision API
- [x] Pagamentos PIX integrados
- [x] Sistema ESG implementado
- [x] Documentação completa

### **Fase 2: Finalização (🔄 Em Progresso)**
- [ ] Conectar mobile ao backend
- [ ] Completar frontend web
- [ ] Testes E2E completos
- [ ] Deploy em produção
- [ ] Demo funcional

### **Fase 3: Expansão (📋 Planejado)**
- [ ] 10 mercados ativos
- [ ] 1.000 usuários ativos
- [ ] Monetização governamental ativa
- [ ] Ecossistema ESG completo
- [ ] IA avançada para ESG

---

## 💰 **MODELO DE MONETIZAÇÃO**

### **🏛️ Monetização Governamental (Principal)**
- **Créditos fiscais** das notas fiscais (ICMS, IPI, PIS/COFINS)
- **Incentivos tributários** do governo (Lei do Bem, Lei de Informática)
- **Cliente recebe 30%** do valor gerado **em tokens GST**
- **GuardFlow recebe 70%** como taxa de serviço
- **Integração GST** - Conversão automática em tokens do ecossistema

### **🛒 Pagamento por Serviço**
- **Plano Básico (10%)**: Escaneamento + cálculo básico
- **Plano Padrão (15%)**: Serviço completo + ESG (RECOMENDADO)
- **Plano Premium (20%)**: Tudo + GuardPass + prioridade

### **📊 Licenciamento de Tecnologia**
- **Licença base**: R$ 2.000/mês por mercado
- **Volume**: R$ 0,50 por transação processada
- **ESG Bonus**: R$ 0,20 por transação ESG
- **Analytics**: R$ 500/mês por dashboard avançado

### **🪙 Integração GST (Governance & Sustainability Tokens)**
- **30% do valor** convertido automaticamente em tokens GST
- **Tokens utilizáveis** no ecossistema ESG
- **Gamificação** com recompensas sustentáveis
- **Governança** tokenizada do sistema
- **Marketplace** de tokens ESG

### **🎯 Princípio Não-Invasivo**
- **NUNCA interferimos** no fluxo de caixa dos mercados
- **Tecnologia como serviço** (SaaS)
- **Valor agregado** sem interferência financeira
- **Compliance** total com LGPD e regulamentações

---

## 🔗 **PROJETOS INTEGRADOS**

### **🪙 Ecossistema GST (Governance & Sustainability Tokens)**
- **[ecosystem-gst](https://github.com/SH1W4/ecosystem-gst)** - Smart contracts e tokens GST
- **[ecosystem-degov](https://github.com/SH1W4/ecosystem-degov)** - Backend Rust para ESG Token Ecosystem
- **Integração completa** - 30% do valor em tokens GST automáticos

### **🔧 Frameworks de Desenvolvimento**
- **[Selfbelt](https://github.com/SH1W4/selfbelt)** - Plataforma de telemetria
- **[Manus Framework](https://github.com/SH1W4/manus)** - Framework de desenvolvimento
- **[EON Framework](https://github.com/SH1W4/eon)** - Framework de integração

---

## 🤝 **CONTRIBUTING**

Agradecemos contribuições! Por favor, veja nosso [Guia de Contribuição](CONTRIBUTING.md) para detalhes.

1. Fork o repositório
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### **Development Setup:**

```bash
# Instalar dependências do backend
cd backend
pip install -r requirements.txt

# Instalar dependências do frontend
cd ../guardflow-web
npm install

# Instalar dependências do mobile
cd ../mobile-app
npm install
```

---

## 📄 **LICENSE**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 **TEAM**

- **SH1W4** - *Initial work* - [GitHub](https://github.com/SH1W4)

---

## 🙏 **ACKNOWLEDGMENTS**

- Comunidade Python e FastAPI
- Comunidade React e React Native
- Desenvolvedores de código aberto
- Todos os contribuidores e testadores

---

## 📞 **SUPPORT**

- **Documentação**: [docs.guardflow.com](https://docs.guardflow.com)
- **Issues**: [GitHub Issues](https://github.com/SH1W4/GuardFlow/issues)
- **Email**: support@guardflow.com
- **Discord**: [GuardFlow Community](https://discord.gg/guardflow)

---

<div align="center">
Made with 🛒 by SH1W4 | Agiliza aí suas compras!<br/>
Sistema de Checkout Inteligente para Varejo
</div>