from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import pandas as pd
import re
import io

class DocumentProcessorService:
    """Servicio encargado del parseo, extracción y sanitización de archivos PDF/CSV."""

    @staticmethod
    def _clean_text(raw_text: str) -> str:
        """
        Limpia y comprime el texto para minimizar el consumo de tokens en la IA.
        - Elimina múltiples saltos de línea y espacios redundantes.
        - Remueve caracteres de control no imprimibles.
        """
        if not raw_text:
            return ""

        cleaned = re.sub(r'\n+', '\n', raw_text)
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
        
        return "\n".join(lines)

    @staticmethod
    async def process_file(file: UploadFile) -> dict:
        filename = file.filename.lower()
        content = await file.read()

        if filename.endswith(".pdf"):
            return DocumentProcessorService._extract_from_pdf(content, file.filename)
        elif filename.endswith(".csv"):
            return DocumentProcessorService._extract_from_csv(content, file.filename)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Formato no soportado. Por favor sube un archivo .pdf o .csv"
            )

    @staticmethod
    def _extract_from_pdf(content: bytes, filename: str) -> dict:
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        raw_text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                raw_text += extracted + "\n"

        cleaned_text = DocumentProcessorService._clean_text(raw_text)
        lines = cleaned_text.split("\n") if cleaned_text else []

        return {
            "filename": filename,
            "file_type": "pdf",
            "total_lines_extracted": len(lines),
            "full_text": cleaned_text,
            "raw_text_preview": cleaned_text[:300] if cleaned_text else "Sin texto legible"
        }

    @staticmethod
    def _extract_from_csv(content: bytes, filename: str) -> dict:
        csv_file = io.BytesIO(content)
        df = pd.read_csv(csv_file)
        
        clean_csv_text = df.to_csv(index=False)

        return {
            "filename": filename,
            "file_type": "csv",
            "total_lines_extracted": len(df),
            "full_text": clean_csv_text,
            "raw_text_preview": df.head(5).to_string()
        }