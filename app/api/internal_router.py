from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.conexion import get_db
from app.services.data_loader import DataLoaderService
router = APIRouter(prefix="/internal", tags=["internal"])

@router.post("/load-university-json")
def load_university_data(db: Session = Depends(get_db)):
    """Carga datos de horarios desde un archivo JSON proporcionado por la universidad"""
    data_loader = DataLoaderService(db)
    try:
        records = data_loader.load_from_university_jso()
        return {"message": f"{records} registros cargados exitosamente"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar datos: {str(e)}")cfv