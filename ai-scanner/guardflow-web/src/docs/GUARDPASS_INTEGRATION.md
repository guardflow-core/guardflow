# GuardPass Integration Guide

## 🔐 **GUARDPASS - INTEGRAÇÃO COM GUARDFLOW**

### **Visão Geral**
O GuardPass é o ecossistema de segurança e autenticação que se conecta ao GuardFlow para fornecer:
- Autenticação OAuth2 segura
- Controle de acesso granular
- Sincronização de dados ESG
- Monitoramento de segurança
- Auditoria de ações

---

## 🚀 **COMO O GUARDPASS SE CONECTA**

### **1. Arquitetura de Conexão**

```
┌─────────────────┐    OAuth2    ┌─────────────────┐
│   GuardFlow     │ ────────────► │   GuardPass     │
│   Frontend      │               │   API Server    │
└─────────────────┘               └─────────────────┘
         │                                 │
         │                                 │
         ▼                                 ▼
┌─────────────────┐               ┌─────────────────┐
│   GuardFlow     │ ◄──────────── │   GuardPass     │
│   Backend       │   Sync Data   │   Database      │
└─────────────────┘               └─────────────────┘
```

### **2. Fluxo de Autenticação**

1. **Inicialização**: GuardFlow verifica se há token válido
2. **Autenticação**: Se não autenticado, redireciona para GuardPass
3. **Autorização**: GuardPass valida credenciais e retorna tokens
4. **Armazenamento**: Tokens são armazenados localmente
5. **Validação**: Cada requisição valida o token

### **3. Tipos de Conexão**

#### **A. Conexão Direta (Recomendada)**
```typescript
// Configuração direta com GuardPass
const guardpassConfig = {
  api_url: 'https://api.guardpass.com',
  client_id: 'guardflow-client',
  client_secret: 'your_secret',
  scopes: ['read:profile', 'write:scans', 'read:esg']
};
```

#### **B. Conexão via Proxy**
```typescript
// Configuração via proxy interno
const guardpassConfig = {
  api_url: 'https://internal-proxy.company.com/guardpass',
  client_id: 'internal-client',
  client_secret: 'internal_secret'
};
```

#### **C. Conexão Local (Desenvolvimento)**
```typescript
// Configuração para desenvolvimento local
const guardpassConfig = {
  api_url: 'http://localhost:8080',
  client_id: 'dev-client',
  client_secret: 'dev_secret'
};
```

---

## 🔧 **CONFIGURAÇÃO DA INTEGRAÇÃO**

### **1. Variáveis de Ambiente**

```bash
# .env
REACT_APP_GUARDPASS_API_URL=https://api.guardpass.com
REACT_APP_GUARDPASS_CLIENT_ID=guardflow-client
REACT_APP_GUARDPASS_CLIENT_SECRET=your_client_secret
REACT_APP_GUARDPASS_REDIRECT_URI=http://localhost:3000/auth/callback
```

### **2. Configuração do Cliente**

```typescript
// guardpassService.ts
const config = {
  api_url: process.env.REACT_APP_GUARDPASS_API_URL,
  client_id: process.env.REACT_APP_GUARDPASS_CLIENT_ID,
  client_secret: process.env.REACT_APP_GUARDPASS_CLIENT_SECRET,
  redirect_uri: process.env.REACT_APP_GUARDPASS_REDIRECT_URI,
  scopes: ['read:profile', 'read:permissions', 'write:scans', 'read:esg']
};
```

---

## 📡 **ENDPOINTS DE INTEGRAÇÃO**

### **1. Autenticação**
```http
POST /oauth/authorize
Content-Type: application/json

{
  "client_id": "guardflow-client",
  "client_secret": "your_secret",
  "grant_type": "client_credentials",
  "scope": "read:profile write:scans read:esg"
}
```

### **2. Informações do Usuário**
```http
GET /api/v1/user/me
Authorization: Bearer {access_token}
```

### **3. Sincronização ESG**
```http
POST /api/v1/esg/sync
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "total_score": 87,
  "total_points": 2450,
  "total_tokens": 125,
  "last_updated": "2025-01-09T18:00:00Z"
}
```

### **4. Dados de Scan**
```http
POST /api/v1/scans
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "scan_id": "scan_123",
  "product_id": "prod_456",
  "esg_score": 85,
  "timestamp": "2025-01-09T18:00:00Z"
}
```

---

## 🔒 **SEGURANÇA E PERMISSÕES**

### **1. Scopes de Acesso**
- `read:profile` - Ler informações do usuário
- `read:permissions` - Verificar permissões
- `write:scans` - Enviar dados de scan
- `read:esg` - Acessar dados ESG
- `write:esg` - Sincronizar dados ESG

### **2. Controle de Acesso**
```typescript
// Verificar permissão específica
const hasPermission = await guardpassService.checkPermission('write:scans');

// Verificar múltiplas permissões
const permissions = ['read:profile', 'write:scans'];
const allGranted = permissions.every(p => 
  guardpassService.checkPermission(p)
);
```

### **3. Renovação de Tokens**
```typescript
// Refresh automático de tokens
const token = guardpassService.getValidToken(); // Auto-refresh se necessário

// Refresh manual
await guardpassService.refreshToken();
```

---

## 📊 **SINCRONIZAÇÃO DE DADOS**

### **1. Dados ESG**
```typescript
// Sincronizar score ESG
const esgData = {
  total_score: 87,
  total_points: 2450,
  total_tokens: 125,
  last_updated: new Date().toISOString()
};

await guardpassService.syncESGData(esgData);
```

### **2. Dados de Scan**
```typescript
// Enviar dados de scan
const scanData = {
  scan_id: 'scan_123',
  product_id: 'prod_456',
  esg_score: 85,
  timestamp: new Date().toISOString()
};

await guardpassService.sendScanData(scanData);
```

### **3. Configurações**
```typescript
// Obter configurações do GuardPass
const config = await guardpassService.getGuardPassConfig();
```

---

## 🚨 **TRATAMENTO DE ERROS**

### **1. Erros de Autenticação**
```typescript
try {
  await guardpassService.authenticate();
} catch (error) {
  if (error.message.includes('invalid_client')) {
    // Credenciais inválidas
  } else if (error.message.includes('invalid_scope')) {
    // Escopo inválido
  }
}
```

### **2. Erros de Conexão**
```typescript
try {
  const status = await guardpassService.checkConnection();
} catch (error) {
  // GuardPass indisponível
  console.error('GuardPass offline:', error);
}
```

### **3. Erros de Permissão**
```typescript
try {
  const hasPermission = await guardpassService.checkPermission('write:scans');
} catch (error) {
  // Usuário não tem permissão
  console.error('Permission denied:', error);
}
```

---

## 🔄 **FLUXO COMPLETO DE INTEGRAÇÃO**

### **1. Inicialização**
```typescript
// Verificar se já está autenticado
if (guardpassService.isAuthenticated()) {
  // Usuário já autenticado
  const user = await guardpassService.getCurrentUser();
} else {
  // Redirecionar para autenticação
  await guardpassService.authenticate();
}
```

### **2. Operações Diárias**
```typescript
// Verificar permissões antes de operações
const canScan = await guardpassService.checkPermission('write:scans');
const canReadESG = await guardpassService.checkPermission('read:esg');

if (canScan) {
  // Permitir operação de scan
}

if (canReadESG) {
  // Permitir acesso a dados ESG
}
```

### **3. Sincronização Periódica**
```typescript
// Sincronizar dados ESG a cada 30 minutos
setInterval(async () => {
  try {
    await guardpassService.syncESGData(currentESGData);
  } catch (error) {
    console.error('ESG sync failed:', error);
  }
}, 30 * 60 * 1000);
```

---

## 📈 **MONITORAMENTO E LOGS**

### **1. Status da Conexão**
```typescript
// Verificar status da conexão
const status = await guardpassService.checkConnection();
console.log('GuardPass Status:', status);
```

### **2. Logs de Integração**
```typescript
// Logs automáticos em todas as operações
guardpassService.on('authenticate', (data) => {
  console.log('User authenticated:', data);
});

guardpassService.on('sync', (data) => {
  console.log('Data synced:', data);
});
```

---

## 🎯 **BENEFÍCIOS DA INTEGRAÇÃO**

### **1. Segurança**
- ✅ Autenticação OAuth2 segura
- ✅ Controle de acesso granular
- ✅ Auditoria completa de ações
- ✅ Renovação automática de tokens

### **2. Sincronização**
- ✅ Dados ESG em tempo real
- ✅ Histórico de scans centralizado
- ✅ Configurações sincronizadas
- ✅ Backup automático

### **3. Monitoramento**
- ✅ Status de conexão em tempo real
- ✅ Logs detalhados de operações
- ✅ Alertas de segurança
- ✅ Métricas de performance

---

## 🚀 **PRÓXIMOS PASSOS**

1. **Configurar** variáveis de ambiente
2. **Testar** conexão com GuardPass
3. **Implementar** autenticação OAuth2
4. **Configurar** sincronização de dados
5. **Monitorar** status da integração

**"GuardPass fornece a base de segurança e autenticação para todo o ecossistema GuardFlow!"** 🔐✨
