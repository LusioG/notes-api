from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a la base SQLite (archivo local tasks.db)
DATABASE_URL = "sqlite:///./tasks.db"


# Engine = conexión principal a la base de datos.
# Es el "motor" que usa SQLAlchemy para hablar con la DB.
# check_same_thread=False permite usar la conexión en múltiples requests (FastAPI es async).
engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread":False}
)
SessionLocal = sessionmaker(bind=engine)

# Clase base para definir los modelos ORM (tablas).
# Todas las clases de models.py heredan de Base.
Base = declarative_base()

# Dependency de FastAPI para obtener una sesión de DB por request.
# Abre sesión → la entrega al endpoint → la cierra al terminar.
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

