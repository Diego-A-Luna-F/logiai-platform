from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicializamos FastAPI
app = FastAPI(
    title="LogiAI API",
    description="API para analisis inteligente de logistica y documentos operativos",
    version="0.1.0", 
)

# Configuración de CORS (Cross-Origin Resource Sharing)
# Permite que nuestro frontend en React pueda realizar peticiones a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificaremos el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Endpoint de prueba para verificar que el servicio esté respondiendo.
    """
    return {
        "status": "online",
        "service": "LogiAI API",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de Health Check (usado por Docker, AWS y sistemas de monitoreo).
    """
    return {"status": "healthy"}