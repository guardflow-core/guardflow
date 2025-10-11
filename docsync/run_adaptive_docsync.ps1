# run_adaptive_docsync.ps1
# Script PowerShell para executar o sistema adaptativo completo do DocSync

param(
    [switch]$Verbose,
    [switch]$SingleCycle,
    [switch]$ContinuousAdaptation,
    [int]$MaxCycles = 5,
    [switch]$LearningOnly,
    [switch]$StructureOnly,
    [switch]$AutoOrganizationOnly,
    [string]$ConfigPath = "esg-token-docsync.yaml"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PythonScript = Join-Path $ScriptDir "adaptive_docsync_simple.py"
$ConfigFile = Join-Path $ScriptDir $ConfigPath
$LogFile = Join-Path $ScriptDir "adaptive_docsync.log"
$ReportFile = Join-Path $ScriptDir "adaptive_docsync_report.json"

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [string]$Color = "White"
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    if ($Verbose -or $Level -eq "ERROR" -or $Level -eq "WARNING") {
        Write-Host $Message -ForegroundColor $Color
    }
}

Write-Host "DocSync Adaptativo - ESG Token Ecosystem" -ForegroundColor Magenta
Write-Host "Data: $(Get-Date)" -ForegroundColor Cyan
Write-Host "Configuracao: $ConfigFile" -ForegroundColor DarkCyan

# 1. Verificar pre-requisitos
Write-Log "Verificando pre-requisitos adaptativos..." "INFO" "DarkYellow"

# Verificar Python
try {
    $pythonVersion = (python --version 2>&1).ToString()
    if ($pythonVersion -match "Python") {
        Write-Log "Python encontrado: $pythonVersion" "INFO" "Green"
    } else {
        Write-Log "Python nao encontrado. Por favor, instale Python 3.x." "ERROR" "Red"
        exit 1
    }
} catch {
    Write-Log "Erro ao verificar Python: $($_.Exception.Message)" "ERROR" "Red"
    exit 1
}

# Verificar arquivo de configuracao
if (Test-Path $ConfigFile) {
    Write-Log "Arquivo de configuracao adaptativa encontrado: $ConfigFile" "INFO" "Green"
} else {
    Write-Log "Arquivo de configuracao adaptativa nao encontrado: $ConfigFile" "ERROR" "Red"
    exit 1
}

# Verificar modulos Python necessarios
$requiredModules = @("yaml", "numpy", "sklearn")
foreach ($module in $requiredModules) {
    try {
        $moduleCheck = python -c "import $module" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Modulo Python '$module' encontrado" "INFO" "Green"
        } else {
            Write-Log "Modulo Python '$module' nao encontrado. Instalando..." "WARNING" "Yellow"
            pip install $module
        }
    } catch {
        Write-Log "Erro ao verificar modulo '$module': $($_.Exception.Message)" "WARNING" "Yellow"
    }
}

# Verificar diretorios monitorados
$monitoredDirs = @(
    "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow",
    "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\ecosystem-degov",
    "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow-SDK"
)

foreach ($dir in $monitoredDirs) {
    if (Test-Path $dir) {
        Write-Log "Diretorio encontrado: $dir" "INFO" "Green"
    } else {
        Write-Log "Diretorio nao encontrado: $dir. A sincronizacao adaptativa pode ser incompleta." "WARNING" "Yellow"
    }
}

# 2. Executar o sistema adaptativo
Write-Log "Iniciando sistema adaptativo ESG Token Ecosystem..." "INFO" "Blue"

# Determinar modo de execucao
$executionMode = "full"
if ($LearningOnly) { $executionMode = "learning" }
if ($StructureOnly) { $executionMode = "structure" }
if ($AutoOrganizationOnly) { $executionMode = "auto_organization" }

Write-Log "Modo de execucao: $executionMode" "INFO" "DarkBlue"

try {
    if ($ContinuousAdaptation) {
        Write-Log "Executando adaptacao continua (maximo $MaxCycles ciclos)..." "INFO" "Blue"
        $pythonOutput = python $PythonScript --continuous --max-cycles $MaxCycles --mode $executionMode 2>&1
    } elseif ($SingleCycle) {
        Write-Log "Executando ciclo adaptativo unico..." "INFO" "Blue"
        $pythonOutput = python $PythonScript --single-cycle --mode $executionMode 2>&1
    } else {
        Write-Log "Executando sistema adaptativo padrao..." "INFO" "Blue"
        $pythonOutput = python $PythonScript --mode $executionMode 2>&1
    }
    
    $LastExitCode = $LASTEXITCODE
    
    if ($LastExitCode -eq 0) {
        Write-Log "Sistema adaptativo concluido com sucesso." "INFO" "Green"
    } else {
        Write-Log "Erro na execucao do sistema adaptativo" "ERROR" "Red"
        Write-Log "Detalhes do erro: $pythonOutput" "ERROR" "Red"
        exit 1
    }
} catch {
    Write-Log "Falha ao executar o sistema adaptativo: $($_.Exception.Message)" "ERROR" "Red"
    exit 1
}

# 3. Finalizacao e Relatorio Adaptativo
if ($LastExitCode -eq 0) {
    Write-Log "Processo adaptativo concluido com sucesso!" "INFO" "Green"
    Write-Host "Relatorio Adaptativo:" -ForegroundColor DarkCyan
    if (Test-Path $ReportFile) {
        $reportContent = Get-Content $ReportFile | ConvertFrom-Json
        Write-Host "Score de Organizacao: $($reportContent.organization_score)" -ForegroundColor Green
        Write-Host "Efetividade do Aprendizado: $($reportContent.learning_effectiveness)" -ForegroundColor Green
        Write-Host "Adaptacoes Aplicadas: $($reportContent.adaptations_applied)" -ForegroundColor Green
        Write-Host "Arquivos Criados: $($reportContent.files_created)" -ForegroundColor Green
        Write-Host "Arquivos Modificados: $($reportContent.files_modified)" -ForegroundColor Green
        Write-Host "Diretorios Criados: $($reportContent.directories_created)" -ForegroundColor Green
        Write-Host "Melhoria Geral: $($reportContent.overall_improvement)%" -ForegroundColor Green
    } else {
        Write-Log "Relatorio adaptativo nao gerado ou nao encontrado em $ReportFile." "ERROR" "Red"
    }
} else {
    Write-Log "Falha no processo adaptativo!" "ERROR" "Red"
}

Write-Host "Exibindo logs adaptativos..." -ForegroundColor DarkCyan
if (Test-Path $LogFile) {
    Write-Host "Ultimas 15 linhas do log adaptativo:" -ForegroundColor DarkGray
    Get-Content $LogFile | Select-Object -Last 15
} else {
    Write-Log "Arquivo de log adaptativo nao encontrado em $LogFile." "ERROR" "Red"
}

Write-Host "Sistema Adaptativo ESG Token Ecosystem - Concluido!" -ForegroundColor Magenta