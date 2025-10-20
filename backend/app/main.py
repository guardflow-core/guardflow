"""
GuardFlow - Main Application
Sistema de tokenização ESG e monetização governamental
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from contextlib import asynccontextmanager

# Importar APIs
from app.api.monetization import router as monetization_router
from app.api.government_monetization import router as government_router
from app.api.ecosystem_saas import router as ecosystem_router
from app.api.esg_dashboard import router as esg_dashboard_router
from app.api.esg_gamification import router as esg_gamification_router
from app.api.agility_tax import router as agility_tax_router
from app.api.qr_checkout import router as qr_checkout_router
from app.api.seve_personalization import router as seve_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guardflow")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando GuardFlow...")
    yield
    logger.info("🛑 Encerrando GuardFlow...")

# Criar aplicação FastAPI
app = FastAPI(
    title="GuardFlow API",
    description="Sistema de tokenização ESG e monetização governamental",
    version="0.1.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(monetization_router, prefix="/api/v1", tags=["Monetização"])
app.include_router(government_router, prefix="/api/v1", tags=["Monetização Governamental"])
app.include_router(ecosystem_router, prefix="/api/v1", tags=["Ecossistema"])
app.include_router(esg_dashboard_router, prefix="/api/v1", tags=["Dashboard ESG"])
app.include_router(esg_gamification_router, prefix="/api/v1", tags=["Gamificação ESG"])
app.include_router(agility_tax_router, prefix="/api/v1", tags=["Agility Tax"])
app.include_router(qr_checkout_router, prefix="/api/v1", tags=["QR Checkout"])
app.include_router(seve_router, prefix="/api/v1", tags=["SEVE Personalization"])

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "GuardFlow API - Sistema de Tokenização ESG",
        "version": "0.1.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "service": "GuardFlow API",
        "version": "0.1.0"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler para exceções gerais"""
    logger.error(f"❌ Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "status_code": 500
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
