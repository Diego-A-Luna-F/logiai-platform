import hashlib
from fastapi import APIRouter, UploadFile, File, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models.schemas import DocumentAnalysisResponse, AIAnalysisReport, DocumentHistoryResponse, DocumentDetailResponse
from app.models.db_models import DocumentModel, AnalysisReportModel
from app.services.document_processor import DocumentProcessorService
from app.services.ai_service import AIService
from app.services.cache_service import CacheService
from app.db.database import get_db

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documentos Logísticos"]
)

@router.post(
    "/upload",
    response_model=DocumentAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Subir y analizar manifiesto o reporte con IA, Caché Redis y Persistencia SQL"
)
async def upload_document(
    response: Response, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"

    # Ahorro de tokens
    extracted_data = await DocumentProcessorService.process_file(file)
    clean_text = extracted_data.get("full_text", "")

    # Generar Hash SHA-256 único del contenido
    text_hash = hashlib.sha256(clean_text.encode('utf-8')).hexdigest()
    cache_key = f"doc_analysis:{text_hash}"

    cache_service = CacheService()

    # Consultar si existe en Redis (Cache Hit)
    cached_analysis = cache_service.get(cache_key)
    if cached_analysis:
        print("--- [REDIS] RETORNANDO RESULTADO DESDE CACHÉ (CACHE HIT) ---")
        return DocumentAnalysisResponse(
            filename=extracted_data["filename"],
            file_type=extracted_data["file_type"],
            total_lines_extracted=extracted_data["total_lines_extracted"],
            raw_text_preview=extracted_data["raw_text_preview"],
            ai_analysis=AIAnalysisReport(**cached_analysis)
        )

    # Si NO está en caché (Cache Miss), procesar con Gemini AI
    try:
        print("--- [GEMINI] NO ESTÁ EN CACHÉ. PROCESANDO CON IA ---")
        ai_service = AIService()
        ai_analysis = await ai_service.analyze_logistics_document(clean_text)

        # Guardar respuesta en Redis (Expiración de 1 hora)
        cache_service.set(cache_key, ai_analysis.model_dump())

        # Guardar permanentemente en la Base de Datos SQL
        existing_doc = db.query(DocumentModel).filter(DocumentModel.file_hash == text_hash).first()
        
        if not existing_doc:
            # Crear registro del Documento
            new_doc = DocumentModel(
                filename=extracted_data["filename"],
                file_type=extracted_data["file_type"],
                file_hash=text_hash,
                total_lines=extracted_data["total_lines_extracted"]
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)

            # Crear registro del Reporte asociado
            new_report = AnalysisReportModel(
                document_id=new_doc.id,
                summary=ai_analysis.summary,
                risk_level=ai_analysis.risk_level,
                anomalies=ai_analysis.anomalies_detected,
                items_detected=[i.model_dump() for i in ai_analysis.items]
            )
            db.add(new_report)
            db.commit()
            print(f"--- [DATABASE] REGISTRO GUARDADO EN DB CON ID: {new_doc.id} ---")

    except Exception as e:
        db.rollback()  # Revierte la transacción en la base de datos si ocurre un error
        raise HTTPException(
            status_code=500,
            detail=f"Error durante el procesamiento o almacenamiento: {str(e)}"
        )

    return DocumentAnalysisResponse(
        filename=extracted_data["filename"],
        file_type=extracted_data["file_type"],
        total_lines_extracted=extracted_data["total_lines_extracted"],
        raw_text_preview=extracted_data["raw_text_preview"],
        ai_analysis=ai_analysis
    )

@router.get(
    "/", 
    response_model=List[DocumentHistoryResponse],
    summary="Listar el historial de documentos analizados"
)
async def get_documents_history(limit: int = 10, db: Session = Depends(get_db)):
    """Devuelve los últimos manifiestos procesados ordenados por los más recientes."""
    docs = db.query(DocumentModel).order_by(DocumentModel.created_at.desc()).limit(limit).all()
    return docs


@router.get(
    "/{document_id}", 
    response_model=DocumentDetailResponse,
    summary="Obtener el detalle de un documento y su análisis de IA"
)
async def get_document_detail(document_id: int, db: Session = Depends(get_db)):
    """Devuelve la información completa de un documento usando su ID."""
    # joinedload ejecuta un JOIN SQL automático para traer el análisis asociado en 1 sola consulta
    doc = db.query(DocumentModel).options(joinedload(DocumentModel.analysis)).filter(DocumentModel.id == document_id).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado en el historial")
        
    return doc