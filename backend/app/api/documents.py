import hashlib
from fastapi import APIRouter, UploadFile, File, HTTPException, Response, status
from app.models.schemas import DocumentAnalysisResponse, AIAnalysisReport
from app.services.document_processor import DocumentProcessorService
from app.services.ai_service import AIService
from app.services.cache_service import CacheService

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documentos Logísticos"]
)

@router.post(
    "/upload",
    response_model=DocumentAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Subir y analizar manifiesto o reporte de logística con IA y Caché Redis"
)
async def upload_document(response: Response, file: UploadFile = File(...)):
    # Desactivar encabezados de caché HTTP en el cliente web
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"

    # Ahorro de tokens
    extracted_data = await DocumentProcessorService.process_file(file)
    clean_text = extracted_data.get("full_text", "")

    # Genera clave (Hash SHA-256) 
    text_hash = hashlib.sha256(clean_text.encode('utf-8')).hexdigest()
    cache_key = f"doc_analysis:{text_hash}"

    cache_service = CacheService()

    # Consulta si el análisis de este texto ya existe en Redis (Cache Hit)
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

    # Si NO está en caché (Cache Miss), consulta al modelo de Gemini AI
    try:
        print("--- [GEMINI] NO ESTÁ EN CACHÉ. PROCESANDO CON IA ---")
        ai_service = AIService()
        ai_analysis = await ai_service.analyze_logistics_document(clean_text)

        # Guarda el resultado en Redis por 1 hora (3600 segundos)
        cache_service.set(cache_key, ai_analysis.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error durante el procesamiento con Inteligencia Artificial: {str(e)}"
        )

    # Respuesta consolidada
    return DocumentAnalysisResponse(
        filename=extracted_data["filename"],
        file_type=extracted_data["file_type"],
        total_lines_extracted=extracted_data["total_lines_extracted"],
        raw_text_preview=extracted_data["raw_text_preview"],
        ai_analysis=ai_analysis
    )