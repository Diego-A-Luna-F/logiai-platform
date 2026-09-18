from fastapi import APIRouter, UploadFile, File, status, HTTPException, Response
from app.models.schemas import DocumentAnalysisResponse
from app.services.document_processor import DocumentProcessorService
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documentos Logísticos"]
)

@router.post(
    "/upload",
    response_model=DocumentAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Subir y analizar manifiesto o reporte de logística con IA"
)
async def upload_document(file: UploadFile = File(...)):
    """
    Recibe un archivo **PDF** o **CSV**, extrae su texto y lo envía a **Gemini AI**
    para realizar un análisis operativo, detección de anomalías y extracción estructurada de SKUs.
    """

    # Extracción física de datos
    extracted_data = await DocumentProcessorService.process_file(file)
    full_text = extracted_data.get("full_text", "")

    # Análisis con Gemini AI
    try:
        print("--- ENVIANDO TEXTO A GEMINI ---")
        ai_service = AIService()
        ai_analysis = await ai_service.analyze_logistics_document(full_text)
        print("--- RESPUESTA RECIBIDA DE GEMINI ---", ai_analysis)
    except Exception as e:
        print(f"--- ERROR EN GEMINI: {str(e)} ---")
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