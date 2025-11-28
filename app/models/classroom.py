from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from app.core.conexion import Base


# 1. Modelo de Aula (Ya lo tenías, lo dejo por referencia)
class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # Ej: "F3", "CETI-S.O."
    capacity = Column(Integer, default=30)
    is_computer_lab = Column(Boolean, default=False) # Para saber si es sala de cómputo