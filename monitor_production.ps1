# monitor_production.ps1
# Script para monitoramento do GuardFlow em produção

Write-Host "📊 Monitoramento do GuardFlow em Produção" -ForegroundColor Green

# Função para verificar saúde do serviço
function Test-ServiceHealth {
    param(
        [string]$ServiceName,
        [string]$Url,
        [string]$ExpectedStatus = "healthy"
    )
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method GET -TimeoutSec 10
        if ($response.status -eq $ExpectedStatus) {
            Write-Host "✅ $ServiceName: $($response.status)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️ $ServiceName: $($response.status)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "❌ $ServiceName: Erro de conexão" -ForegroundColor Red
        return $false
    }
}

# Função para verificar métricas
function Get-ServiceMetrics {
    param(
        [string]$ServiceName,
        [string]$Url
    )
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method GET -TimeoutSec 10
        Write-Host "📈 $ServiceName Metrics:" -ForegroundColor Cyan
        Write-Host "  Response Time: $($response.response_time)ms" -ForegroundColor White
        Write-Host "  Memory Usage: $($response.memory_usage)MB" -ForegroundColor White
        Write-Host "  CPU Usage: $($response.cpu_usage)%" -ForegroundColor White
        Write-Host "  Active Connections: $($response.active_connections)" -ForegroundColor White
    } catch {
        Write-Host "❌ $ServiceName: Erro ao obter métricas" -ForegroundColor Red
    }
}

# Verificar serviços
Write-Host "🔍 Verificando saúde dos serviços..." -ForegroundColor Yellow

# Backend
$backendHealth = Test-ServiceHealth -ServiceName "Backend" -Url "http://localhost:8002/health"

# Frontend
$frontendHealth = Test-ServiceHealth -ServiceName "Frontend" -Url "http://localhost:3000"

# Banco de dados
$dbHealth = Test-ServiceHealth -ServiceName "Database" -Url "http://localhost:8002/health/database"

# Redis
$redisHealth = Test-ServiceHealth -ServiceName "Redis" -Url "http://localhost:8002/health/redis"

# SYMBEON Integration
$symbeonHealth = Test-ServiceHealth -ServiceName "SYMBEON" -Url "http://localhost:8002/health/symbeon"

# ESG Engine
$esgHealth = Test-ServiceHealth -ServiceName "ESG Engine" -Url "http://localhost:8002/health/esg"

Write-Host "`n📊 Métricas de Performance:" -ForegroundColor Yellow

# Obter métricas do backend
Get-ServiceMetrics -ServiceName "Backend" -Url "http://localhost:8002/metrics"

# Obter métricas do frontend
Get-ServiceMetrics -ServiceName "Frontend" -Url "http://localhost:3000/metrics"

# Verificar logs de erro
Write-Host "`n📋 Verificando logs de erro..." -ForegroundColor Yellow

try {
    $errorLogs = Invoke-RestMethod -Uri "http://localhost:8002/logs/errors" -Method GET
    if ($errorLogs.count -eq 0) {
        Write-Host "✅ Nenhum erro encontrado nos logs" -ForegroundColor Green
    } else {
        Write-Host "⚠️ $($errorLogs.count) erros encontrados nos logs" -ForegroundColor Yellow
        foreach ($log in $errorLogs) {
            Write-Host "  - $($log.timestamp): $($log.message)" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "❌ Erro ao obter logs" -ForegroundColor Red
}

# Verificar uso de recursos
Write-Host "`n💻 Uso de Recursos:" -ForegroundColor Yellow

# CPU
try {
    $cpuUsage = Get-Counter -Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 1
    Write-Host "CPU Usage: $([math]::Round($cpuUsage.CounterSamples[0].CookedValue, 2))%" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao obter uso de CPU" -ForegroundColor Red
}

# Memória
try {
    $memory = Get-Counter -Counter "\Memory\Available MBytes" -SampleInterval 1 -MaxSamples 1
    $totalMemory = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory / 1MB
    $usedMemory = $totalMemory - $memory.CounterSamples[0].CookedValue
    $memoryUsage = ($usedMemory / $totalMemory) * 100
    Write-Host "Memory Usage: $([math]::Round($memoryUsage, 2))%" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao obter uso de memória" -ForegroundColor Red
}

# Disco
try {
    $disk = Get-Counter -Counter "\LogicalDisk(C:)\% Free Space" -SampleInterval 1 -MaxSamples 1
    $diskUsage = 100 - $disk.CounterSamples[0].CookedValue
    Write-Host "Disk Usage: $([math]::Round($diskUsage, 2))%" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao obter uso de disco" -ForegroundColor Red
}

# Relatório final
Write-Host "`n📊 RELATÓRIO DE MONITORAMENTO:" -ForegroundColor Green

$totalServices = 6
$healthyServices = 0

if ($backendHealth) { $healthyServices++ }
if ($frontendHealth) { $healthyServices++ }
if ($dbHealth) { $healthyServices++ }
if ($redisHealth) { $healthyServices++ }
if ($symbeonHealth) { $healthyServices++ }
if ($esgHealth) { $healthyServices++ }

$healthPercentage = ($healthyServices / $totalServices) * 100

Write-Host "Serviços Saudáveis: $healthyServices/$totalServices ($([math]::Round($healthPercentage, 1))%)" -ForegroundColor Cyan

if ($healthPercentage -ge 90) {
    Write-Host "🎉 Sistema funcionando perfeitamente!" -ForegroundColor Green
} elseif ($healthPercentage -ge 70) {
    Write-Host "⚠️ Sistema funcionando com alguns problemas" -ForegroundColor Yellow
} else {
    Write-Host "🚨 Sistema com problemas críticos!" -ForegroundColor Red
}

Write-Host "`n📋 URLs de Acesso:" -ForegroundColor Yellow
Write-Host "  Backend API: http://localhost:8002" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "  Health Check: http://localhost:8002/health" -ForegroundColor Cyan
Write-Host "  Metrics: http://localhost:8002/metrics" -ForegroundColor Cyan

Write-Host "`n🔄 Para monitoramento contínuo, execute este script a cada 5 minutos" -ForegroundColor Yellow
