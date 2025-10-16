# 📝 CHANGELOG - GuardFlow

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2025-10-16

### ✨ Adicionado
- ESG Engine núcleo implementado (`backend/app/services/esg_engine.py`)
  - 14 fatores ESG (Ambiental, Social, Governança)
  - Mapeamento NCM → Fatores ESG
  - Cálculo ponderado por categoria e score geral
  - Insights automáticos por categoria
- API ESG Engine (`backend/app/api/esg_engine.py`)
  - `POST /api/v1/esg-engine/calculate-score`
  - `GET /api/v1/esg-engine/factors`
  - `GET /api/v1/esg-engine/factors/by-ncm/{ncm}`
  - `GET /api/v1/esg-engine/categories`
  - `GET /api/v1/esg-engine/health`
- Documentos de Compliance
  - `docs/COMPLIANCE_LGPD.md`
  - `docs/COMPLIANCE_SEFAZ.md`

### 🔧 Modificado
- `app.main` refatorado para carregar routers de forma isolada (fail-safe)
- README enriquecido com endpoints do ESG Engine
- Índice de documentação atualizado

### 🧪 Testes
- Nova suíte `tests/test_esg_engine.py`
- Suite backend com 14 testes passando

### 📈 Status do Projeto
- Progresso estimado: 90% (antes: 85%)

## [1.0.0] - 2024-12-19

### 🎉 Adicionado
- **Backend FastAPI** com arquitetura robusta e segura
  - Autenticação OAuth2/JWT implementada
  - Sistema RBAC (Role-Based Access Control)
  - Rate limiting e proteção CORS
  - Middleware de segurança e logging
  - Integração com Prometheus para métricas
- **Infraestrutura Docker** completa
  - `docker-compose.dev.yml` com todos os serviços
  - PostgreSQL 15 + Redis 7 + Prometheus + Grafana
  - Configuração de desenvolvimento otimizada
- **Sistema de Observabilidade**
  - Métricas Prometheus integradas
  - Dashboards Grafana configurados
  - Health checks enriquecidos
  - Logs estruturados
- **Testes Automatizados**
  - Cobertura de testes para auth, cart, payment
  - Testes de health check e endpoints críticos
  - CI/CD com GitHub Actions
- **Documentação Completa**
  - README.md atualizado com nova arquitetura
  - Guias de operação e setup detalhados
  - Documentação de API interativa
- **Configurações Padronizadas**
  - `.env.example` para todas as aplicações
  - Configurações de API_BASE_URL alinhadas
  - `.gitignore` unificado
- **Estrutura de Projeto Reorganizada**
  - Consolidação de demos web em `examples/`
  - Documentação centralizada em `docs/`
  - Scripts de automação em `scripts/`

### 🔧 Modificado
- **Estrutura de Repositório**
  - Reorganização inteligente de pastas e arquivos
  - Consolidação de documentação duplicada
  - Padronização de configurações
- **Backend**
  - Implementação de segurança robusta
  - Contratos Pydantic padronizados
  - Rotas com fallback para módulos opcionais
  - Health check enriquecido com métricas
- **Frontend Web**
  - Configuração de API_BASE_URL padronizada
  - Dockerfile otimizado
  - Estrutura consolidada
- **Mobile App**
  - Configuração de API_BASE_URL
  - Estrutura de projeto limpa
- **Docker**
  - Configuração de portas otimizada
  - Serviços de monitoramento integrados
  - Ambiente de desenvolvimento completo

### 🐛 Corrigido
- **Conflitos de Porta**
  - Redis configurado para porta 6380
  - Evita conflitos com instâncias locais
- **Problemas de Banco de Dados**
  - Configuração correta do asyncpg para PostgreSQL
  - URLs de conexão padronizadas
- **Problemas de Testes**
  - PYTHONPATH configurado corretamente
  - Imports condicionais para módulos opcionais
  - Testes passando em ambiente mínimo

### 🔒 Segurança
- **Autenticação OAuth2/JWT**
  - Tokens seguros com expiração configurável
  - Rotação automática de chaves
- **Rate Limiting**
  - Proteção contra abuso de API
  - Configuração flexível por endpoint
- **CORS e Trusted Hosts**
  - Configuração de origens confiáveis
  - Validação de hosts
- **Variáveis de Ambiente**
  - Secrets gerenciados via .env
  - Exemplos seguros fornecidos

### 📊 Monitoramento
- **Prometheus Metrics**
  - Métricas de performance da API
  - Contadores de requisições e erros
  - Métricas de recursos do sistema
- **Grafana Dashboards**
  - Visualização de métricas em tempo real
  - Alertas configuráveis
  - Dashboards pré-configurados
- **Health Checks**
  - Endpoint `/health` enriquecido
  - Verificação de dependências
  - Status detalhado do sistema

### 🧪 Testes
- **Cobertura de Testes**
  - Testes para endpoints críticos
  - Mocks para serviços externos
  - Testes de autenticação e autorização
- **CI/CD**
  - GitHub Actions configurado
  - Linting automático com ruff
  - Testes automatizados em PRs
- **Ambiente de Teste**
  - Configuração mínima para testes
  - Imports condicionais
  - Fallbacks para módulos opcionais

### 📚 Documentação
- **README.md**
  - Arquitetura atualizada com diagramas
  - Instruções de instalação completas
  - Exemplos de integração
  - Roadmap atualizado
- **Guias Operacionais**
  - `OPERACAO_REPO.md` - Guia completo de operação
  - `SETUP_DEV.md` - Setup de desenvolvimento
  - `GUIA_MIGRACAO_ESTRUTURA.md` - Guia de migração
- **Documentação Técnica**
  - API Reference interativa
  - Exemplos de código
  - Troubleshooting guide

### 🚀 Performance
- **Otimizações de Backend**
  - Async/await implementado
  - Pool de conexões otimizado
  - Cache Redis integrado
- **Docker**
  - Imagens otimizadas
  - Build multi-stage
  - Dependências mínimas

### 🔄 DevOps
- **Docker Compose**
  - Stack completo de desenvolvimento
  - Serviços de monitoramento
  - Configuração de rede
- **GitHub Actions**
  - CI/CD automatizado
  - Testes em múltiplos ambientes
  - Deploy automático
- **Versionamento**
  - Conventional Commits
  - Semantic Versioning
  - Changelog automático

---

## [0.9.0] - 2024-12-18

### 🎉 Adicionado
- Estrutura inicial do projeto
- Backend FastAPI básico
- Frontend React
- Mobile React Native
- Documentação inicial

### 🔧 Modificado
- Estrutura de pastas
- Configurações básicas

### 🐛 Corrigido
- Problemas de configuração inicial
- Dependências básicas

---

## 📋 Próximas Versões

### [1.1.0] - Planejado
- [ ] Conectar mobile ao backend
- [ ] Completar frontend web
- [ ] Testes E2E completos
- [ ] Deploy em produção

### [1.2.0] - Planejado
- [ ] 10 mercados ativos
- [ ] 1.000 usuários ativos
- [ ] Monetização governamental ativa
- [ ] Ecossistema ESG completo

### [2.0.0] - Planejado
- [ ] Multi-tenant architecture
- [ ] Microserviços especializados
- [ ] Blockchain integration
- [ ] Marketplace de tokens ESG

---

<div align="center">
📝 **GuardFlow Changelog**<br/>
Histórico de Mudanças e Evolução
</div>
