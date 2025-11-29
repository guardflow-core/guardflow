# 🔗 **{{SERVICE_NAME}} - Blockchain Service**

[![Blockchain](https://img.shields.io/badge/Blockchain-{{BLOCKCHAIN_TYPE}}-purple.svg)]({{BLOCKCHAIN_URL}})
[![ESG Token](https://img.shields.io/badge/ESG%20Token-{{VERSION}}-green.svg)](https://github.com/SH1W4/ecosystem-degov)
[![Status](https://img.shields.io/badge/Status-{{STATUS}}-{{STATUS_COLOR}}.svg)]({{PROJECT_URL}})

---

## 🎯 **VISÃO GERAL**

O **{{SERVICE_NAME}}** é um serviço blockchain integrado ao **ESG Token Ecosystem**, implementando {{BLOCKCHAIN_TYPE}} para {{FUNCTIONS}}.

### **Características Principais:**
- 🔗 **Blockchain Híbrida** - Privada (Hyperledger Besu) + Pública ({{BLOCKCHAIN_TYPE}})
- 🪙 **6 Tokens ESG** - EcoToken, EcoScore, CarbonCredit, EcoCertificate, EcoStake, EcoGem
- 🔒 **Smart Contracts** - Contratos inteligentes seguros e auditados
- ⚡ **High Performance** - Transações rápidas e escaláveis
- 🌐 **Cross-Chain** - Interoperabilidade entre blockchains

---

## 🏗️ **ARQUITETURA BLOCKCHAIN**

### **Stack Tecnológico:**
- **Blockchain**: {{BLOCKCHAIN_TYPE}}
- **Smart Contracts**: Solidity
- **Network**: {{NETWORK}}
- **Consensus**: Proof of Stake
- **Storage**: IPFS + Blockchain

### **Diagrama de Arquitetura:**

```mermaid
graph TB
    subgraph "🔗 Blockchain Layer"
        A[{{BLOCKCHAIN_TYPE}} Network] --> B[Smart Contracts]
        B --> C[Token Contracts]
        C --> D[Marketplace Contracts]
        D --> E[Governance Contracts]
    end
    
    subgraph "🪙 Token Contracts"
        F[EcoToken ECT<br/>ERC-20] --> G[EcoScore ECS<br/>ERC-1155]
        G --> H[CarbonCredit CCR<br/>ERC-1155]
        H --> I[EcoCertificate ECR<br/>ERC-721]
        I --> J[EcoStake EST<br/>ERC-20]
        J --> K[EcoGem EGM<br/>ERC-20]
    end
    
    subgraph "🔌 Integration Layer"
        L[ESG Token Backend] --> M[Blockchain API]
        M --> N[Smart Contract Interface]
        N --> O[Token Management]
    end
    
    subgraph "📊 Analytics Layer"
        P[Blockchain Analytics] --> Q[Token Metrics]
        Q --> R[Transaction Insights]
        R --> S[Performance Monitoring]
    end
    
    A --> F
    L --> A
    P --> A
```

---

## 🚀 **CONFIGURAÇÃO**

### **Pré-requisitos:**
- {{PREREQUISITES}}

### **Instalação:**
```bash
# Clone o repositório
git clone {{REPO_URL}}
cd {{PROJECT_NAME}}

# Instale as dependências
npm install
# ou
yarn install

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Compile os contratos
npm run compile
# ou
yarn compile

# Execute os testes
npm run test
# ou
yarn test
```

### **Configuração de Rede:**
```javascript
// hardhat.config.js
module.exports = {
  networks: {
    {{NETWORK}}_mainnet: {
      url: "{{RPC_URL}}",
      accounts: [process.env.PRIVATE_KEY],
      gasPrice: {{GAS_PRICE}},
      gas: {{GAS_LIMIT}}
    },
    {{NETWORK}}_testnet: {
      url: "{{TESTNET_RPC_URL}}",
      accounts: [process.env.PRIVATE_KEY],
      gasPrice: {{TESTNET_GAS_PRICE}},
      gas: {{TESTNET_GAS_LIMIT}}
    }
  },
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  }
};
```

---

## 📋 **SMART CONTRACTS**

### **Contratos Implementados:**

#### **1. EcoToken (ECT) - ERC-20**
```solidity
// EcoToken.sol
contract EcoToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18; // 1 bilhão
    uint256 public constant INITIAL_SUPPLY = 100_000_000 * 10**18; // 100 milhões
    
    constructor() ERC20("EcoToken", "ECT") {
        _mint(msg.sender, INITIAL_SUPPLY);
    }
    
    function mint(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Max supply exceeded");
        _mint(to, amount);
    }
    
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
}
```

#### **2. EcoScore (ECS) - ERC-1155**
```solidity
// EcoScore.sol
contract EcoScore is ERC1155, Ownable {
    mapping(uint256 => EcoScoreData) public ecoScores;
    
    struct EcoScoreData {
        uint256 score;
        uint256 level;
        string category;
        uint256 timestamp;
    }
    
    function mintEcoScore(
        address to,
        uint256 id,
        uint256 score,
        string memory category
    ) external onlyOwner {
        ecoScores[id] = EcoScoreData({
            score: score,
            level: calculateLevel(score),
            category: category,
            timestamp: block.timestamp
        });
        
        _mint(to, id, 1, "");
    }
}
```

#### **3. CarbonCredit (CCR) - ERC-1155**
```solidity
// CarbonCredit.sol
contract CarbonCredit is ERC1155, Ownable {
    mapping(uint256 => CarbonCreditData) public carbonCredits;
    
    struct CarbonCreditData {
        uint256 amount; // kg CO2
        string verification;
        uint256 vintage;
        string project;
    }
    
    function mintCarbonCredit(
        address to,
        uint256 id,
        uint256 amount,
        string memory verification,
        string memory project
    ) external onlyOwner {
        carbonCredits[id] = CarbonCreditData({
            amount: amount,
            verification: verification,
            vintage: block.timestamp,
            project: project
        });
        
        _mint(to, id, amount, "");
    }
}
```

#### **4. EcoCertificate (ECR) - ERC-721**
```solidity
// EcoCertificate.sol
contract EcoCertificate is ERC721, Ownable {
    mapping(uint256 => CertificateData) public certificates;
    
    struct CertificateData {
        string title;
        string description;
        uint256 level;
        string issuer;
        uint256 timestamp;
    }
    
    function mintCertificate(
        address to,
        uint256 tokenId,
        string memory title,
        string memory description,
        uint256 level,
        string memory issuer
    ) external onlyOwner {
        certificates[tokenId] = CertificateData({
            title: title,
            description: description,
            level: level,
            issuer: issuer,
            timestamp: block.timestamp
        });
        
        _mint(to, tokenId);
    }
}
```

#### **5. EcoStake (EST) - ERC-20**
```solidity
// EcoStake.sol
contract EcoStake is ERC20, Ownable {
    mapping(address => StakingData) public stakingData;
    
    struct StakingData {
        uint256 amount;
        uint256 timestamp;
        uint256 tier;
    }
    
    function stake(uint256 amount) external {
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");
        
        stakingData[msg.sender] = StakingData({
            amount: amount,
            timestamp: block.timestamp,
            tier: calculateTier(amount)
        });
        
        _transfer(msg.sender, address(this), amount);
    }
}
```

#### **6. EcoGem (EGM) - ERC-20**
```solidity
// EcoGem.sol
contract EcoGem is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 10_000_000 * 10**18; // 10 milhões
    mapping(address => bool) public premiumMembers;
    
    function mintEcoGem(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Max supply exceeded");
        _mint(to, amount);
    }
    
    function setPremiumMember(address user, bool status) external onlyOwner {
        premiumMembers[user] = status;
    }
}
```

---

## 🔌 **API ENDPOINTS**

### **Blockchain Service Endpoints:**
- `GET /api/v1/blockchain/health` - Saúde da rede blockchain
- `GET /api/v1/blockchain/status` - Status dos contratos
- `POST /api/v1/blockchain/deploy` - Deploy de contratos
- `GET /api/v1/blockchain/transactions/{hash}` - Detalhes da transação

### **Token Management Endpoints:**
- `GET /api/v1/tokens/balance/{address}` - Saldo de tokens
- `POST /api/v1/tokens/transfer` - Transferir tokens
- `POST /api/v1/tokens/mint` - Mintar tokens
- `POST /api/v1/tokens/burn` - Queimar tokens

### **Smart Contract Endpoints:**
- `GET /api/v1/contracts/{address}` - Informações do contrato
- `POST /api/v1/contracts/call` - Chamar função do contrato
- `GET /api/v1/contracts/events` - Eventos do contrato

---

## 🧪 **TESTES**

### **Testes de Smart Contracts:**
```bash
# Testar todos os contratos
npm run test:contracts

# Testar contratos específicos
npm run test:EcoToken
npm run test:EcoScore
npm run test:CarbonCredit
npm run test:EcoCertificate
npm run test:EcoStake
npm run test:EcoGem

# Testar integração
npm run test:integration
```

### **Testes de Deploy:**
```bash
# Deploy em testnet
npm run deploy:testnet

# Deploy em mainnet
npm run deploy:mainnet

# Verificar deploy
npm run verify:contracts
```

---

## 📊 **MONITORAMENTO**

### **Métricas de Blockchain:**
- **Block Height**: {{BLOCK_HEIGHT}}
- **Gas Price**: {{GAS_PRICE}} Gwei
- **Transaction Count**: {{TX_COUNT}}
- **Contract Calls**: {{CONTRACT_CALLS}}

### **Métricas de Tokens:**
- **Total Supply**: {{TOTAL_SUPPLY}}
- **Circulating Supply**: {{CIRCULATING_SUPPLY}}
- **Token Transfers**: {{TOKEN_TRANSFERS}}
- **Active Addresses**: {{ACTIVE_ADDRESSES}}

---

## 🔒 **SEGURANÇA**

### **Auditoria de Segurança:**
- **Smart Contract Audit**: ✅ Concluída
- **Penetration Testing**: ✅ Concluída
- **Code Review**: ✅ Concluída
- **Vulnerability Assessment**: ✅ Concluída

### **Medidas de Segurança:**
- **Access Control**: Controle de acesso baseado em roles
- **Reentrancy Protection**: Proteção contra ataques de reentrância
- **Integer Overflow**: Proteção contra overflow de inteiros
- **Gas Optimization**: Otimização de gas para eficiência

---

## 🛣️ **ROADMAP**

### **Próximas Funcionalidades:**
- [ ] **v{{NEXT_VERSION}}** - {{NEXT_FEATURES}}
- [ ] **v{{FUTURE_VERSION}}** - {{FUTURE_FEATURES}}

### **Melhorias Planejadas:**
- [ ] {{IMPROVEMENT_1}}
- [ ] {{IMPROVEMENT_2}}
- [ ] {{IMPROVEMENT_3}}

---

## 📞 **SUPORTE**

- **Documentação**: [docs/](docs/)
- **Issues**: [GitHub Issues]({{ISSUES_URL}})
- **Discord**: [ESG Token Community](https://discord.gg/esg-token)
- **Email**: {{SUPPORT_EMAIL}}

---

**Desenvolvido com ❤️ para o ESG Token Ecosystem**




