"""
GuardFlow - Simple Backend for Demo
Backend simplificado para demonstração
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Criar aplicação FastAPI
app = FastAPI(
    title="GuardFlow API",
    description="Sistema de checkout inteligente",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "GuardFlow API - Sistema de Checkout Inteligente",
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

@app.get("/api/v1/scanner/stats")
async def get_scanner_stats():
    """Estatísticas do scanner"""
    return {
        "success": True,
        "data": {
            "total_scans": 1250,
            "successful_scans": 1180,
            "success_rate": 94.4,
            "avg_scan_time_ms": 850
        }
    }

@app.get("/api/v1/esg/dashboard")
async def get_esg_dashboard():
    """Dashboard ESG"""
    return {
        "success": True,
        "data": {
            "total_score": 87,
            "total_points": 2450,
            "total_tokens": 125
        }
    }

@app.get("/api/v1/products")
async def get_products():
    """Lista de produtos"""
    return {
        "success": True,
        "data": {
            "total": 150,
            "products": [
                {"id": 1, "name": "Produto 1", "price": 10.50},
                {"id": 2, "name": "Produto 2", "price": 15.75}
            ]
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_main:app",
        host="127.0.0.1",
        port=8002,
        reload=True
    )
