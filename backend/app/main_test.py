"""
GuardFlow Backend - Versão de Teste Simplificada
Versão sem dependências externas complexas para testes rápidos
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guardflow")

# Criar aplicação FastAPI
app = FastAPI(
    title="GuardFlow API - Test Version",
    description="API do GuardFlow para testes",
    version="1.0.0-test",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar e incluir routers básicos (sem dependências externas)
try:
    from app.api.scanner import router as scanner_router
    app.include_router(scanner_router, prefix="/api/v1", tags=["Scanner"])
    logger.info("✅ Scanner API carregada")
except Exception as e:
    logger.warning(f"⚠️ Scanner API não carregada: {e}")

try:
    from app.api.cart import router as cart_router
    app.include_router(cart_router, prefix="/api/v1", tags=["Carrinho"])
    logger.info("✅ Cart API carregada")
except Exception as e:
    logger.warning(f"⚠️ Cart API não carregada: {e}")

try:
    from app.api.esg_engine import router as esg_router
    app.include_router(esg_router, prefix="/api/v1", tags=["ESG"])
    logger.info("✅ ESG API carregada")
except Exception as e:
    logger.warning(f"⚠️ ESG API não carregada: {e}")

try:
    from app.api.qr_checkout import router as qr_checkout_router
    app.include_router(qr_checkout_router, prefix="/api/v1", tags=["QR Checkout"])
    logger.info("✅ QR Checkout API carregada")
except Exception as e:
    logger.warning(f"⚠️ QR Checkout API não carregada: {e}")

try:
    from app.api.seve_personalization import router as seve_router
    app.include_router(seve_router, prefix="/api/v1", tags=["SEVE Personalization"])
    logger.info("✅ SEVE API carregada")
except Exception as e:
    logger.warning(f"⚠️ SEVE API não carregada: {e}")

try:
    from app.api.symbeon_advanced import router as symbeon_advanced_router
    app.include_router(symbeon_advanced_router, prefix="/api/v1", tags=["SYMBEON Advanced"])
    logger.info("✅ SYMBEON Advanced API carregada")
except Exception as e:
    logger.warning(f"⚠️ SYMBEON Advanced API não carregada: {e}")

try:
    from app.api.performance import router as performance_router
    app.include_router(performance_router, prefix="/api/v1/performance", tags=["Performance"])
    logger.info("✅ Performance API carregada")
except Exception as e:
    logger.warning(f"⚠️ Performance API não carregada: {e}")

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "GuardFlow API - Versão de Teste",
        "version": "1.0.0-test",
        "status": "running",
        "docs": "/docs",
        "routes_loaded": len(app.routes)
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "version": "1.0.0-test",
        "apis_loaded": len([route for route in app.routes if route.path.startswith("/api")]),
        "total_routes": len(app.routes)
    }

@app.get("/test")
async def test_endpoint():
    """Endpoint de teste"""
    apis_status = {}
    
    # Verificar quais APIs estão carregadas
    for route in app.routes:
        if route.path.startswith("/api/v1"):
            tag = route.tags[0] if route.tags else "Unknown"
            if tag not in apis_status:
                apis_status[tag] = 0
            apis_status[tag] += 1
    
    return {
        "message": "Sistema de teste funcionando",
        "apis_loaded": apis_status,
        "total_api_routes": sum(apis_status.values()),
        "system_status": "✅ OK"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Iniciando GuardFlow Test Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
