from sqlalchemy.orm import Session
from app.core.conexion import SessionLocal


def get_db():
    """
    Dependencia que proporciona una sesión de base de datos.
    Se cierra automáticamente después de cada request.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
