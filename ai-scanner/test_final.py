#!/usr/bin/env python3
"""
Teste Final do Sistema GuardFlow
Script para verificar se todos os componentes estão funcionando
"""

import os
import sys
import importlib.util
from pathlib import Path

def test_backend():
    """Testa o backend"""
    print("🔧 TESTANDO BACKEND...")
    
    # Verificar se o diretório backend existe
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Diretório backend não encontrado")
        return False
    
    # Verificar arquivos principais
    main_file = backend_path / "app" / "main.py"
    if not main_file.exists():
        print("❌ Arquivo main.py não encontrado")
        return False
    
    print("✅ Estrutura backend OK")
    
    # Tentar importar FastAPI básico
    try:
        import fastapi
        print("✅ FastAPI disponível")
    except ImportError:
        print("❌ FastAPI não instalado")
        return False
    
    # Verificar APIs
    api_path = backend_path / "app" / "api"
    if api_path.exists():
        api_files = list(api_path.glob("*.py"))
        print(f"✅ {len(api_files)} arquivos de API encontrados")
    
    return True

def test_frontend():
    """Testa o frontend"""
    print("\n🌐 TESTANDO FRONTEND...")
    
    # Verificar se o diretório frontend existe
    frontend_path = Path("guardflow-web")
    if not frontend_path.exists():
        print("⚠️ Diretório guardflow-web não encontrado")
        return False
    
    # Verificar package.json
    package_json = frontend_path / "package.json"
    if not package_json.exists():
        print("❌ package.json não encontrado")
        return False
    
    print("✅ Estrutura frontend OK")
    
    # Verificar src
    src_path = frontend_path / "src"
    if src_path.exists():
        tsx_files = list(src_path.rglob("*.tsx"))
        print(f"✅ {len(tsx_files)} arquivos TSX encontrados")
    
    return True

def test_mobile():
    """Testa o mobile"""
    print("\n📱 TESTANDO MOBILE...")
    
    # Verificar se o diretório mobile existe
    mobile_path = Path("mobile-app")
    if not mobile_path.exists():
        print("⚠️ Diretório mobile-app não encontrado")
        return False
    
    # Verificar package.json
    package_json = mobile_path / "package.json"
    if not package_json.exists():
        print("❌ package.json não encontrado")
        return False
    
    print("✅ Estrutura mobile OK")
    
    return True

def test_structure():
    """Testa estrutura geral"""
    print("\n📋 TESTANDO ESTRUTURA GERAL...")
    
    required_files = [
        "README.md",
        "backend/requirements.txt",
        "backend/app/main.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {missing_files}")
        return False
    
    print("✅ Estrutura geral OK")
    return True

def main():
    """Função principal"""
    print("🧪 TESTE FINAL DO SISTEMA GUARDFLOW")
    print("=" * 40)
    
    # Verificar diretório atual
    current_dir = Path.cwd()
    print(f"📁 Diretório atual: {current_dir}")
    
    # Executar testes
    tests = [
        ("Estrutura", test_structure),
        ("Backend", test_backend),
        ("Frontend", test_frontend),
        ("Mobile", test_mobile)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results[test_name] = False
    
    # Resumo final
    print("\n🎯 RESUMO FINAL")
    print("=" * 20)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 SISTEMA PRONTO PARA TESTE!")
        print("✅ Todos os componentes estão presentes")
        print("✅ Estrutura está correta")
        print("✅ Arquivos principais encontrados")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Instalar dependências: pip install -r backend/requirements.txt")
        print("2. Executar backend: cd backend && uvicorn app.main_test:app --reload")
        print("3. Executar frontend: cd guardflow-web && npm start")
        print("4. Acessar: http://localhost:8000/docs")
        
    else:
        print("\n⚠️ SISTEMA PRECISA DE AJUSTES")
        print("Alguns componentes estão faltando ou com problemas")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
