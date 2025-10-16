# 🛒 GuardFlow - Sistema de Checkout ESG Integrado

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

**Sistema de Checkout ESG Integrado ao Ecossistema de Tokenização**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api) • [SDK](#-sdk) • [Contributing](#-contributing)

</div>

## 📋 Overview

GuardFlow é um sistema de checkout ESG integrado que agiliza compras sustentáveis e se conecta ao ecossistema de tokenização ESG. Desenvolvido com foco em experiência de usuário e integração com sistemas de tokenização, oferece checkout rápido, inteligente e conectado ao ecossistema ESG.

### 🌟 Key Features

- **🛒 Checkout Inteligente**: Scanner de produtos com computer vision e reconhecimento automático
- **⚡ Pagamento Rápido**: PIX instantâneo e integração com GuardPass
- **🌱 Integração ESG**: Conexão automática com ecossistema de tokenização ESG
- **📱 Multi-Platform**: Web, mobile e APIs RESTful completas
- **🤖 IA Personalizada**: Ofertas personalizadas baseadas em comportamento sustentável
- **🔗 Integração ERP**: Sincronização com sistemas de mercado (SAP, Oracle, Dynamics)
- **📊 Analytics ESG**: Métricas de impacto ambiental e histórico de compras
- **🏆 Gamificação**: Sistema de badges e recompensas por compras sustentáveis
- **🔄 Ecossistema Conectado**: Integração com tokens GST e monetização governamental
- **📱 Interface Intuitiva**: Qualquer pessoa usa na primeira vez

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React 18+, TypeScript, Tailwind CSS
- **Mobile**: React Native, Expo
- **Database**: SQLite (desenvolvimento), PostgreSQL (produção)
- **AI/ML**: Custom models, NLTK, scikit-learn
- **Blockchain**: Smart contracts ESG, DeFi protocols
- **Infrastructure**: Docker, Docker Compose
- **Monitoring**: Structured logging, Health checks

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ (for frontend)
- Git
- Docker (optional, for containerized deployment)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/SH1W4/guardflow.git
   cd guardflow
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Platform-Specific Setup**
   - **macOS**: See [macOS Setup Guide](docs/getting-started/MACOS_SETUP.md)
   - **Windows**: See [Windows Setup Guide](docs/getting-started/WINDOWS_SETUP.md)
   - **Linux**: See [Linux Setup Guide](docs/getting-started/LINUX_SETUP.md)

4. **Frontend Setup**
   ```bash
   cd guardflow-web
   npm install
   ```

5. **Mobile Setup**
   ```bash
   cd mobile-app
   npm install
   ```

6. **Run the application**
   ```bash
   # Backend
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
   
   # Frontend (new terminal)
   cd guardflow-web
   npm start
   
   # Mobile (new terminal)
   cd mobile-app
   npx expo start
   ```

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# API: http://localhost:8002
# Frontend: http://localhost:3000
# Mobile: Expo Go app
```

## 🚀 Usage

### Checkout Inteligente

Sistema de checkout com scanner automático:

```python
# Example: Processar checkout com scanner
response = requests.post(
    "http://localhost:8002/api/v1/checkout/process",
    json={
        "user_id": "user-123",
        "products": [
            {"barcode": "123456789", "quantity": 2},
            {"barcode": "987654321", "quantity": 1}
        ],
        "payment_method": "pix"
    }
)
result = response.json()
# Returns: Checkout processado, produtos identificados, total calculado
```

### Integração ESG

Conectar checkout ao ecossistema ESG:

```python
# Example: Integrar com tokenização ESG
response = requests.post(
    "http://localhost:8002/api/v1/esg/integrate-checkout",
    json={
        "checkout_id": "CHECKOUT-12345",
        "user_id": "user-123",
        "esg_preferences": ["organic", "sustainable"]
    }
)
result = response.json()
# Returns: Conexão com ecossistema ESG, tokens disponíveis
```

### Analytics ESG

Métricas de impacto das compras:

```python
# Example: Obter analytics ESG
response = requests.get(
    "http://localhost:8002/api/v1/analytics/esg/user-123"
)
analytics = response.json()
# Returns: Impacto ambiental, produtos sustentáveis, histórico ESG
```

## 🎯 GuardFlow SDK

### Ecossistema de Tokenização ESG

O **GuardFlow SDK** é um produto autosuficiente da GuardDrive que implementa o ecossistema completo de tokenização ESG, ao qual o GuardFlow se conecta:

```python
from guardflow_sdk import GuardFlowSDK

# Inicializar SDK autosuficiente
sdk = GuardFlowSDK(api_key="your-key")

# Tokenização ESG
esg_result = sdk.esg.convert_invoice_to_tokens({
    "invoice_id": "INV-123",
    "amount": 1000,
    "esg_score": 85,
    "products": [{"name": "Produto Orgânico", "sustainable": True}]
})

# Monetização governamental
gov_result = sdk.monetization.process_government_credits({
    "invoice_id": "INV-123",
    "amount": 1000,
    "tax_credits": ["ICMS", "IPI", "PIS_COFINS"]
})

# ESG Asset Token (Estratégia Inteligente)
asset_result = sdk.esg_asset.mint_from_invoice({
    "invoice_number": "NF-123",
    "amount": 2000,
    "products": [{"name": "Produto ESG", "sustainable": True}]
})

# Staking ESG
staking_result = sdk.esg_asset.stake_for_rewards(
    asset_result['asset_id'], 1000, 90
)

# DeFi Liquidity Pools
pool_result = sdk.liquidity_pools.create_esg_pool({
    "type": "esg_gst",
    "token_a": "ESG",
    "token_b": "GST",
    "initial_liquidity": 10000
})
```

### Módulos do SDK (Ecossistema ESG)

- **🌱 ESG Engine** - Tokenização ESG autônoma
- **🏛️ Government Monetization** - Créditos fiscais automáticos
- **🤖 AI Services** - Personalização e analytics
- **🔗 ERP Connectors** - Integração com mercados
- **⛓️ Blockchain Bridge** - Smart contracts ESG
- **🪙 GST Ecosystem** - Sistema de tokens completo
- **🎨 NFT System** - Colecionabilidade ESG
- **🧠 ESG Asset Token** - Estratégia inteligente
- **📜 Smart Contracts** - Deploy automático
- **💧 Liquidity Pools** - DeFi ESG

### Integração GuardFlow ↔ SDK

O GuardFlow se conecta ao SDK para:
- **Tokenização automática** de compras ESG
- **Monetização governamental** de notas fiscais
- **Analytics ESG** personalizados
- **Gamificação** com tokens GST
- **Blockchain integration** para registros imutáveis

## 📖 Documentation

### Architecture

```
guardflow/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── monetization.py      # ESG monetization
│   │   │   ├── esg_dashboard.py     # ESG dashboard
│   │   │   ├── esg_gamification.py # ESG gamification
│   │   │   └── government_monetization.py # Tax credits
│   │   ├── models/         # Database models
│   │   └── main.py         # FastAPI application
│   └── requirements.txt   # Python dependencies
├── guardflow-web/         # React frontend
│   ├── src/               # React source
│   └── package.json       # Dependencies
├── mobile-app/            # React Native mobile
│   ├── src/               # Mobile source
│   └── package.json       # Dependencies
├── docs/                  # Documentation
└── examples/              # Usage examples
```

### Core Components

#### ESG Tokenization Engine
Advanced ESG calculation with sustainability and carbon bonuses:
- Base ESG score (40-90%)
- Sustainability bonus (+5% per green product)
- Carbon bonus (+15% for low carbon footprint)
- Maximum: 100% of purchase value

#### Government Monetization
Automated tax credit processing:
- ICMS: 18% of invoice value
- IPI: 15% of invoice value
- PIS/COFINS: 3.65% of invoice value
- Lei do Bem: 20% of R&D investment
- Lei da Informática: 15% of invoice value

#### ESG Gamification System
Engagement through gamification:
- Badges with specific criteria
- Challenges with token rewards
- Leaderboards by period
- ESG levels (Novato → Mestre ESG)

## 🔌 API Reference

### ESG Endpoints

#### `GET /api/v1/esg/dashboard/{user_id}`
Get comprehensive ESG dashboard for user

**Response:**
```json
{
  "success": true,
  "data": {
    "total_esg_tokens": 1250,
    "total_esg_value_converted": 5000.00,
    "total_carbon_offset_kg": 150.5,
    "num_esg_assets": 12,
    "recent_esg_conversions": [...],
    "ranking_position": 15,
    "esg_level": "Intermediário ESG"
  }
}
```

#### `POST /api/v1/esg/challenges/join`
Join an ESG challenge

**Request:**
```json
{
  "challenge_id": "challenge_1",
  "user_id": "user-123"
}
```

#### `GET /api/v1/esg/leaderboard`
Get ESG leaderboard by period

**Query Parameters:**
- `period`: daily, weekly, monthly, yearly
- `limit`: number of results (default: 50)

### Monetization Endpoints

#### `POST /api/v1/monetization/invoice/convert-to-esg`
Convert invoice to ESG tokens

**Request:**
```json
{
  "invoice_id": "INV-12345",
  "user_id": "user-123",
  "sustainability_score": 85,
  "carbon_footprint_kg": 2.5,
  "products": [
    {
      "name": "Produto Orgânico",
      "category": "Alimentos",
      "sustainable": true
    }
  ]
}
```

#### `POST /api/v1/government/invoice/authorize-government-monetization`
Process government tax credits

**Request:**
```json
{
  "invoice_id": "INV-12345",
  "user_id": "user-123",
  "invoice_amount": 1000.00,
  "tax_credits": ["ICMS", "IPI", "PIS_COFINS"],
  "company_cnpj": "12.345.678/0001-90"
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python test_esg_implementation.py

# Run backend tests
cd backend
pytest

# Run frontend tests
cd guardflow-web
npm test

# Run mobile tests
cd mobile-app
npm test
```

## 📊 Performance

- **ESG Calculation**: ~50ms per transaction
- **Government Monetization**: ~200ms per invoice
- **Dashboard Loading**: <500ms for full metrics
- **API Response**: <100ms average
- **Memory Usage**: <1GB typical
- **Supported Formats**: JSON, CSV, PDF

## 🛣️ Roadmap

### Phase 1: Core ESG (✅ Completed)
- [x] ESG tokenization system
- [x] Government monetization
- [x] ESG dashboard
- [x] Gamification system
- [x] RESTful APIs

### Phase 2: Market Integration (🔄 In Progress)
- [ ] ERP integration (SAP, Oracle, Microsoft Dynamics)
- [ ] Market partnerships (Carrefour, Walmart, etc.)
- [ ] Advanced AI services
- [ ] Mobile app optimization

### Phase 3: Ecosystem Expansion (📋 Planned)
- [ ] International expansion
- [ ] Advanced analytics
- [ ] Blockchain integration
- [ ] Enterprise features

## 💰 Business Model

### Revenue Sources
1. **ESG Tokenization**: 2-5% fee on tokenized value
2. **Government Monetization**: 10-15% of tax credits
3. **AI Services**: Subscription-based pricing
4. **Market Licensing**: Technology licensing fees
5. **Transaction Fees**: Per-transaction charges

### Market Potential
- **TAM**: R$ 100 billion/month (Brazilian supermarkets)
- **SAM**: R$ 25 billion/month (ERP-enabled markets)
- **SOM**: R$ 5 billion/month (partner markets)

### Revenue Projections
- **Year 1**: R$ 1M/month (10 markets, 1K users each)
- **Year 2**: R$ 18.75M/month (25 markets, 5K users each)
- **Year 3**: R$ 50M/month (50+ markets, 10K users each)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run linting
flake8 backend/
black backend/

# Run tests with coverage
pytest --cov=backend tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **SH1W4** - *Initial work* - [GitHub](https://github.com/SH1W4)

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- React team for the robust frontend ecosystem
- All contributors and testers
- Brazilian sustainability initiatives

## 📞 Support

- **Documentation**: [docs.guardflow.com](https://docs.guardflow.com)
- **Issues**: [GitHub Issues](https://github.com/SH1W4/guardflow/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SH1W4/guardflow/discussions)
- **Email**: support@guardflow.com

---

<div align="center">
Made with 🌱 by SH1W4 | Transforming sustainability into value
</div>