"""
GuardFlow API - Versão Simplificada para Teste
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Criar aplicação FastAPI
app = FastAPI(
    title="GuardFlow API",
    description="GuardFlow - Agiliza aí suas compras! API Backend",
    version="1.0.0",
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

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "GuardFlow API - Agiliza aí! 🚀",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "GuardFlow agilizando perfeitamente! ✅",
        "version": "1.0.0",
        "timestamp": "2024-10-14T21:40:00Z"
    }

@app.get("/agiliza")
async def agiliza():
    """Endpoint de teste"""
    return {
        "message": "Agilizou! GuardFlow funcionando! ⚡",
        "status": "success"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

