from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL de conexión a PostgreSQL (Supabase)
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine principal de conexión a la base
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos ORM
Base = declarative_base()


# Dependency de FastAPI para abrir y cerrar sesiones de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()