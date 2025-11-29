# API Enterprise - ESG Token Ecosystem

## Endpoints Principais

### ESG Metrics
- `POST /api/v1/metrics` - Criar métricas
- `GET /api/v1/metrics/{id}` - Obter métricas
- `PUT /api/v1/metrics/{id}` - Atualizar métricas

### Token Management
- `POST /api/v1/tokens/mint` - Mintar tokens
- `POST /api/v1/tokens/transfer` - Transferir tokens
- `GET /api/v1/tokens/balance/{address}` - Saldo de tokens

### Blockchain Integration
- `POST /api/v1/blockchain/deploy` - Deploy de contratos
- `GET /api/v1/blockchain/status` - Status da blockchain

### AI Services
- `POST /api/v1/ai/analyze` - Análise de dados
- `POST /api/v1/ai/predict` - Predições
- `POST /api/v1/ai/recommend` - Recomendações

## Autenticação
Bearer Token: `Authorization: Bearer <token>`

## Rate Limiting
100 requests/minute por IP
