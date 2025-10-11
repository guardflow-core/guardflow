# 🚀 **Guia de Instalação - DocSync Adaptativo**

## **Sistema Inteligente de Estrutura Adaptativa - ESG Token Ecosystem**

Este guia detalha como instalar e configurar o **DocSync Adaptativo** para o **ESG Token Ecosystem**.

---

## 📋 **Pré-requisitos**

### **Sistema Operacional:**
- **Windows 10/11** (recomendado)
- **PowerShell 5.1+** ou **PowerShell Core 7+**
- **Python 3.8+** (recomendado Python 3.9+)

### **Ferramentas Necessárias:**
```bash
# Verificar Python
python --version

# Verificar PowerShell
$PSVersionTable.PSVersion

# Verificar Git (opcional)
git --version
```

---

## 🔧 **Instalação Passo a Passo**

### **1. Preparar Ambiente:**
```powershell
# Criar diretório de trabalho
mkdir C:\ESG-Token-Ecosystem
cd C:\ESG-Token-Ecosystem

# Clonar ou baixar o projeto
git clone https://github.com/seu-usuario/ESG-Token-Ecosystem.git
# OU baixar e extrair o ZIP
```

### **2. Instalar Dependências Python:**
```bash
# Instalar dependências básicas
pip install pyyaml numpy scikit-learn

# Verificar instalação
python -c "import yaml, numpy, sklearn; print('Dependências instaladas com sucesso!')"
```

### **3. Configurar DocSync:**
```powershell
# Navegar para o diretório docsync
cd docsync

# Copiar arquivo de configuração de exemplo
Copy-Item "esg-token-docsync.yaml.example" "esg-token-docsync.yaml"

# Verificar configuração
Get-Content esg-token-docsync.yaml
```

### **4. Ajustar Configuração:**
```yaml
# Editar esg-token-docsync.yaml
directories:
  - path: "C:/SEU/CAMINHO/PARA/GuardFlow"  # Ajustar conforme seu ambiente
    type: "documentation"
    sync_enabled: true
    # ... outras configurações
```

### **5. Testar Instalação:**
```powershell
# Testar sistema básico
.\run_adaptive_docsync.ps1 -StructureOnly

# Testar com saída detalhada
.\run_adaptive_docsync.ps1 -Verbose
```

---

## ⚙️ **Configuração Avançada**

### **1. Configuração de Diretórios:**
```yaml
# Ajustar paths conforme seu ambiente
directories:
  - path: "C:/Users/SeuUsuario/Desktop/PROJETOS/GuardFlow"
    type: "documentation"
    sync_enabled: true
    patterns:
      - "*.md"
      - "*.yaml"
      - "*.json"
    exclude:
      - "**/__pycache__"
      - "**/.git"
      - "**/node_modules"
```

### **2. Configuração de Aprendizado:**
```yaml
# Ajustar parâmetros de aprendizado
learning_config:
  feedback_weight: 0.3
  pattern_weight: 0.4
  historical_weight: 0.3
  adaptation_threshold: 0.7
  learning_rate: 0.1
  max_iterations: 100
```

### **3. Configuração de Auto-Organização:**
```yaml
# Ajustar ações automáticas
auto_actions:
  create_missing_files: true
  standardize_naming: true
  organize_directories: true
  validate_esg_content: true
  update_documentation: true
```

---

## 🚀 **Primeiro Uso**

### **1. Execução Básica:**
```powershell
# Executar sistema adaptativo completo
.\run_adaptive_docsync.ps1

# Verificar logs
Get-Content adaptive_docsync.log
```

### **2. Verificar Relatórios:**
```powershell
# Ver relatório principal
Get-Content adaptive_docsync_report.json | ConvertFrom-Json | Format-List

# Ver métricas específicas
$report = Get-Content adaptive_docsync_report.json | ConvertFrom-Json
Write-Host "Score de Organização: $($report.organization_score)"
```

### **3. Executar Modos Específicos:**
```powershell
# Apenas aprendizado contínuo
.\run_adaptive_docsync.ps1 -LearningOnly

# Apenas análise de estrutura
.\run_adaptive_docsync.ps1 -StructureOnly

# Apenas auto-organização
.\run_adaptive_docsync.ps1 -AutoOrganizationOnly
```

---

## 🔧 **Troubleshooting**

### **Problemas Comuns:**

#### **1. Python não encontrado:**
```bash
# Instalar Python
# Baixar de: https://www.python.org/downloads/
# Marcar "Add Python to PATH" durante instalação

# Verificar instalação
python --version
```

#### **2. Módulos Python não encontrados:**
```bash
# Instalar dependências
pip install pyyaml numpy scikit-learn

# Verificar instalação
python -c "import yaml, numpy, sklearn"
```

#### **3. Erro de permissão:**
```powershell
# Executar como administrador
Start-Process PowerShell -Verb RunAs

# Verificar permissões
Test-Path -Path "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow" -PathType Container
```

#### **4. Configuração não encontrada:**
```powershell
# Verificar arquivo de configuração
Test-Path esg-token-docsync.yaml

# Criar configuração padrão
Copy-Item "esg-token-docsync.yaml.example" "esg-token-docsync.yaml"
```

#### **5. Erro de aprendizado:**
```bash
# Verificar dados de aprendizado
Test-Path learning_data.json

# Limpar dados de aprendizado
Remove-Item learning_data.json -Force
```

---

## 📊 **Monitoramento e Logs**

### **Arquivos de Log:**
- **adaptive_docsync.log** - Log principal do sistema adaptativo
- **continuous_learning.log** - Logs de aprendizado contínuo
- **auto_organization.log** - Logs de auto-organização
- **adaptive_structure.log** - Logs de estrutura adaptativa

### **Comandos de Monitoramento:**
```powershell
# Ver logs em tempo real
Get-Content adaptive_docsync.log -Wait

# Ver últimas 20 linhas
Get-Content adaptive_docsync.log | Select-Object -Last 20

# Filtrar por nível de log
Get-Content adaptive_docsync.log | Where-Object { $_ -match "ERROR" }
```

---

## 📈 **Relatórios e Métricas**

### **Relatórios Gerados:**
- **adaptive_docsync_report.json** - Relatório principal
- **continuous_learning_report.json** - Relatório de aprendizado
- **auto_organization_report.json** - Relatório de auto-organização
- **adaptive_structure_report.json** - Relatório de estrutura

### **Visualização de Relatórios:**
```powershell
# Ver relatório completo
Get-Content adaptive_docsync_report.json | ConvertFrom-Json | Format-List

# Ver métricas específicas
$report = Get-Content adaptive_docsync_report.json | ConvertFrom-Json
Write-Host "Score de Organização: $($report.organization_score)"
Write-Host "Efetividade do Aprendizado: $($report.learning_effectiveness)"
Write-Host "Adaptações Aplicadas: $($report.adaptations_applied)"
```

---

## 🛠️ **Manutenção**

### **Limpeza de Logs:**
```powershell
# Limpar logs antigos (manter últimos 30 dias)
Get-ChildItem *.log | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item

# Limpar dados de aprendizado antigos
Get-ChildItem learning_data*.json | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-90) } | Remove-Item
```

### **Backup de Configuração:**
```powershell
# Fazer backup da configuração
Copy-Item "esg-token-docsync.yaml" "esg-token-docsync.yaml.backup"

# Restaurar configuração
Copy-Item "esg-token-docsync.yaml.backup" "esg-token-docsync.yaml"
```

### **Atualização do Sistema:**
```powershell
# Fazer backup antes da atualização
Copy-Item -Recurse "docsync" "docsync_backup"

# Atualizar arquivos (substituir por novos arquivos)
# ... processo de atualização ...

# Verificar funcionamento após atualização
.\run_adaptive_docsync.ps1 -StructureOnly
```

---

## 🎯 **Próximos Passos**

### **Após Instalação:**
1. **Executar Primeiro Ciclo**: `.\run_adaptive_docsync.ps1 -SingleCycle`
2. **Verificar Relatórios**: Analisar relatórios gerados
3. **Ajustar Configuração**: Personalizar conforme necessário
4. **Executar Adaptação Contínua**: `.\run_adaptive_docsync.ps1 -ContinuousAdaptation`

### **Configuração Avançada:**
1. **Personalizar Regras**: Ajustar regras de organização
2. **Configurar Padrões ESG**: Definir padrões específicos
3. **Ajustar Ações Automáticas**: Configurar ações desejadas
4. **Monitorar Performance**: Acompanhar métricas de performance

---

## 📞 **Suporte**

### **Arquivos de Suporte:**
- **ADAPTIVE_DOCSYNC_README.md** - Documentação principal
- **ADAPTIVE_DOCSYNC_GUIDE.md** - Guia de uso
- **INSTALLATION_GUIDE.md** - Este guia de instalação

### **Comandos de Ajuda:**
```powershell
# Ajuda do sistema adaptativo
.\run_adaptive_docsync.ps1 -Help

# Verificar configuração
Get-Content esg-token-docsync.yaml

# Verificar logs
Get-Content adaptive_docsync.log
```

---

## 🏆 **Conclusão**

O **DocSync Adaptativo** está agora instalado e configurado para o **ESG Token Ecosystem**.

### **Sistema Pronto:**
✅ **Instalação Completa** - Todas as dependências instaladas  
✅ **Configuração Aplicada** - Sistema configurado conforme ambiente  
✅ **Testes Realizados** - Sistema testado e funcionando  
✅ **Documentação Disponível** - Guias e manuais disponíveis  
✅ **Suporte Configurado** - Sistema de suporte ativo  

### **Próximos Passos:**
1. **Executar Primeiro Ciclo** para familiarizar-se com o sistema
2. **Ajustar Configuração** conforme suas necessidades
3. **Monitorar Relatórios** para acompanhar melhorias
4. **Executar Adaptação Contínua** para evolução automática

---

**Desenvolvido com ❤️ e 🧠 para o ESG Token Ecosystem**
