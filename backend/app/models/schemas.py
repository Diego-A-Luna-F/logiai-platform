from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LogisticsItem(BaseModel):
    """Esquema para un artículo individual dentro de un manifiesto de carga."""
    sku: str = Field(..., description="Código único de producto / SKU")
    description: str = Field(..., description="Descripción del artículo")
    quantity: int = Field(..., ge=1, description="Cantidad (debe ser mayor o igual a 1)")
    status: str = Field(..., description="Estado del producto (ej: Normal, Faltante, Dañado, En Tránsito)")

class AIAnalysisReport(BaseModel):
    """Esquema que define la estructura que la IA debe generar obligatoriamente."""
    summary: str = Field(..., description="Resumen ejecutivo del manifiesto o documento analizado")
    risk_level: str = Field(..., description="Nivel de riesgo operativo detectado: Bajo, Medio o Alto")
    anomalies_detected: List[str] = Field(default_factory=list, description="Lista de irregularidades, inconsistencias o discrepancias encontradas")
    items: List[LogisticsItem] = Field(default_factory=list, description="Lista de artículos procesados del documento")

class DocumentAnalysisResponse(BaseModel):
    """Respuesta estructurada que devolverá la API tras analizar un archivo."""
    filename: str
    file_type: str
    total_lines_extracted: int
    raw_text_preview: str
    ai_analysis: Optional[AIAnalysisReport] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)

# Esquemas Historial (GET)

class AnalysisReportDB(BaseModel):
    summary: str
    risk_level: str
    anomalies: List[str]
    items_detected: List[dict]

    class Config:
        from_attributes = True  # Permite que Pydantic lea directamente los modelos de SQLAlchemy

class DocumentHistoryResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    total_lines: int
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentDetailResponse(DocumentHistoryResponse):
    analysis: Optional[AnalysisReportDB] = None