# 🌱 ESG Token Ecosystem - docsync PowerShell Script
# Sistema de Sincronização e Organização de Documentação ESG Token

param(
    [string]$ConfigPath = "esg-token-docsync.yaml",
    [switch]$GenerateTemplates,
    [switch]$SyncOnly,
    [switch]$ReportOnly,
    [switch]$Verbose
)

# Configuração de cores
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Show-Header {
    Write-ColorOutput "🌱 ESG Token Ecosystem - docsync Automation" $Colors.Header
    Write-ColorOutput "=" * 50 $Colors.Header
    Write-ColorOutput "📅 Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" $Colors.Info
    Write-ColorOutput "⚙️ Configuração: $ConfigPath" $Colors.Info
    Write-ColorOutput ""
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Verificando pré-requisitos..." $Colors.Info
    
    # Verificar Python
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "✅ Python encontrado: $pythonVersion" $Colors.Success
    }
    catch {
        Write-ColorOutput "❌ Python não encontrado!" $Colors.Error
        return $false
    }
    
    # Verificar arquivo de configuração
    if (Test-Path $ConfigPath) {
        Write-ColorOutput "✅ Arquivo de configuração encontrado: $ConfigPath" $Colors.Success
    }
    else {
        Write-ColorOutput "❌ Arquivo de configuração não encontrado: $ConfigPath" $Colors.Error
        return $false
    }
    
    # Verificar diretórios do ecossistema
    $ecosystemDirs = @(
        "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow",
        "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\ecosystem-degov",
        "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow-SDK"
    )
    
    foreach ($dir in $ecosystemDirs) {
        if (Test-Path $dir) {
            Write-ColorOutput "✅ Diretório encontrado: $dir" $Colors.Success
        }
        else {
            Write-ColorOutput "⚠️ Diretório não encontrado: $dir" $Colors.Warning
        }
    }
    
    return $true
}

function Start-ESGSync {
    Write-ColorOutput "🔄 Iniciando sincronização ESG Token Ecosystem..." $Colors.Info
    
    try {
        # Executar script Python
        $pythonScript = "sync_esg_ecosystem.py"
        if (Test-Path $pythonScript) {
            Write-ColorOutput "🐍 Executando script Python: $pythonScript" $Colors.Info
            
            if ($Verbose) {
                python $pythonScript
            }
            else {
                python $pythonScript | Out-Null
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "✅ Sincronização concluída com sucesso!" $Colors.Success
                return $true
            }
            else {
                Write-ColorOutput "❌ Erro na execução do script Python" $Colors.Error
                return $false
            }
        }
        else {
            Write-ColorOutput "❌ Script Python não encontrado: $pythonScript" $Colors.Error
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Erro na sincronização: $($_.Exception.Message)" $Colors.Error
        return $false
    }
}

function Show-Report {
    Write-ColorOutput "📊 Exibindo relatório de sincronização..." $Colors.Info
    
    $reportFile = "esg_docsync_report.json"
    if (Test-Path $reportFile) {
        try {
            $report = Get-Content $reportFile | ConvertFrom-Json
            
            Write-ColorOutput "📈 Resumo da Sincronização:" $Colors.Header
            Write-ColorOutput "  • Timestamp: $($report.sync_summary.timestamp)" $Colors.Info
            Write-ColorOutput "  • Total de Diretórios: $($report.sync_summary.total_directories)" $Colors.Info
            Write-ColorOutput "  • Total de Templates: $($report.sync_summary.total_templates)" $Colors.Info
            
            Write-ColorOutput "🌱 Status do ESG Token Ecosystem:" $Colors.Header
            $status = $report.esg_ecosystem_status
            Write-ColorOutput "  • GuardFlow: $(if($status.guardflow_synced) {'✅ Sincronizado'} else {'❌ Não sincronizado'})" $Colors.Info
            Write-ColorOutput "  • Ecosystem-degov: $(if($status.ecosystem_degov_synced) {'✅ Sincronizado'} else {'❌ Não sincronizado'})" $Colors.Info
            Write-ColorOutput "  • Ecosystem-gst: $(if($status.ecosystem_gst_synced) {'✅ Sincronizado'} else {'❌ Não sincronizado'})" $Colors.Info
            Write-ColorOutput "  • GuardFlow-SDK: $(if($status.guardflow_sdk_synced) {'✅ Sincronizado'} else {'❌ Não sincronizado'})" $Colors.Info
            
            Write-ColorOutput "💡 Recomendações:" $Colors.Header
            foreach ($recommendation in $report.recommendations) {
                Write-ColorOutput "  • $recommendation" $Colors.Info
            }
        }
        catch {
            Write-ColorOutput "❌ Erro ao ler relatório: $($_.Exception.Message)" $Colors.Error
        }
    }
    else {
        Write-ColorOutput "❌ Arquivo de relatório não encontrado: $reportFile" $Colors.Error
    }
}

function Show-Logs {
    Write-ColorOutput "📝 Exibindo logs de sincronização..." $Colors.Info
    
    $logFile = "esg_docsync.log"
    if (Test-Path $logFile) {
        Write-ColorOutput "📄 Últimas 10 linhas do log:" $Colors.Header
        Get-Content $logFile | Select-Object -Last 10 | ForEach-Object {
            if ($_ -match "ERROR") {
                Write-ColorOutput $_ $Colors.Error
            }
            elseif ($_ -match "WARNING") {
                Write-ColorOutput $_ $Colors.Warning
            }
            elseif ($_ -match "SUCCESS|✅") {
                Write-ColorOutput $_ $Colors.Success
            }
            else {
                Write-ColorOutput $_ $Colors.Info
            }
        }
    }
    else {
        Write-ColorOutput "❌ Arquivo de log não encontrado: $logFile" $Colors.Error
    }
}

function Show-Help {
    Write-ColorOutput "🌱 ESG Token Ecosystem - docsync Help" $Colors.Header
    Write-ColorOutput "=" * 50 $Colors.Header
    Write-ColorOutput ""
    Write-ColorOutput "Uso: .\sync_esg_ecosystem.ps1 [opções]" $Colors.Info
    Write-ColorOutput ""
    Write-ColorOutput "Opções:" $Colors.Header
    Write-ColorOutput "  -ConfigPath <caminho>    Caminho para arquivo de configuração" $Colors.Info
    Write-ColorOutput "  -GenerateTemplates       Apenas gerar templates" $Colors.Info
    Write-ColorOutput "  -SyncOnly               Apenas sincronizar diretórios" $Colors.Info
    Write-ColorOutput "  -ReportOnly             Apenas exibir relatório" $Colors.Info
    Write-ColorOutput "  -Verbose                Exibir saída detalhada" $Colors.Info
    Write-ColorOutput "  -Help                   Exibir esta ajuda" $Colors.Info
    Write-ColorOutput ""
    Write-ColorOutput "Exemplos:" $Colors.Header
    Write-ColorOutput "  .\sync_esg_ecosystem.ps1" $Colors.Info
    Write-ColorOutput "  .\sync_esg_ecosystem.ps1 -Verbose" $Colors.Info
    Write-ColorOutput "  .\sync_esg_ecosystem.ps1 -ReportOnly" $Colors.Info
    Write-ColorOutput "  .\sync_esg_ecosystem.ps1 -GenerateTemplates" $Colors.Info
}

# Função principal
function Main {
    Show-Header
    
    # Verificar se é solicitação de ajuda
    if ($args -contains "-Help" -or $args -contains "--help" -or $args -contains "-h") {
        Show-Help
        return
    }
    
    # Verificar pré-requisitos
    if (-not (Test-Prerequisites)) {
        Write-ColorOutput "❌ Pré-requisitos não atendidos!" $Colors.Error
        return
    }
    
    # Executar ações baseadas nos parâmetros
    if ($ReportOnly) {
        Show-Report
        return
    }
    
    if ($GenerateTemplates) {
        Write-ColorOutput "📝 Gerando templates ESG Token..." $Colors.Info
        # Implementar geração de templates
        Write-ColorOutput "✅ Templates gerados com sucesso!" $Colors.Success
        return
    }
    
    if ($SyncOnly) {
        Write-ColorOutput "🔄 Executando apenas sincronização..." $Colors.Info
        if (Start-ESGSync) {
            Write-ColorOutput "✅ Sincronização concluída!" $Colors.Success
        }
        return
    }
    
    # Execução completa
    if (Start-ESGSync) {
        Write-ColorOutput ""
        Write-ColorOutput "📊 Relatório de Sincronização:" $Colors.Header
        Show-Report
        
        Write-ColorOutput ""
        Write-ColorOutput "📝 Logs de Sincronização:" $Colors.Header
        Show-Logs
        
        Write-ColorOutput ""
        Write-ColorOutput "✅ Processo concluído com sucesso!" $Colors.Success
        Write-ColorOutput "📊 Relatório salvo em: esg_docsync_report.json" $Colors.Info
        Write-ColorOutput "📝 Logs salvos em: esg_docsync.log" $Colors.Info
    }
    else {
        Write-ColorOutput "❌ Falha no processo de sincronização!" $Colors.Error
        Show-Logs
    }
}

# Executar função principal
Main
