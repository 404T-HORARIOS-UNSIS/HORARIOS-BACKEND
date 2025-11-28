from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.core.conexion import Base

# 2. Modelo de Profesor
class Professor(Base):
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    # ID externo por si sincronizas con otro sistema de la universidad
    external_id = Column(String, unique=True, nullable=True) 