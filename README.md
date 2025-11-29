<div align="center">

# 🛒 Agilize.ai

### Menos fila. Mais vida.

**Tecnologia Ética para o Varejo**

*Powered by GuardFlow Protocol*

---

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Rust](https://img.shields.io/badge/Rust-1.87+-orange.svg)](https://www.rust-lang.org/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)

</div>

---

## 🎯 Sobre o Projeto

**Agilize.ai** é uma plataforma de inteligência artificial ética que transforma a experiência de compra no varejo. Combinamos **blockchain**, **IA** e **ESG** para criar um ecossistema transparente, sustentável e centrado no ser humano.

### 💡 Missão
Simplificar a vida de quem compra e trabalha no varejo através de experiências ágeis, sustentáveis e humanas.

### 🌟 Visão
Ser a ponte entre inovação tecnológica e confiança social no setor de varejo.

---

## 🎨 Identidade Visual

### Paleta de Cores (Sistema ESG)

| Cor | Hex | Significado |
|-----|-----|-------------|
| 🟢 **Verde-Água** | `#31DBC3` | Inteligência simbiótica e confiança |
| 🟡 **Amarelo Solar** | `#FFB911` | Clareza e ação positiva |
| 🔴 **Vermelho Ético** | `#FB4F48` | Energia e movimento |
| ⚫ **Fundo Noturno** | `#0F1421` | Profundidade e foco |

### 🔤 Tipografia
- **Títulos**: Montserrat (Bold)
- **Corpo**: Inter (Regular)
- **Digital**: Manrope (SemiBold)

---

## ⚙️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  • Tailwind CSS + Glassmorphism UI                      │
│  • MetaMask Integration (Web3)                          │
│  • Responsive Design                                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ REST API
                 │
┌────────────────▼────────────────────────────────────────┐
│                  Backend (Rust + Axum)                   │
│  • /api/scan - AI Model Analysis                        │
│  • /health - Health Check                               │
│  • CORS Enabled                                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 │
┌────────────────▼────────────────────────────────────────┐
│              Blockchain (Sepolia Testnet)                │
│  • TrinityGSTToken (0xfb927...5c45)                     │
│  • AET, ECR Token Integration                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Web3**: ethers.js v6
- **State Management**: React Hooks

### Backend
- **Language**: Rust 1.87+
- **Framework**: Axum
- **Runtime**: Tokio
- **Serialization**: Serde
- **Database**: SQLx (planned)

### Blockchain
- **Network**: Ethereum Sepolia Testnet
- **Smart Contracts**: Solidity 0.8.28
- **Tools**: Hardhat, ethers.js

---

## 📦 Instalação

### Pré-requisitos
- Node.js 18+
- Rust 1.87+
- MetaMask (Browser Extension)

### 1. Clone o Repositório
```bash
git clone https://github.com/guardflow-core/guardflow.git
cd guardflow
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Acesse: `http://localhost:5173`

### 3. Backend Setup
```bash
cd backend
cargo build
cargo run
```
API disponível em: `http://localhost:3000`

---

## 🎯 Features

### ✅ Implementado (MVP v0.1)
- [x] Landing Page com Agilize.ai Branding
- [x] Conexão MetaMask (Wallet)
- [x] API REST com endpoint `/api/scan`
- [x] Mock de Análise de IA
- [x] Design System ESG completo
- [x] Brand Book e Assets Visuais

### 🔄 Em Desenvolvimento
- [ ] Integração Frontend ↔ Backend
- [ ] Conexão com Sepolia Testnet
- [ ] Display de Token Balance (AET)
- [ ] Dashboard de Métricas ESG
- [ ] Scan de IA Real (Python Integration)

### 🔮 Roadmap
- [ ] Mainnet Deployment
- [ ] Mobile App (React Native)
- [ ] Parcerias com Redes de Varejo
- [ ] Certificação ESG Automatizada

---

## 🧪 API Endpoints

### `GET /`
Mensagem de boas-vindas.

**Response:**
```json
{
  "message": "Welcome to GuardFlow API"
}
```

### `GET /health`
Health check do servidor.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### `POST /api/scan`
Análise de modelo de IA (mock).

**Request:**
```json
{
  "model_url": "https://example.com/model",
  "scan_type": "bias"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "score": 92,
  "status": "completed",
  "details": {
    "bias_detected": false,
    "fairness_metric": "0.95",
    "timestamp": "2025-11-29T12:00:00Z"
  }
}
```

---

## 🎨 Design Assets

Todos os assets visuais estão disponíveis em `/Design`:
- Brand Book completo
- 13 mockups e apresentações
- Logo variations
- Color palettes
- UI/UX examples

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m ''feat: Add AmazingFeature''`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🔗 Links

- **Website**: [agilize.ai](https://agilize.ai) *(em breve)*
- **Documentation**: [docs.guardflow.io](https://docs.guardflow.io) *(em breve)*
- **Twitter**: [@AgilizeAI](https://twitter.com/AgilizeAI) *(em breve)*

---

## 👥 Time

**GuardFlow Core Team**
- Desenvolvido com ❤️ pela equipe GuardFlow
- Pilot Use Case: Agilize.ai (Retail Tech)

---

<div align="center">

**Agilize.ai** — Menos fila. Mais vida.

*Powered by [GuardFlow Protocol](https://github.com/guardflow-core)*

</div>
