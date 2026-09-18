import os
from google import genai
from google.genai import types
from app.models.schemas import AIAnalysisReport

class AIService:
    """Servicio encargado de interactuar con el modelo de IA Gemini."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno.")
        self.client = genai.Client(api_key=api_key)

    async def analyze_logistics_document(self, document_text: str) -> AIAnalysisReport:
        """
        Envía el texto del documento a Gemini para extraer los items y generar
        un reporte de riesgo/anomalías utilizando respuestas estructuradas (Pydantic).
        """
        prompt = f"""
        Actúa como un experto en auditoría logística y administración de cadenas de suministro (supply chain).
        Analiza el siguiente texto extraído de un manifiesto de carga o reporte operativo y realiza lo siguiente:
        1. Resume el contenido principal.
        2. Determina el nivel de riesgo operativo (Bajo, Medio o Alto).
        3. Identifica anomalías, datos faltantes, retrasos o discrepancias.
        4. Extrae la lista de productos o ítems identificados con su SKU, descripción, cantidad y estado.

        Texto del documento:
        \"\"\"
        {document_text}
        \"\"\"
        """

        # Invocamos la API de Gemini forzando el formato JSON según el esquema AIAnalysisReport
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIAnalysisReport,
                temperature=0.2  # Temperatura baja para respuestas más precisas y deterministas
            ),
        )

        report = AIAnalysisReport.model_validate_json(response.text)
        return report