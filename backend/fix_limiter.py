#!/usr/bin/env python3
"""
Script para corrigir automaticamente os problemas do slowapi limiter
Adiciona o parâmetro 'request: Request' em todas as funções que usam @limiter.limit()
"""

import os
import re
from pathlib import Path

def fix_limiter_in_file(file_path):
    """Corrige os problemas do limiter em um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Padrão para encontrar funções com @limiter.limit() sem request
        pattern = r'@limiter\.limit\([^)]+\)\s*\n\s*async def (\w+)\s*\(\s*([^)]*)\s*\):'
        
        def replace_func(match):
            func_name = match.group(1)
            params = match.group(2).strip()
            
            # Se já tem request, não alterar
            if 'request: Request' in params:
                return match.group(0)
            
            # Adicionar request: Request no início dos parâmetros
            if params:
                new_params = f"request: Request, {params}"
            else:
                new_params = "request: Request"
            
            return f"@limiter.limit({match.group(0).split('@limiter.limit(')[1].split(')')[0]})\n    async def {func_name}({new_params}):"
        
        # Aplicar a correção
        new_content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
        
        # Se houve mudanças, salvar o arquivo
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Corrigido: {file_path}")
            return True
        else:
            print(f"ℹ️  Nenhuma correção necessária: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def main():
    """Executa a correção em todos os arquivos da API"""
    api_dir = Path("app/api")
    
    if not api_dir.exists():
        print("❌ Diretório app/api não encontrado")
        return
    
    files_fixed = 0
    
    # Processar todos os arquivos Python na pasta API
    for py_file in api_dir.glob("*.py"):
        if py_file.name != "__init__.py":
            if fix_limiter_in_file(py_file):
                files_fixed += 1
    
    print(f"\n🎯 Correção concluída! {files_fixed} arquivos foram corrigidos.")

if __name__ == "__main__":
    main()
