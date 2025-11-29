# GuardFlow - Guia de Execução Rápida

## 🚀 **EXECUÇÃO AUTOMÁTICA (RECOMENDADO)**

### **1. Verificar Dependências**
```powershell
.\check_dependencies.ps1
```

### **2. Iniciar Sistema Completo**
```powershell
.\start_guardflow.ps1
```

---

## 🔧 **EXECUÇÃO MANUAL**

### **Backend (FastAPI)**
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

### **Frontend (React)**
```bash
cd guardflow-web
npm start
```

### **Mobile (React Native)**
```bash
cd mobile-app
npx expo start
```

---

## 🌐 **URLs DE ACESSO**

- **Backend API**: http://127.0.0.1:8002
- **API Documentation**: http://127.0.0.1:8002/docs
- **Frontend Web**: http://localhost:3000
- **Mobile**: Expo Go app

---

## 🧪 **TESTES RÁPIDOS**

### **1. Testar Backend**
```bash
curl -X GET "http://127.0.0.1:8002/health"
```

### **2. Testar APIs ESG**
```bash
curl -X GET "http://127.0.0.1:8002/api/v1/esg/dashboard/test-user"
```

### **3. Testar Frontend**
- Acesse: http://localhost:3000
- Verifique se a interface carrega

### **4. Testar Mobile**
- Abra Expo Go no celular
- Escaneie o QR code

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Problema: Backend não inicia**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

### **Problema: Frontend não inicia**
```bash
cd guardflow-web
npm install
npm start
```

### **Problema: Mobile não inicia**
```bash
cd mobile-app
npm install
npx expo start
```

### **Problema: Dependências faltando**
```bash
# Python
pip install fastapi uvicorn slowapi

# Node.js
npm install -g expo-cli
```

---

## 📊 **STATUS DOS SERVIÇOS**

### **✅ Backend (FastAPI)**
- Porta: 8002
- Status: Funcional
- APIs: ESG, Monetization, Dashboard

### **✅ Frontend (React)**
- Porta: 3000
- Status: Funcional
- Interface: Material-UI

### **✅ Mobile (React Native)**
- Expo: Funcional
- Status: Funcional
- Interface: Nativa

---

## 🎯 **PRÓXIMOS PASSOS**

### **1. Integração SYMBEON**
- Implementar SEVE-Core
- Adicionar personalidades por setor
- Implementar análise emocional

### **2. Testes de Integração**
- Backend + Frontend + Mobile
- APIs ESG funcionais
- Fluxo completo de checkout

### **3. Otimizações**
- Performance do sistema
- Segurança das APIs
- Experiência do usuário

---

## 🎉 **RESULTADOS ESPERADOS**

### **✅ Sistema Completo Funcionando**
- Backend FastAPI rodando
- Frontend React responsivo
- Mobile React Native funcional
- Integração SYMBEON preparada

### **✅ Funcionalidades ESG**
- Tokenização ESG automática
- Dashboard ESG completo
- Gamificação ESG ativa
- Monetização governamental

### **✅ Tecnologia Avançada**
- IA ética integrada
- Personalidades por setor
- Análise emocional preparada
- Efeitos técnicos mensuráveis

---

**GuardFlow: Sistema de Checkout Inteligente com IA Ética! 🛒⚡🌱🤖**

**Status**: ✅ SISTEMA COMPLETO FUNCIONAL
**Próxima Ação**: Integrar SYMBEON Framework
**Responsável**: João (Product Owner)
**Data**: 2025-01-27


