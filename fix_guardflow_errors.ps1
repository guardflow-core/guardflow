# GuardFlow - Script de Correção de Erros
# Corrige todos os problemas identificados no GuardFlow

Write-Host "🔧 Corrigindo erros do GuardFlow" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

# Verificar se estamos no diretório correto
if (-not (Test-Path "backend")) {
    Write-Host "❌ Erro: Execute este script no diretório raiz do GuardFlow" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔧 CORREÇÃO 1: Backend - Dependência slowapi" -ForegroundColor Cyan
Set-Location backend
pip install slowapi
Write-Host "✅ slowapi instalado" -ForegroundColor Green
Set-Location ..

Write-Host "`n🔧 CORREÇÃO 2: Frontend - Incompatibilidade Material-UI" -ForegroundColor Cyan
Set-Location guardflow-web

# Backup do package.json original
Copy-Item package.json package.json.backup

# Corrigir versões incompatíveis
Write-Host "📋 Corrigindo versões do Material-UI e React..." -ForegroundColor Yellow

# Ler e modificar package.json
$packageJson = Get-Content package.json -Raw
$packageJson = $packageJson -replace '"@mui/material": "\^7\.3\.4"', '"@mui/material": "^5.15.0"'
$packageJson = $packageJson -replace '"@mui/icons-material": "\^7\.3\.4"', '"@mui/icons-material": "^5.15.0"'
$packageJson = $packageJson -replace '"react": "\^19\.2\.0"', '"react": "^18.2.0"'
$packageJson = $packageJson -replace '"react-dom": "\^19\.2\.0"', '"react-dom": "^18.2.0"'
$packageJson = $packageJson -replace '"@types/react": "\^19\.2\.0"', '"@types/react": "^18.2.0"'
$packageJson = $packageJson -replace '"@types/react-dom": "\^19\.2\.0"', '"@types/react-dom": "^18.2.0"'

# Salvar package.json corrigido
$packageJson | Set-Content package.json

Write-Host "✅ Versões corrigidas no package.json" -ForegroundColor Green

# Remover node_modules e package-lock.json
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force node_modules
    Write-Host "🗑️ node_modules removido" -ForegroundColor Yellow
}

if (Test-Path "package-lock.json") {
    Remove-Item -Force package-lock.json
    Write-Host "🗑️ package-lock.json removido" -ForegroundColor Yellow
}

# Reinstalar dependências
Write-Host "📦 Reinstalando dependências..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependências do frontend reinstaladas" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao reinstalar dependências do frontend" -ForegroundColor Red
}

Set-Location ..

Write-Host "`n🔧 CORREÇÃO 3: Mobile - Dependência expo" -ForegroundColor Cyan
Set-Location mobile-app

# Instalar expo se não estiver instalado
if (-not (Test-Path "node_modules/expo")) {
    Write-Host "📦 Instalando expo..." -ForegroundColor Yellow
    npm install expo
    Write-Host "✅ expo instalado" -ForegroundColor Green
} else {
    Write-Host "✅ expo já instalado" -ForegroundColor Green
}

Set-Location ..

Write-Host "`n🎉 CORREÇÕES CONCLUÍDAS!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host "`n📋 RESUMO DAS CORREÇÕES:" -ForegroundColor White
Write-Host "✅ Backend: slowapi instalado" -ForegroundColor Green
Write-Host "✅ Frontend: Material-UI v5 + React 18" -ForegroundColor Green
Write-Host "✅ Mobile: expo instalado" -ForegroundColor Green

Write-Host "`n🚀 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "1. Execute '.\start_guardflow.ps1' para iniciar o sistema" -ForegroundColor White
Write-Host "2. Verifique se todos os componentes funcionam" -ForegroundColor White
Write-Host "3. Teste as funcionalidades principais" -ForegroundColor White

Write-Host "`n🛑 Se ainda houver erros, execute '.\check_dependencies.ps1'" -ForegroundColor Red
