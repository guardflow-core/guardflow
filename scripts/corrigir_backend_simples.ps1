# Corrigir Backend - Script Simples
Write-Host "Corrigindo Backend..." -ForegroundColor Green

# Encontrar GuardFlow
$guardflow = Get-ChildItem -Path "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS" -Name "GuardFlow" -Directory
if ($guardflow) {
    $path = "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\$guardflow"
    Write-Host "Encontrado: $path" -ForegroundColor Green
    Set-Location $path
    
    # Verificar backend
    if (Test-Path "backend") {
        Write-Host "Backend existe" -ForegroundColor Green
        Set-Location backend
        
        # Criar main.py se não existir
        if (-not (Test-Path "app\main.py")) {
            Write-Host "Criando app/main.py..." -ForegroundColor Yellow
            New-Item -ItemType Directory -Path "app" -Force | Out-Null
            
            $main = @"
from fastapi import FastAPI

app = FastAPI(title="GuardFlow API")

@app.get("/")
async def root():
    return {"message": "GuardFlow API funcionando!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
"@
            $main | Out-File -FilePath "app\main.py" -Encoding UTF8
        }
        
        # Criar requirements.txt
        if (-not (Test-Path "requirements.txt")) {
            Write-Host "Criando requirements.txt..." -ForegroundColor Yellow
            $req = @"
fastapi==0.104.1
uvicorn[standard]==0.24.0
"@
            $req | Out-File -FilePath "requirements.txt" -Encoding UTF8
        }
        
        # Instalar dependências
        Write-Host "Instalando dependências..." -ForegroundColor Yellow
        pip install fastapi uvicorn
        
        # Testar
        Write-Host "Testando backend..." -ForegroundColor Yellow
        python -m uvicorn app.main:app --reload --port 8000 &
        
        Start-Sleep -Seconds 3
        
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
            Write-Host "SUCCESS: Backend funcionando!" -ForegroundColor Green
        } catch {
            Write-Host "ERROR: Backend não funcionando" -ForegroundColor Red
        }
        
    } else {
        Write-Host "Backend não encontrado" -ForegroundColor Red
    }
} else {
    Write-Host "GuardFlow não encontrado" -ForegroundColor Red
}


