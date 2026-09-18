from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import pandas as pd
import io

class DocumentProcessorService:
    """Servicio encargado del parseo y extracción de texto de archivos PDF/CSV."""

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
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        return {
            "filename": filename,
            "file_type": "pdf",
            "total_lines_extracted": len(lines),
            "full_text": text,
            "raw_text_preview": text[:300] if text else "Sin texto legible",
            "items_detected": []  # En el siguiente paso la IA poblará estos items
        }

    @staticmethod
    def _extract_from_csv(content: bytes, filename: str) -> dict:
        csv_file = io.BytesIO(content)
        df = pd.read_csv(csv_file)
        full_csv_text = df.to_string()

        return {
            "filename": filename,
            "file_type": "csv",
            "total_lines_extracted": len(df),
            "full_text": full_csv_text,
            "raw_text_preview": df.head(5).to_string(),
            "items_detected": []
        }