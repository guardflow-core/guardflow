# 🚀 **SCRIPT DE REORGANIZAÇÃO DO GUARDFLOW**
# Este script implementa a reorganização inteligente da estrutura do projeto

param(
    [switch]$DryRun = $false,
    [switch]$Backup = $true,
    [switch]$CleanMetadata = $true
)

Write-Host "🔄 Iniciando reorganização do GuardFlow..." -ForegroundColor Green

# 📁 Criar backup se solicitado
if ($Backup) {
    Write-Host "📦 Criando backup do projeto..." -ForegroundColor Yellow
    $backupName = "GuardFlow_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item -Path "." -Destination "../$backupName" -Recurse
    Write-Host "✅ Backup criado: $backupName" -ForegroundColor Green
}

# 🧹 Limpeza de arquivos desnecessários
if ($CleanMetadata) {
    Write-Host "🧹 Removendo arquivos .metadata.json..." -ForegroundColor Yellow
    Get-ChildItem -Path "." -Filter "*.metadata.json" -Recurse | Remove-Item -Force
    Write-Host "✅ Arquivos .metadata.json removidos" -ForegroundColor Green
}

# 📁 Criar nova estrutura de diretórios
Write-Host "📁 Criando nova estrutura de diretórios..." -ForegroundColor Yellow

$newStructure = @(
    "apps/backend",
    "apps/frontend",
    "apps/mobile", 
    "apps/sdk/python",
    "apps/sdk/javascript",
    "apps/sdk/rust",
    "services/analytics",
    "services/docsync",
    "services/ai",
    "infrastructure/docker",
    "infrastructure/k8s",
    "infrastructure/nginx",
    "infrastructure/terraform",
    "docs/api",
    "docs/user-guide",
    "docs/developer",
    "docs/business",
    "docs/architecture",
    "examples/basic",
    "examples/advanced",
    "examples/integrations",
    "tests/unit",
    "tests/integration",
    "tests/e2e",
    "scripts/deployment",
    "scripts/development",
    "scripts/maintenance",
    "config/environments",
    "config/database",
    "config/integrations",
    "tools/linting",
    "tools/formatting",
    "tools/testing"
)

foreach ($dir in $newStructure) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Criado: $dir" -ForegroundColor Green
    }
}

# 📦 Mover arquivos para nova estrutura
Write-Host "📦 Movendo arquivos para nova estrutura..." -ForegroundColor Yellow

# Backend
if (Test-Path "backend") {
    Move-Item -Path "backend/*" -Destination "apps/backend/" -Force
    Write-Host "  ✅ Backend movido" -ForegroundColor Green
}

# Frontend
if (Test-Path "guardflow-web") {
    Move-Item -Path "guardflow-web/*" -Destination "apps/frontend/" -Force
    Write-Host "  ✅ Frontend movido" -ForegroundColor Green
}

# Mobile
if (Test-Path "mobile-app") {
    Move-Item -Path "mobile-app/*" -Destination "apps/mobile/" -Force
    Write-Host "  ✅ Mobile movido" -ForegroundColor Green
}

# SDK
if (Test-Path "guardflow-sdk") {
    Move-Item -Path "guardflow-sdk/*" -Destination "apps/sdk/python/" -Force
    Write-Host "  ✅ SDK Python movido" -ForegroundColor Green
}

# Services
if (Test-Path "analytics") {
    Move-Item -Path "analytics/*" -Destination "services/analytics/" -Force
    Write-Host "  ✅ Analytics movido" -ForegroundColor Green
}

if (Test-Path "docsync") {
    Move-Item -Path "docsync/*" -Destination "services/docsync/" -Force
    Write-Host "  ✅ DocSync movido" -ForegroundColor Green
}

# Examples
if (Test-Path "examples") {
    Move-Item -Path "examples/*" -Destination "examples/basic/" -Force
    Write-Host "  ✅ Examples movidos" -ForegroundColor Green
}

# 📚 Organizar documentação
Write-Host "📚 Organizando documentação..." -ForegroundColor Yellow

$docCategories = @{
    "business" = @("EAP_*.md", "ESTRATEGIA_*.md", "ROADMAP_*.md", "PLANO_*.md")
    "architecture" = @("ARQUITETURA_*.md", "ESTRUTURA_*.md", "INTEGRATION_*.md")
    "developer" = @("DESENVOLVIMENTO_*.md", "SETUP_*.md", "TODO_*.md")
    "api" = @("API_*.md", "ENDPOINTS_*.md")
}

foreach ($category in $docCategories.Keys) {
    $patterns = $docCategories[$category]
    foreach ($pattern in $patterns) {
        Get-ChildItem -Path "." -Filter $pattern | ForEach-Object {
            $destPath = "docs/$category/$($_.Name)"
            Move-Item -Path $_.FullName -Destination $destPath -Force
            Write-Host "  ✅ Movido: $($_.Name) -> docs/$category/" -ForegroundColor Green
        }
    }
}

# 🧹 Limpeza final
Write-Host "🧹 Limpeza final..." -ForegroundColor Yellow

# Remover diretórios vazios
Get-ChildItem -Path "." -Directory | Where-Object { (Get-ChildItem $_.FullName -Recurse | Measure-Object).Count -eq 0 } | Remove-Item -Force

# Remover arquivos temporários
$tempFiles = @("*.log", "*.tmp", "*.temp", "*.bak")
foreach ($pattern in $tempFiles) {
    Get-ChildItem -Path "." -Filter $pattern -Recurse | Remove-Item -Force
}

Write-Host "✅ Limpeza final concluída" -ForegroundColor Green

# 📋 Criar arquivo de configuração da nova estrutura
Write-Host "📋 Criando arquivo de configuração..." -ForegroundColor Yellow

$config = @{
    "project" = "GuardFlow"
    "version" = "2.0.0"
    "structure" = "Reorganized"
    "date" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "directories" = $newStructure
}

$config | ConvertTo-Json -Depth 3 | Out-File -FilePath "config/project-structure.json" -Encoding UTF8

Write-Host "✅ Arquivo de configuração criado" -ForegroundColor Green

# 📊 Relatório final
Write-Host "📊 Reorganização concluída!" -ForegroundColor Green
Write-Host "📁 Nova estrutura criada com sucesso" -ForegroundColor Green
Write-Host "📚 Documentação organizada" -ForegroundColor Green
Write-Host "🧹 Arquivos desnecessários removidos" -ForegroundColor Green
Write-Host "📋 Configuração salva" -ForegroundColor Green

Write-Host "`n🎯 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Verificar funcionamento dos apps" -ForegroundColor White
Write-Host "2. Atualizar referências nos códigos" -ForegroundColor White
Write-Host "3. Testar integrações" -ForegroundColor White
Write-Host "4. Documentar nova estrutura" -ForegroundColor White
Write-Host "5. Treinar equipe" -ForegroundColor White

Write-Host "`n🚀 GuardFlow reorganizado com sucesso!" -ForegroundColor Green
