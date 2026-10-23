from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class DocumentModel(Base):
    """Tabla que registra cada archivo físico subido."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_hash = Column(String(64), unique=True, index=True, nullable=False)
    total_lines = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación 1 a 1 con el reporte de análisis
    analysis = relationship("AnalysisReportModel", back_populates="document", uselist=False, cascade="all, delete-orphan")


class AnalysisReportModel(Base):
    """Tabla que guarda el diagnóstico de riesgo y los SKUs detectados por la IA."""
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, unique=True)
    summary = Column(Text, nullable=False)
    risk_level = Column(String(50), nullable=False)  # Bajo, Medio, Alto, Crítico
    anomalies = Column(JSON, nullable=False)         
    items_detected = Column(JSON, nullable=False)   
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("DocumentModel", back_populates="analysis")