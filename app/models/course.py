from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date, Time
from app.core.conexion import Base
from sqlalchemy.orm import relationship

# 3. Modelo de Materia (EL NÚCLEO)
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos Básicos
    name = Column(String, index=True, nullable=False)       # Ej: "Cálculo I"
    group_name = Column(String, index=True, nullable=False) # Ej: "106-A"
    semester = Column(Integer, nullable=True)               # Ej: 1, 3, 5 (Opcional, útil para filtrar)
    
    # Relaciones (Foreign Keys)
    professor_id = Column(Integer, ForeignKey("professors.id"))
    
    # CLAVE PARA TU REQUERIMIENTO:
    # Si "Matemáticas 104A" y "Matemáticas 104B" deben presentar juntas,
    # ambas deben tener el mismo número aquí (ej: 100).
    # El algoritmo buscará materias con el mismo cluster_id para agendarlas igual.
    cluster_id = Column(Integer, nullable=True, index=True)

    # Definición de Relaciones para SQLAlchemy
    professor = relationship("Professor", backref="courses")
    
    # Una materia tiene MUCHOS horarios de clase (Lunes 9am, Miercoles 11am...)
    # cascade="all, delete-orphan" significa que si borras la materia, se borran sus horarios.
    regular_schedules = relationship("RegularSchedule", back_populates="course", cascade="all, delete-orphan")
    
    # Una materia tiene UN solo examen final/parcial agendado
    exam = relationship("Exam", uselist=False, back_populates="course")


# 4. Horarios Habituales (Para la preferencia de horario)
class RegularSchedule(Base):
    __tablename__ = "regular_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    day_of_week = Column(Integer) # 0=Lunes, 1=Martes... 6=Domingo
    start_time = Column(Time)     # Ej: 09:00:00
    end_time = Column(Time)       # Ej: 10:00:00
    
    # Opcional: Si quieres recordar en qué aula toman clase normalmente
    # classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True) 
    
    course = relationship("Course", back_populates="regular_schedules")