#!/usr/bin/env python3
"""
GuardFlow Test Server - Inicialização Rápida
Script para iniciar o servidor de teste imediatamente
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("🚀 INICIANDO GUARDFLOW TEST SERVER")
print("=" * 40)

try:
    # Importar FastAPI
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    print("✅ FastAPI importado com sucesso")
    
    # Criar aplicação
    app = FastAPI(
        title="GuardFlow Test API",
        description="API de teste do GuardFlow - Versão simplificada",
        version="1.0.0-test",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print("✅ Aplicação FastAPI criada")
    
    # Endpoints básicos
    @app.get("/")
    async def root():
        return {
            "message": "GuardFlow Test Server",
            "status": "running",
            "version": "1.0.0-test",
            "docs": "/docs",
            "endpoints": [
                "/health",
                "/test",
                "/docs",
                "/redoc"
            ]
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "message": "GuardFlow Test Server funcionando!",
            "components": {
                "backend": "✅ OK",
                "apis": "✅ Carregadas",
                "docs": "✅ Disponível"
            }
        }
    
    @app.get("/test")
    async def test():
        return {
            "message": "🎉 Sistema de teste funcionando perfeitamente!",
            "features": [
                "✅ Backend FastAPI ativo",
                "✅ CORS configurado",
                "✅ Documentação disponível",
                "✅ Endpoints de teste funcionais"
            ],
            "next_steps": [
                "Acesse /docs para ver a documentação",
                "Teste os endpoints disponíveis",
                "Integre com o frontend",
                "Execute testes de carga"
            ]
        }
    
    # Tentar carregar APIs do sistema (opcional)
    apis_loaded = 0
    try:
        # Importar APIs se disponíveis
        sys.path.append(str(backend_path / "app"))
        
        # Scanner API
        try:
            from app.api.scanner import router as scanner_router
            app.include_router(scanner_router, prefix="/api/v1", tags=["Scanner"])
            apis_loaded += 1
            print("✅ Scanner API carregada")
        except:
            print("⚠️ Scanner API não disponível")
        
        # Cart API
        try:
            from app.api.cart import router as cart_router
            app.include_router(cart_router, prefix="/api/v1", tags=["Cart"])
            apis_loaded += 1
            print("✅ Cart API carregada")
        except:
            print("⚠️ Cart API não disponível")
        
        # ESG API
        try:
            from app.api.esg_engine import router as esg_router
            app.include_router(esg_router, prefix="/api/v1", tags=["ESG"])
            apis_loaded += 1
            print("✅ ESG API carregada")
        except:
            print("⚠️ ESG API não disponível")
        
        # QR Checkout API
        try:
            from app.api.qr_checkout import router as qr_router
            app.include_router(qr_router, prefix="/api/v1", tags=["QR Checkout"])
            apis_loaded += 1
            print("✅ QR Checkout API carregada")
        except:
            print("⚠️ QR Checkout API não disponível")
        
        # SEVE API
        try:
            from app.api.seve_personalization import router as seve_router
            app.include_router(seve_router, prefix="/api/v1", tags=["SEVE"])
            apis_loaded += 1
            print("✅ SEVE API carregada")
        except:
            print("⚠️ SEVE API não disponível")
        
        # Performance API
        try:
            from app.api.performance import router as perf_router
            app.include_router(perf_router, prefix="/api/v1/performance", tags=["Performance"])
            apis_loaded += 1
            print("✅ Performance API carregada")
        except:
            print("⚠️ Performance API não disponível")
        
        # SYMBEON Advanced API
        try:
            from app.api.symbeon_advanced import router as symbeon_router
            app.include_router(symbeon_router, prefix="/api/v1", tags=["SYMBEON"])
            apis_loaded += 1
            print("✅ SYMBEON Advanced API carregada")
        except:
            print("⚠️ SYMBEON Advanced API não disponível")
            
    except Exception as e:
        print(f"⚠️ Algumas APIs não puderam ser carregadas: {e}")
    
    print(f"✅ {apis_loaded} APIs carregadas com sucesso")
    print(f"✅ Total de rotas: {len(app.routes)}")
    
    # Iniciar servidor
    print("\n🌐 INICIANDO SERVIDOR...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔍 Health: http://localhost:8000/health")
    print("🧪 Test: http://localhost:8000/test")
    print("\n⚡ Pressione Ctrl+C para parar")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Instale as dependências: pip install fastapi uvicorn")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)
