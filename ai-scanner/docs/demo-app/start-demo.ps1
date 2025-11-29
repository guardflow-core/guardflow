# Agilizia_AI Demo App - Script de Inicialização
# PowerShell script para iniciar o app de demonstração

Write-Host "🚀 Agilizia_AI - App de Demonstração" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instalando..." -ForegroundColor Red
    Write-Host "Por favor, instale Python 3.7+ de https://python.org" -ForegroundColor Yellow
    exit 1
}

# Verificar se estamos na pasta correta
if (-not (Test-Path "index.html")) {
    Write-Host "❌ Arquivo index.html não encontrado!" -ForegroundColor Red
    Write-Host "Certifique-se de estar na pasta docs/demo-app/" -ForegroundColor Yellow
    exit 1
}

Write-Host "📁 Pasta atual: $(Get-Location)" -ForegroundColor Blue

# Iniciar servidor HTTP
Write-Host "🌐 Iniciando servidor HTTP..." -ForegroundColor Yellow
Write-Host "📱 Acesse: http://localhost:8000" -ForegroundColor Green
Write-Host "🛑 Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor Python
try {
    python -m http.server 8000
} catch {
    Write-Host "❌ Erro ao iniciar servidor HTTP" -ForegroundColor Red
    Write-Host "Tentando método alternativo..." -ForegroundColor Yellow
    
    # Método alternativo com Node.js
    try {
        npx http-server -p 8000
    } catch {
        Write-Host "❌ Erro ao iniciar servidor alternativo" -ForegroundColor Red
        Write-Host "Abra o arquivo index.html diretamente no navegador" -ForegroundColor Yellow
    }
}