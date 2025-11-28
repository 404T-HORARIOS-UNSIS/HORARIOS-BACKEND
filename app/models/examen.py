from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.core.conexion import Base


# 5. El Examen Generado (El Resultado)
class Exam(Base):
    __tablename__ = "examens"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relaciones
    course_id = Column(Integer, ForeignKey("courses.id"), unique=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    
    # Datos del Examen
    exam_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    
    course = relationship("Course", back_populates="exam")
    classroom = relationship("Classroom")