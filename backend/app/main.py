from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.documents import router as documents_router

# Importaciones para la DB
from app.db.database import engine, Base
import app.models.db_models  # Carga los modelos ORM en memoria

# Crear automáticamente tablas en la DB SQL al arrancar
Base.metadata.create_all(bind=engine)

# Inicializamos FastAPI
app = FastAPI(
    title="LogiAI API",
    description="API para análisis inteligente de logística y documentos operativos",
    version="0.1.0", 
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos rutas de documentos
app.include_router(documents_router)

@app.get("/")
async def root():
    """Endpoint de prueba para verificar que el servicio esté respondiendo."""
    return {
        "status": "online",
        "service": "LogiAI API",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint de Health Check (usado por Docker, AWS y sistemas de monitoreo)."""
    return {"status": "healthy"}