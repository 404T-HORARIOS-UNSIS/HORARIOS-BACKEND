from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List

class ExamResponse(BaseModel):
    id: int
    course: str      # Nombre de la materia
    group: str       # Grupo (ej. 106-A)
    professor: str   # Nombre del profe
    classroom: str   # Aula asignada
    date: date       # Fecha del examen
    start: time      # Hora inicio
    end: time        # Hora fin

    class Config:
        # Esto permite que Pydantic lea datos directamente de los modelos de SQLAlchemy
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True