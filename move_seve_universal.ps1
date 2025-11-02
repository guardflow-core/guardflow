# Script para mover SEVE-UNIVERSAL para o diretório correto
$sourcePath = "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow\SEVE-UNIVERSAL"
$destinationPath = "C:\Users\João\Desktop\PROJETOS\00_ECOSYSTEM_COMERCIAL\SEVE-FRAMEWORK"

# Verificar se o diretório de origem existe
if (Test-Path $sourcePath) {
    Write-Host "Diretório de origem encontrado: $sourcePath"
    
    # Criar diretório de destino se não existir
    if (-not (Test-Path $destinationPath)) {
        New-Item -ItemType Directory -Path $destinationPath -Force
        Write-Host "Diretório de destino criado: $destinationPath"
    }
    
    # Mover todos os arquivos e pastas
    Get-ChildItem -Path $sourcePath -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($sourcePath.Length + 1)
        $targetPath = Join-Path $destinationPath $relativePath
        
        if ($_.PSIsContainer) {
            # É um diretório
            if (-not (Test-Path $targetPath)) {
                New-Item -ItemType Directory -Path $targetPath -Force
                Write-Host "Diretório criado: $targetPath"
            }
        } else {
            # É um arquivo
            $targetDir = Split-Path $targetPath -Parent
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force
            }
            Copy-Item -Path $_.FullName -Destination $targetPath -Force
            Write-Host "Arquivo copiado: $targetPath"
        }
    }
    
    Write-Host "Movimentação concluída com sucesso!"
    
    # Verificar se a movimentação foi bem-sucedida
    $filesInDestination = Get-ChildItem -Path $destinationPath -Recurse | Measure-Object
    Write-Host "Total de itens no destino: $($filesInDestination.Count)"
    
} else {
    Write-Host "Diretório de origem não encontrado: $sourcePath"
    Write-Host "Verificando diretórios disponíveis..."
    Get-ChildItem -Path "C:\Users\João\Desktop\PROJETOS\02_ORGANIZATIONS\GuardFlow" | Select-Object Name
}
