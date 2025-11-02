from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GuardFlow API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GuardFlow API funcionando!", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API funcionando"}

@app.get("/api/v1/scanner/health")
async def scanner_health():
    return {"status": "healthy", "service": "scanner"}

@app.get("/api/v1/esg/health")
async def esg_health():
    return {"status": "healthy", "service": "esg"}

@app.get("/api/v1/payment/health")
async def payment_health():
    return {"status": "healthy", "service": "payment"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


