import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener URL de la base de datos desde el entorno o usar SQLite por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./logiai.db")

# Si la base de datos es SQLite, pasamos check_same_thread a través de connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Se pasa connect_args correctamente como argumento con nombre
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Inyecta una sesión de base de datos en los endpoints de FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()