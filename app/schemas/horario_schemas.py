from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List

class RawScheduleInput(BaseModel):
    idprofesor: str
    nombreCompleto: str
    materia: str
    nombreGrupo: str
    nombreAula: str
    dia: int # 1=Lunes, 2=Martes, ..., 7=Domingo
    hora: int # Hora en formato 24h, ej. 13=1pm

    class Config:
        extra = "ignore"