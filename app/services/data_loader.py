import json
import os
from datetime import time
from sqlalchemy.orm import Session
from app.models import course, professor, classroom, regular_schedule
from app.models.course import Course
from app.schemas.horario_schemas import RawScheduleInput


class DataLoaderService:
    def __init__(self, db: Session):
        self.db = db

    def load_from_university_jso(self, filename: str= "706.json"):
        file_path = os.path.join("app", "data", filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        records_processed = 0

        for item in raw_data:
            # 1. Validar datos
            try:
                data = RawScheduleInput(**item)
            except Exception as e:
                print(f"Error al parsear el registro: {e}")
                continue
            # 2. Gestionar Profesor (buscar por id externo o Nombre)
            prof = self.db.query(professor).filter(professor.external_id == data.idprofesor).first()
            if not prof:
                prof = professor(
                    full_name = data.nombreCompleto.strip(),
                    external_id = data.idprofesor
                )
                self.db.add(prof)
                self.db.commit()
                self.db.refresh(prof)

            # 3. Gestionar  aula
            classroom = self.db.query(classroom).filter(classroom.name == data.nombreAula).first()
            if not classroom:
                classroom = classroom(name = data.nombreAula)
                self.db.add(classroom)
                self.db.commit()
                self.db.refresh(classroom)

            # 4. Gestionar materia
            course = self.db.query(Course).filter(
                Course.name == data.materia,
                Course.group_name == data.nombreGrupo
            ).first()

            if not course:
                course = course (
                    name = data.materia,
                    group_name = data.nombreGrupo,
                    professor_id = prof.id
                )
                self.db.add(course)
                self.db.commit()
                self.db.refresh(course)

            # 5. Gestionar Horario regular
            day_python = data.dia - 1

            start_t = time(data.hora, 0)
            end_t = time(data.hora + 1, 0)

            # evitar duplicados
            existing_schedule = self.db.query(regular_schedule).filter(
                regular_schedule.course_id == course.id,
                regular_schedule.day_of_week == day_python,
                regular_schedule.start_time == start_t,
            ).first()

            if not existing_schedule:
                schedule = regular_schedule(
                    course_id = course.id,
                    day_of_week = day_python,
                    start_time = start_t,
                    end_time = end_t,
                )
                self.db.add(schedule)
                records_processed += 1
        self.db.commit()
        return { "status": "success", "records_processed": records_processed }

