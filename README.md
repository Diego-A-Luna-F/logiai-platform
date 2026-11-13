# LogiAI Platform — Intelligent Logistics Document Analysis



Plataforma full-stack para la ingesta, respaldo en la nube, extracción estructurada y análisis de riesgos en documentos logísticos (manifiestos de carga, reportes de incidencias y pedimentos en formatos **PDF** y **CSV**) impulsada por **Google Gemini AI** y **AWS S3**.



---



## Arquitectura y Flujo de Datos



El sistema implementa una arquitectura orientada a **idempotencia, resiliencia y optimización de costos** en la nube:



1. **Validación Previa (Gatekeeper):** El backend sanitiza el documento y valida su formato (`.pdf`, `.csv`) y legibilidad antes de consumir recursos externos.

2. **Deduplicación por Hash (SHA-256):** Se genera una huella digital única del contenido extraído. Si el documento ya fue procesado anteriormente (*Cache Hit* en **Redis** o registro existente en **SQL**), se retorna el análisis al instante evitando subidas duplicadas a S3 y llamadas innecesarias a la API de IA.

3. **Almacenamiento Inmutable en AWS S3:** Los documentos nuevos y válidos se respaldan automáticamente en un bucket de **Amazon S3** organizados cronológicamente (`manifests/YYYYMMDD/<uuid>_<filename>`) mediante `boto3`.

4. **Análisis Estructurado con Gemini AI:** Extracción de resumen ejecutivo, nivel de riesgo (`Bajo`, `Medio`, `Alto`), anomalías detectadas e ítems logísticos en formato JSON estricto.

5. **Persistencia y Auditoría:** Almacenamiento relacional mediante **SQLAlchemy** para consulta histórica, búsqueda por nombre y filtrado por nivel de riesgo.



---



## Stack Tecnológico



* **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic, SQLAlchemy.

* **Inteligencia Artificial:** Google GenAI SDK (`google-genai`).

* **Cloud & Storage:** AWS S3 (`boto3`).

* **Caché & Rendimiento:** Redis 7 (Alpine).

* **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Producción).

* **Frontend:** React, Vite, Tailwind CSS.

* **Infraestructura:** Docker & Docker Compose.



---



## Estructura del Proyecto



```text

logiai-platform/

├── backend/

│   ├── app/

│   │   ├── api/            # Endpoints REST (documents.py)

│   │   ├── db/             # Configuración y sesión de base de datos

│   │   ├── models/         # Modelos SQLAlchemy y esquemas Pydantic

│   │   └── services/       # Lógica de negocio (AI, S3, Redis, Document Processor)

│   ├── Dockerfile          # Imagen Python 3.12-slim

│   └── requirements.txt    # Dependencias ancladas

├── frontend/

│   ├── src/

│   │   └── components/     # FileUpload, AnalysisViewer, HistoryTable, Navbar

│   ├── Dockerfile          # Imagen Node 20-alpine

│   └── package.json

├── docker-compose.yml      # Orquestación de servicios (api, redis, frontend)

├── .env.example            # Plantilla de variables de entorno

└── README.md

```



---



## Instalación y Despliegue Local con Docker



### 1. Clonar el repositorio

```bash

git clone https://github.com/tu-usuario/logiai-platform.git

cd logiai-platform

```



### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basado en `.env.example` y completa tus credenciales:



```env

# Google Gemini API

GEMINI_API_KEY=tu_api_key_de_gemini



# Redis

REDIS_HOST=redis

REDIS_PORT=6379



# Base de Datos

DATABASE_URL=sqlite:///./logiai.db



# AWS S3 Configuration

AWS_ACCESS_KEY_ID=tu_access_key_id

AWS_SECRET_ACCESS_KEY=tu_secret_access_key

AWS_REGION=us-east-2

AWS_S3_BUCKET_NAME=logiai-manifests-diego-2026

```



### 3. Construir y levantar los contenedores

```bash

docker-compose up --build -d

```



### 4. Accesos a la Plataforma

* **Interfaz Web (Frontend):** `http://localhost:5173`

* **Documentación Interactiva API (Swagger UI):** `http://localhost:8000/docs`



---



## Endpoints Principales



| Método | Ruta | Descripción |

| :--- | :--- | :--- |

| `POST` | `/api/v1/documents/upload` | Sube un manifiesto (`.pdf` o `.csv`), valida, respalda en S3 y analiza con IA. |

| `GET` | `/api/v1/documents/` | Lista el historial de documentos con filtros opcionales (`search`, `risk_level`, `limit`). |

| `GET` | `/api/v1/documents/{id}` | Obtiene el detalle completo y reporte de anomalías de un documento específico. |



---



## Autor



**Diego Armando Luna Flores** — Mechatronics & Full-Stack Software Engineer
