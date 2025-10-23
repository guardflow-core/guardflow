# 🔧 GUARDFLOW - CORRIGIR TODOS OS ERROS TYPESCRIPT
# Script abrangente para corrigir todos os erros TypeScript

Write-Host "🔧 GUARDFLOW - CORRIGINDO TODOS OS ERROS TYPESCRIPT" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green

cd guardflow-web

# 1. Corrigir imports de ícones inexistentes
Write-Host "`n📦 1. CORRIGINDO IMPORTS DE ÍCONES..." -ForegroundColor Yellow

# Remover Eco (não existe) - QRCheckoutDemo.tsx
(Get-Content src/pages/QRCheckoutDemo.tsx) | 
    ForEach-Object { 
        $_ -replace "  Eco,", "  // Eco," -replace
        "icon={<Eco />}", "icon={<Nature />}" -replace
        "Cannot find name 'Eco'", "// Eco icon removed"
    } | 
    Set-Content src/pages/QRCheckoutDemo.tsx

# Remover EcoIcon (não existe) - ScannerPage.tsx
(Get-Content src/pages/ScannerPage.tsx) | 
    ForEach-Object { 
        $_ -replace "  EcoIcon,", "  // EcoIcon," -replace
        "icon={<EcoIcon />}", "icon={<Nature />}"
    } | 
    Set-Content src/pages/ScannerPage.tsx

# Corrigir Database (não existe) - Monitoring.tsx
(Get-Content src/pages/Monitoring.tsx) | 
    ForEach-Object { 
        $_ -replace "  Database,", "  // Database," -replace
        "icon: <Database />", "icon: <Storage />" -replace
        "Cannot find name 'Database'", "// Database icon replaced with Storage"
    } | 
    Set-Content src/pages/Monitoring.tsx

# Remover Integration e Theme (não existem) - Settings.tsx
(Get-Content src/pages/Settings.tsx) | 
    ForEach-Object { 
        $_ -replace "  Integration,", "  // Integration," -replace
        "  Theme,", "  // Theme,"
    } | 
    Set-Content src/pages/Settings.tsx

Write-Host "✅ Imports de ícones corrigidos" -ForegroundColor Green

# 2. Corrigir erros de tipos
Write-Host "`n🔧 2. CORRIGINDO ERROS DE TIPOS..." -ForegroundColor Yellow

# Corrigir color prop em QRCheckoutDemo.tsx
(Get-Content src/pages/QRCheckoutDemo.tsx) | 
    ForEach-Object { 
        $_ -replace "color={guardpassEnabled \? 'primary' : 'default'}", "color={guardpassEnabled ? 'primary' : 'inherit'}"
    } | 
    Set-Content src/pages/QRCheckoutDemo.tsx

# Corrigir tipos em UsersPage.tsx
(Get-Content src/pages/UsersPage.tsx) | 
    ForEach-Object { 
        $_ -replace "role: string", "role: 'admin' | 'manager' | 'cashier' | 'customer'" -replace
        "type: string", "type: 'payment' | 'analytics' | 'erp' | 'notification'"
    } | 
    Set-Content src/pages/UsersPage.tsx

# Corrigir spread types em Settings.tsx
(Get-Content src/pages/Settings.tsx) | 
    ForEach-Object { 
        $_ -replace "\.\.\.prev\[parent as keyof typeof prev\]", "...(prev[parent] || {})"
    } | 
    Set-Content src/pages/Settings.tsx

Write-Host "✅ Erros de tipos corrigidos" -ForegroundColor Green

# 3. Instalar dependências faltantes
Write-Host "`n📦 3. INSTALANDO DEPENDÊNCIAS FALTANTES..." -ForegroundColor Yellow

npm install @types/recharts --save-dev
Write-Host "✅ @types/recharts instalado" -ForegroundColor Green

# 4. Corrigir imports de redux-persist
Write-Host "`n🔄 4. CORRIGINDO REDUX-PERSIST..." -ForegroundColor Yellow

# Verificar se redux-persist está instalado
if (!(Test-Path "node_modules/redux-persist")) {
    npm install redux-persist
    Write-Host "✅ redux-persist instalado" -ForegroundColor Green
} else {
    Write-Host "✅ redux-persist já instalado" -ForegroundColor Green
}

# 5. Compilar para verificar erros restantes
Write-Host "`n🔨 5. COMPILANDO TYPESCRIPT..." -ForegroundColor Yellow

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
