import osimport os



content = r'''from fastapi import APIRouter, Depends, HTTPExceptioncontent = r"""from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Sessionfrom sqlalchemy.orm import Session

from datetime import date, time, timedeltafrom datetime import date, time, timedelta

from typing import Listfrom typing import List



from app.core.conexion import get_dbfrom app.core.conexion import get_db

from app.models.examen import Examfrom app.models.examen import Exam

from app.models.course import Coursefrom app.models.course import Course

from app.models.professor import Professorfrom app.models.professor import Professor

from app.models.classroom import Classroomfrom app.models.classroom import Classroom

from app.schemas.examen_schemas import ExamResponse, MessageResponsefrom app.schemas.examen_schemas import ExamResponse, MessageResponse



router = APIRouter(router = APIRouter(

    prefix="/examenes",     prefix="/examenes", 

    tags=["examenes"])    tags=["examenes"])



@router.get("/exams", response_model=List[ExamResponse])@router.get("/exams", response_model=List[ExamResponse])

def get_all_exams(db: Session = Depends(get_db)):def get_all_exams(db: Session = Depends(get_db)):

    """    """

    Retorna la lista de exámenes agendados.    Retorna la lista de exámenes agendados.

    """    """

    exams = db.query(Exam).all()    exams = db.query(Exam).all()

        

    # Mapeamos los objetos de DB al formato JSON plano que definimos en el Schema    # Mapeamos los objetos de DB al formato JSON plano que definimos en el Schema

    results = []    results = []

    for exam in exams:    for exam in exams:

        results.append({        results.append({

            "id": exam.id,            "id": exam.id,

            "course": exam.course.name,            "course": exam.course.name,

            "group": exam.course.group_name,            "group": exam.course.group_name,

            "professor": exam.course.professor.full_name,            "professor": exam.course.professor.full_name,

            "classroom": exam.classroom.name,            "classroom": exam.classroom.name,

            "date": exam.exam_date,            "date": exam.exam_date,

            "start": exam.start_time,            "start": exam.start_time,

            "end": exam.end_time            "end": exam.end_time

        })        })

        

    return results    return results



@router.post("/seed-pdf-data", response_model=MessageResponse)@router.post("/seed-pdf-data", response_model=MessageResponse)

def seed_data_from_pdf(db: Session = Depends(get_db)):def seed_data_from_pdf(db: Session = Depends(get_db)):

    """    """

    Endpoint temporal para cargar datos reales del PDF (Informática 106-A)    Endpoint temporal para cargar datos reales del PDF (Informática 106-A)

    """    """

    # 1. Verificar si ya existen datos para no duplicar    # 1. Verificar si ya existen datos para no duplicar

    if db.query(Course).filter(Course.group_name == "106-A").first():    if db.query(Course).filter(Course.group_name == "106-A").first():

        return {"message": "Los datos ya fueron cargados previamente."}        return {"message": "Los datos ya fueron cargados previamente."}



    # 2. Crear Profesores (Datos del PDF)    # 2. Crear Profesores (Datos del PDF)

    prof_irving = Professor(full_name="Mtro. Irving Ulises Hernández Miguel")    prof_irving = Professor(full_name="Mtro. Irving Ulises Hernández Miguel")

    prof_fabiola = Professor(full_name="M.I.S. Fabiola Crespo Barrios")    prof_fabiola = Professor(full_name="M.I.S. Fabiola Crespo Barrios")

    prof_oswaldo = Professor(full_name="M.I.T.I. Oswaldo Rey Ávila Barrón")    prof_oswaldo = Professor(full_name="M.I.T.I. Oswaldo Rey Ávila Barrón")

        

    db.add_all([prof_irving, prof_fabiola, prof_oswaldo])    db.add_all([prof_irving, prof_fabiola, prof_oswaldo])

    db.commit()    db.commit()



    # 3. Crear Aulas    # 3. Crear Aulas

    classroom_ceti = Classroom(name="CETI-S.O.", capacity=30, is_computer_lab=True)    classroom_ceti = Classroom(name="CETI-S.O.", capacity=30, is_computer_lab=True)

    classroom_e2 = Classroom(name="E2", capacity=40)    classroom_e2 = Classroom(name="E2", capacity=40)

    classroom_d4 = Classroom(name="D4", capacity=40)    classroom_d4 = Classroom(name="D4", capacity=40)

        

    db.add_all([classroom_ceti, classroom_e2, classroom_d4])    db.add_all([classroom_ceti, classroom_e2, classroom_d4])

    db.commit()    db.commit()



    # 4. Crear Materias y asignar Exámenes    # 4. Crear Materias y asignar Exámenes

    # Datos extraídos de: LICENCIATURA EN INFORMÁTICA.pdf (Página 2)    # Datos extraídos de: LICENCIATURA EN INFORMÁTICA.pdf (Página 2)

        

    # Materia 1: Diseño Estructurado    # Materia 1: Diseño Estructurado

    course1 = Course(name="Diseño Estructurado de Algoritmos", group_name="106-A", professor_id=prof_irving.id)    course1 = Course(name="Diseño Estructurado de Algoritmos", group_name="106-A", professor_id=prof_irving.id)

    db.add(course1)    db.add(course1)

    db.commit()    db.commit()

        

    exam1 = Exam(    exam1 = Exam(

        course_id=course1.id,        course_id=course1.id,

        classroom_id=classroom_ceti.id,        classroom_id=classroom_ceti.id,

        exam_date=date(2025, 10, 28), # 28/10/2025        exam_date=date(2025, 10, 28), # 28/10/2025

        start_time=time(17, 0),       # 17:00        start_time=time(17, 0),       # 17:00

        end_time=time(19, 0)          # Asumimos 2 horas        end_time=time(19, 0)          # Asumimos 2 horas

    )    )



    # Materia 2: Administración    # Materia 2: Administración

    course2 = Course(name="Administración", group_name="106-A", professor_id=prof_fabiola.id)    course2 = Course(name="Administración", group_name="106-A", professor_id=prof_fabiola.id)

    db.add(course2)    db.add(course2)

    db.commit()    db.commit()



    exam2 = Exam(    exam2 = Exam(

        course_id=course2.id,        course_id=course2.id,

        classroom_id=classroom_e2.id,        classroom_id=classroom_e2.id,

        exam_date=date(2025, 10, 29), # 29/10/2025        exam_date=date(2025, 10, 29), # 29/10/2025

        start_time=time(13, 0),       # 13:00        start_time=time(13, 0),       # 13:00

        end_time=time(15, 0)        end_time=time(15, 0)

    )    )



    # Materia 3: Historia del Pensamiento Filosófico    # Materia 3: Historia del Pensamiento Filosófico

    course3 = Course(name="Historia del Pensamiento Filosófico", group_name="106-A", professor_id=prof_oswaldo.id)    course3 = Course(name="Historia del Pensamiento Filosófico", group_name="106-A", professor_id=prof_oswaldo.id)

    db.add(course3)    db.add(course3)

    db.commit()    db.commit()



    exam3 = Exam(    exam3 = Exam(

        course_id=course3.id,        course_id=course3.id,

        classroom_id=classroom_d4.id,        classroom_id=classroom_d4.id,

        exam_date=date(2025, 10, 30), # 30/10/2025        exam_date=date(2025, 10, 30), # 30/10/2025

        start_time=time(16, 0),       # 16:00        start_time=time(16, 0),       # 16:00

        end_time=time(18, 0)        end_time=time(18, 0)

    )    )



    db.add_all([exam1, exam2, exam3])    db.add_all([exam1, exam2, exam3])

    db.commit()    db.commit()



    return {"message": "Datos del PDF (Grupo 106-A) cargados exitosamente"}    return {"message": "Datos del PDF (Grupo 106-A) cargados exitosamente"}

'''"""



with open('/home/jlopez/Documentos/horarios-backend/app/api/examen_routes.py', 'w') as f:with open('/home/jlopez/Documentos/horarios-backend/app/api/examen_routes.py', 'w') as f:

    f.write(content)    f.write(content)

