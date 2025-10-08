# Setup de Desenvolvimento

## Pré-requisitos
- Python 3.11
- Node.js LTS
- Git

## Backend (FastAPI)
1. Copie o arquivo de exemplo e ajuste variáveis:
   - `cp backend/.env.example backend/.env` (ajuste conforme necessário)
2. Crie venv e instale dependências:
   - Windows PowerShell
     - `cd backend`
     - `python -m venv venv`
     - `venv\Scripts\Activate.ps1`
     - `pip install -r requirements.txt`
3. Execute a API:
   - `uvicorn app.main:app --reload --port 8000`
4. Acesse:
   - Docs: `http://localhost:8000/docs`
   - Health: `http://localhost:8000/health`
   - Métricas: `http://localhost:8000/metrics`

## Mobile App (React Native)
1. `cd mobile-app`
2. `yarn` ou `npm install`
3. Configure a base URL da API (arquivo de config/env do app)
4. Rodar (exemplo Expo/CLI): `yarn start`

## Demos Web (opcionais)
- `guardflow-web`, `guardflow-web-demo`, `guardflow-demo` são exemplos. Ajuste `API_BASE_URL` conforme necessidade.

## Observabilidade
- Logs: `backend/logs/guardflow.log`
- Métricas Prometheus: `/metrics`

## Dicas
- Mantenha `.env` fora do versionamento; use `.env.example` como referência.
- Use branches `feature/*` e abra PR para `develop`.

