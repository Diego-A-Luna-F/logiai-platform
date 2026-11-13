import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import uuid

class S3Service:
    def __init__(self):
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region_name = os.getenv("AWS_REGION", "us-east-2")
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

        # Inicializamos el cliente oficial de S3
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region_name
        )

    def upload_file(self, file_bytes: bytes, original_filename: str, content_type: str) -> str:
        """
        Sube los bytes de un archivo a S3 y devuelve la clave (ruta interna) del objeto.
        """
        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET_NAME no está configurado en el archivo .env")

        # Nombre único con fecha y UUID para evitar sobrescribir archivos con el mismo nombre
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        unique_id = uuid.uuid4().hex[:8]
        safe_filename = original_filename.replace(" ", "_")
        s3_key = f"manifests/{timestamp}/{unique_id}_{safe_filename}"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_bytes,
                ContentType=content_type
            )
            return s3_key
        except ClientError as e:
            print(f"Error subiendo archivo a S3: {e}")
            raise Exception(f"Fallo al almacenar el documento en AWS S3: {str(e)}")

# Instancia para importar endpoints
s3_service = S3Service()