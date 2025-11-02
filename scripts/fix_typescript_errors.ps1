# 🔧 GUARDFLOW - CORRIGIR ERROS TYPESCRIPT
# Script para corrigir erros TypeScript automaticamente

Write-Host "🔧 GUARDFLOW - CORRIGINDO ERROS TYPESCRIPT" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# 1. Corrigir imports de ícones inexistentes
Write-Host "`n📦 1. CORRIGINDO IMPORTS DE ÍCONES..." -ForegroundColor Yellow

# Remover Eco (não existe)
(Get-Content guardflow-web/src/pages/QRCheckoutDemo.tsx) | 
    ForEach-Object { $_ -replace "  Eco,", "  // Eco," } | 
    Set-Content guardflow-web/src/pages/QRCheckoutDemo.tsx

# Remover EcoIcon (não existe)
(Get-Content guardflow-web/src/pages/ScannerPage.tsx) | 
    ForEach-Object { $_ -replace "  EcoIcon,", "  // EcoIcon," } | 
    Set-Content guardflow-web/src/pages/ScannerPage.tsx

# Remover Integration (não existe)
(Get-Content guardflow-web/src/pages/Settings.tsx) | 
    ForEach-Object { $_ -replace "  Integration,", "  // Integration," } | 
    Set-Content guardflow-web/src/pages/Settings.tsx

# Remover Theme (não existe)
(Get-Content guardflow-web/src/pages/Settings.tsx) | 
    ForEach-Object { $_ -replace "  Theme,", "  // Theme," } | 
    Set-Content guardflow-web/src/pages/Settings.tsx

Write-Host "✅ Imports de ícones corrigidos" -ForegroundColor Green

# 2. Instalar dependências faltantes
Write-Host "`n📦 2. INSTALANDO DEPENDÊNCIAS FALTANTES..." -ForegroundColor Yellow

cd guardflow-web
npm install recharts @types/recharts --save
Write-Host "✅ Recharts instalado" -ForegroundColor Green

# 3. Compilar para verificar erros restantes
Write-Host "`n🔨 3. COMPILANDO TYPESCRIPT..." -ForegroundColor Yellow

npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Compilação bem sucedida!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Ainda há erros de compilação" -ForegroundColor Yellow
    Write-Host "Execute 'npm run build' para ver detalhes" -ForegroundColor Yellow
}

cd ..

Write-Host "`n🎉 CORREÇÃO DE ERROS TYPESCRIPT FINALIZADA!" -ForegroundColor Green
Write-Host "Execute 'cd guardflow-web && npm start' para testar" -ForegroundColor Cyan



