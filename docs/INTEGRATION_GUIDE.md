# 🔗 Guia de Integração - GuardFlow GST Ecosystem

## 📋 Visão Geral

Este guia explica como integrar o **GuardFlow GST Ecosystem** em diferentes projetos GuardFlow ou aplicações externas.

## 🚀 Quick Start

### 1. Instalação

```bash
npm install @guardflow/gst-ecosystem
```

### 2. Configuração Básica

```javascript
const { GuardFlowGST } = require('@guardflow/gst-ecosystem');

const gst = new GuardFlowGST({
  network: 'mainnet',
  contracts: {
    gstToken: '0x...',
    marketplace: '0x...',
    converter: '0x...'
  },
  api: {
    baseUrl: 'https://api.guardflow.com/gst'
  }
});
```

## 🔧 Integrações Disponíveis

### 1. **GuardFlow Core**

```javascript
// Integração com GuardFlow Core
const { GuardFlowCore } = require('@guardflow/core');
const { GuardFlowGST } = require('@guardflow/gst-ecosystem');

const core = new GuardFlowCore(config);
const gst = new GuardFlowGST({
  ...config,
  integration: {
    core: core
  }
});

// Usar GST no contexto do Core
await gst.convertNFEToNFT(nfeData);
```

### 2. **GuardFlow SaaS**

```javascript
// Integração com GuardFlow SaaS
const { GuardFlowSaaS } = require('@guardflow/saas');
const { GuardFlowGST } = require('@guardflow/gst-ecosystem');

const saas = new GuardFlowSaaS(config);
const gst = new GuardFlowGST({
  ...config,
  integration: {
    saas: saas
  }
});

// Usar GST no contexto do SaaS
await gst.scanProduct(cartId, productId, quantity);
```

### 3. **GuardFlow Web**

```typescript
// Integração com GuardFlow Web
import { GuardFlowGST } from '@guardflow/gst-ecosystem';
import { GSTProvider } from '@guardflow/gst-ecosystem/react';

function App() {
  return (
    <GSTProvider config={gstConfig}>
      <GuardFlowDashboard />
    </GSTProvider>
  );
}
```

### 4. **GuardFlow Mobile**

```javascript
// Integração com GuardFlow Mobile
import { GuardFlowGST } from '@guardflow/gst-ecosystem';

const gst = new GuardFlowGST({
  network: 'mainnet',
  contracts: {...}
});

// Escanear produto no carrinho
await gst.scanProduct(cartId, productId, quantity);
```

## 📱 Exemplos de Uso

### Conversão NFe → NFT

```javascript
// Converter NFe em NFT
const result = await gst.convertNFEToNFT({
  nfeId: 'NFE-123456789',
  storeName: 'Supermercado Parceiro',
  storeCNPJ: '12.345.678/0001-90',
  purchaseAmount: 150.75,
  products: ['Produto A', 'Produto B'],
  sustainableProducts: [
    {
      name: 'Produto Orgânico',
      category: 'Alimentos',
      carbonFootprint: 10,
      isOrganic: true,
      isLocal: false,
      isRecyclable: true,
      sustainabilityPoints: 80
    }
  ],
  ipfsHash: 'QmTestHash123'
});

console.log('NFT criado:', result.tokenId);
console.log('GST recompensado:', result.gstReward);
```

### Escaneamento de Produtos

```javascript
// Escanear produto no carrinho
const scanResult = await gst.scanProduct(
  'cart-123',
  'prod-456',
  2
);

console.log('Produto escaneado:', scanResult.productName);
console.log('Score de sustentabilidade:', scanResult.sustainabilityScore);
```

### Obter NFTs do Usuário

```javascript
// Obter NFTs do usuário
const nfts = await gst.getUserNFTs('0x...');

nfts.forEach(nft => {
  console.log('NFT ID:', nft.tokenId);
  console.log('NFe ID:', nft.nfeId);
  console.log('Score de sustentabilidade:', nft.sustainabilityScore);
});
```

### Marketplace

```javascript
// Obter produtos do marketplace
const marketplace = await gst.getMarketplace();

marketplace.products.forEach(product => {
  console.log('Produto:', product.name);
  console.log('Preço em GST:', product.gstPrice);
  console.log('Score de sustentabilidade:', product.sustainabilityScore);
});
```

### Gamificação

```javascript
// Obter dados de gamificação
const gamification = await gst.getGamification('0x...');

console.log('Nível:', gamification.level);
console.log('Experiência:', gamification.experience);
console.log('Conquistas:', gamification.achievements);
```

## 🔧 Configuração Avançada

### Configuração de Rede

```javascript
const gst = new GuardFlowGST({
  network: 'mainnet', // 'mainnet', 'testnet', 'localhost'
  contracts: {
    gstToken: '0x...',
    invoiceNFT: '0x...',
    marketplace: '0x...',
    gamification: '0x...',
    governance: '0x...',
    nfeConverter: '0x...',
    smartCart: '0x...'
  },
  provider: new ethers.providers.JsonRpcProvider('https://...'),
  signer: wallet
});
```

### Configuração de API

```javascript
const gst = new GuardFlowGST({
  api: {
    baseUrl: 'https://api.guardflow.com/gst',
    version: 'v1',
    timeout: 30000,
    retries: 3
  }
});
```

### Configuração de Integração

```javascript
const gst = new GuardFlowGST({
  integration: {
    guardflowCore: {
      enabled: true,
      apiEndpoint: 'https://api.guardflow.com/core'
    },
    guardflowSaaS: {
      enabled: true,
      apiEndpoint: 'https://api.guardflow.com/saas'
    }
  }
});
```

## 🧪 Testing

### Testes Unitários

```javascript
// Exemplo de teste
const { GuardFlowGST } = require('@guardflow/gst-ecosystem');

describe('GuardFlowGST', () => {
  let gst;

  beforeEach(() => {
    gst = new GuardFlowGST({
      network: 'localhost',
      contracts: {...}
    });
  });

  it('should convert NFe to NFT', async () => {
    const result = await gst.convertNFEToNFT({
      nfeId: 'NFE-123',
      storeName: 'Test Store',
      purchaseAmount: 100
    });

    expect(result.success).toBe(true);
    expect(result.tokenId).toBeDefined();
  });
});
```

### Testes de Integração

```javascript
// Exemplo de teste de integração
describe('GST Integration', () => {
  it('should integrate with GuardFlow Core', async () => {
    const core = new GuardFlowCore(config);
    const gst = new GuardFlowGST({
      ...config,
      integration: { core }
    });

    const result = await gst.convertNFEToNFT(nfeData);
    expect(result.success).toBe(true);
  });
});
```

## 📊 Monitoramento

### Health Check

```javascript
// Verificar saúde do sistema
const health = await gst.healthCheck();

console.log('Status:', health.status);
console.log('Contratos:', health.contracts);
console.log('API:', health.api);
```

### Métricas

```javascript
// Obter estatísticas do ecossistema
const stats = await gst.getEcosystemStats();

console.log('Total de NFTs:', stats.totalNFTs);
console.log('Total de GST:', stats.totalGST);
console.log('Usuários ativos:', stats.activeUsers);
```

## 🔒 Segurança

### Autenticação

```javascript
const gst = new GuardFlowGST({
  authentication: {
    type: 'api-key',
    apiKey: 'your-api-key'
  }
});
```

### Criptografia

```javascript
const gst = new GuardFlowGST({
  security: {
    encryption: true,
    signature: true,
    audit: true
  }
});
```

## 🚀 Deploy

### Deploy Local

```bash
npm run deploy:local
```

### Deploy Testnet

```bash
npm run deploy:testnet
```

### Deploy Mainnet

```bash
npm run deploy:mainnet
```

## 📞 Suporte

- **Documentação**: [docs.guardflow.com/gst-ecosystem](https://docs.guardflow.com/gst-ecosystem)
- **Issues**: [GitHub Issues](https://github.com/SH1W4/guardflow-gst-ecosystem/issues)
- **Email**: gst-ecosystem@guardflow.com

---

<div align="center">
Made with 🌱 by SH1W4 | Transformando sustentabilidade em valor digital!
</div>

