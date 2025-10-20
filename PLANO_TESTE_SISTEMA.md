# 🧪 PLANO DE TESTE - GuardFlow Sistema Completo

## 🎯 **OBJETIVO**
Preparar e testar o sistema GuardFlow para garantir que está **100% funcional** para demonstrações e uso em produção.

## 📋 **CHECKLIST DE PREPARAÇÃO**

### ✅ **1. DEPENDÊNCIAS BACKEND**
```bash
# Instalar dependências críticas
pip install psutil==5.9.6
pip install prometheus-fastapi-instrumentator
pip install slowapi[redis]==0.1.9
```

### ✅ **2. CONFIGURAÇÃO AMBIENTE**
```bash
# Criar .env no backend
DATABASE_URL=sqlite:///./guardflow.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-change-in-production
ENVIRONMENT=development
DEBUG=true
```

### ✅ **3. TESTE DE IMPORTAÇÕES**
```python
# Testar se todas as APIs importam corretamente
python -c "from app.main import app; print('✅ Backend OK')"
```

### ✅ **4. FRONTEND BUILD**
```bash
# Testar build do frontend
cd guardflow-web
npm install
npm run build
```

## 🚀 **SEQUÊNCIA DE TESTES**

### **FASE 1: Testes Básicos**
1. ✅ Importações do backend
2. ✅ Inicialização do FastAPI
3. ✅ Acesso às rotas principais
4. ✅ Build do frontend

### **FASE 2: Testes de Integração**
1. ✅ APIs funcionando
2. ✅ Frontend conectando com backend
3. ✅ Banco de dados funcionando
4. ✅ Cache Redis operacional

### **FASE 3: Testes Funcionais**
1. ✅ Scanner de produtos
2. ✅ Carrinho de compras
3. ✅ Dashboard ESG
4. ✅ QR Checkout
5. ✅ SEVE Personalization
6. ✅ Performance Monitor

## 🔧 **COMANDOS DE TESTE RÁPIDO**

### **Teste Backend Simples**
```bash
cd backend
python -c "
import sys
sys.path.append('.')
try:
    from app.main import app
    print('✅ Backend imports OK')
    print('✅ FastAPI app criado')
    print('✅ Rotas carregadas:', len(app.routes))
except Exception as e:
    print('❌ Erro:', e)
"
```

### **Teste Frontend Simples**
```bash
cd guardflow-web
npm list react react-dom @mui/material
```

### **Teste APIs**
```bash
# Iniciar backend
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testar endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

## 📊 **CRITÉRIOS DE SUCESSO**

### **Backend (Obrigatório)**
- ✅ Todas as importações funcionam
- ✅ FastAPI inicia sem erros
- ✅ 9 APIs principais carregadas
- ✅ Documentação acessível em /docs

### **Frontend (Obrigatório)**
- ✅ Build sem erros críticos
- ✅ Todas as páginas renderizam
- ✅ Navegação funciona
- ✅ Componentes carregam

### **Integração (Desejável)**
- ✅ Frontend conecta com backend
- ✅ APIs respondem corretamente
- ✅ Dados são exibidos
- ✅ Funcionalidades básicas operam

## 🎯 **RESULTADO ESPERADO**

Após executar todos os testes, o sistema deve estar:

1. **✅ FUNCIONAL** - Todas as partes principais funcionando
2. **✅ ACESSÍVEL** - URLs respondendo corretamente
3. **✅ INTEGRADO** - Frontend e backend comunicando
4. **✅ DEMONSTRÁVEL** - Pronto para apresentações

## 🚀 **PRÓXIMOS PASSOS APÓS TESTES**

1. **Demonstração Executiva** - Sistema pronto para apresentar
2. **Testes de Carga** - Validar performance sob stress
3. **Deploy Produção** - Usar scripts de deploy criados
4. **Vendas SaaS** - Iniciar processo comercial

---

**Status**: 🧪 **PRONTO PARA TESTE**  
**Objetivo**: Sistema 100% funcional para demonstrações  
**Timeline**: Testes completos em 30 minutos
