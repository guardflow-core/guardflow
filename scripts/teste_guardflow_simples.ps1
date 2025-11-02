# 🧪 GUARDFLOW - TESTE SIMPLES DO SISTEMA
# Script para testar as funcionalidades básicas do GuardFlow

Write-Host "🧪 GUARDFLOW - TESTE SIMPLES DO SISTEMA" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# 1. Verificar estrutura do projeto
Write-Host "`n📁 1. VERIFICANDO ESTRUTURA DO PROJETO..." -ForegroundColor Yellow

$directories = @(
    "backend",
    "guardflow-web", 
    "mobile",
    "docs",
    "scripts"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "✅ $dir - Existe" -ForegroundColor Green
    } else {
        Write-Host "❌ $dir - Não encontrado" -ForegroundColor Red
    }
}

# 2. Verificar arquivos principais
Write-Host "`n📄 2. VERIFICANDO ARQUIVOS PRINCIPAIS..." -ForegroundColor Yellow

$files = @(
    "backend/app/main.py",
    "backend/requirements.txt",
    "guardflow-web/package.json",
    "mobile/package.json",
    "docs/PRESENTACAO_IMPRESSIONANTE_GUARDFLOW.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file - Existe" -ForegroundColor Green
    } else {
        Write-Host "❌ $file - Não encontrado" -ForegroundColor Red
    }
}

# 3. Verificar APIs implementadas
Write-Host "`n🔧 3. VERIFICANDO APIs IMPLEMENTADAS..." -ForegroundColor Yellow

$apis = @(
    "backend/app/api/auth.py",
    "backend/app/api/users.py",
    "backend/app/api/products.py",
    "backend/app/api/scanner.py",
    "backend/app/api/payment.py",
    "backend/app/api/esg_engine.py",
    "backend/app/api/checkout_symbiotic_agent.py"
)

foreach ($api in $apis) {
    if (Test-Path $api) {
        Write-Host "✅ $api - Implementada" -ForegroundColor Green
    } else {
        Write-Host "❌ $api - Não encontrada" -ForegroundColor Red
    }
}

# 4. Verificar componentes React
Write-Host "`n🎨 4. VERIFICANDO COMPONENTES REACT..." -ForegroundColor Yellow

$components = @(
    "guardflow-web/src/App.tsx",
    "guardflow-web/src/components/Dashboard.tsx",
    "guardflow-web/src/pages/Dashboard.tsx",
    "guardflow-web/src/pages/Markets.tsx",
    "guardflow-web/src/pages/Analytics.tsx",
    "guardflow-web/src/store/index.ts"
)

foreach ($component in $components) {
    if (Test-Path $component) {
        Write-Host "✅ $component - Implementado" -ForegroundColor Green
    } else {
        Write-Host "❌ $component - Não encontrado" -ForegroundColor Red
    }
}

# 5. Verificar mobile app
Write-Host "`n📱 5. VERIFICANDO MOBILE APP..." -ForegroundColor Yellow

$mobileFiles = @(
    "mobile/App.tsx",
    "mobile/src/screens/ScannerScreen.tsx",
    "mobile/src/screens/CartScreen.tsx",
    "mobile/src/screens/ESGScreen.tsx",
    "mobile/src/navigation/AppNavigator.tsx"
)

foreach ($file in $mobileFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file - Implementado" -ForegroundColor Green
    } else {
        Write-Host "❌ $file - Não encontrado" -ForegroundColor Red
    }
}

# 6. Verificar documentação
Write-Host "`n📚 6. VERIFICANDO DOCUMENTAÇÃO..." -ForegroundColor Yellow

$docs = @(
    "docs/PRESENTACAO_IMPRESSIONANTE_GUARDFLOW.md",
    "docs/SEVE_CARE_DOCUMENTATION.md",
    "docs/EAP_GUARDFLOW_V3_COMPLETA.md",
    "docs/demo-app/index.html"
)

foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "✅ $doc - Disponível" -ForegroundColor Green
    } else {
        Write-Host "❌ $doc - Não encontrado" -ForegroundColor Red
    }
}

# 7. Resumo do teste
Write-Host "`n📊 7. RESUMO DO TESTE:" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Green

$totalFiles = $files.Count + $apis.Count + $components.Count + $mobileFiles.Count + $docs.Count
$foundFiles = 0

foreach ($file in ($files + $apis + $components + $mobileFiles + $docs)) {
    if (Test-Path $file) {
        $foundFiles++
    }
}

$percentage = [math]::Round(($foundFiles / $totalFiles) * 100, 1)

Write-Host "📁 Arquivos verificados: $totalFiles" -ForegroundColor White
Write-Host "✅ Arquivos encontrados: $foundFiles" -ForegroundColor Green
Write-Host "📊 Percentual de completude: $percentage%" -ForegroundColor Cyan

if ($percentage -ge 90) {
    Write-Host "🎉 SISTEMA GUARDFLOW COMPLETO!" -ForegroundColor Green
    Write-Host "🚀 Pronto para demonstração!" -ForegroundColor Green
} elseif ($percentage -ge 70) {
    Write-Host "⚠️ Sistema quase completo" -ForegroundColor Yellow
    Write-Host "🔧 Alguns ajustes necessários" -ForegroundColor Yellow
} else {
    Write-Host "❌ Sistema incompleto" -ForegroundColor Red
    Write-Host "🛠️ Muitos arquivos faltando" -ForegroundColor Red
}

Write-Host "`n🎪 TESTE SIMPLES FINALIZADO!" -ForegroundColor Green



