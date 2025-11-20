# Horarios Backend API

API para gestión de exámenes y horarios.

### Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
DATABASE_URL=postgresql://user_horarios:horarios123@localhost:5433/horarios_db
```

### Instalar dependencias

Poetry:

```bash
poetry install
```

### Levantar la base de datos

```bash
docker-compose up -d
```

### Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

---

## Estructura del Proyecto

```
horarios-backend/
├── app/
│   ├── api/              # Endpoints y rutas
│   ├── core/             # Conexión y configuraciones de BD
│   ├── models/           # Modelos de la BD (tablas)
│   ├── repositories/     # Acceso a datos y operaciones CRUD
│   ├── schemas/          # Esquemas de validación (entrada/salida)
│   └── services/         # Lógica de negocio
├── .env                  # Variables de entorno
├── .gitignore
├── docker-compose.yml    # Configuración de PostgreSQL
├── main.py               # Punto de entrada de la aplicación
└── README.md
```

---

### **Flujo de una petición:**

```
Petición (crear examen)
    ↓
API (recibe petición)
    ↓
Schemas (valida formato de datos)
    ↓
Services (genera examen - lógica de negocio)
    ↓
Repositories (guarda en BD)
    ↓
Models (tabla de BD)
    ↓
Schemas (formato de respuesta)
    ↓
Respuesta
```

---

## Documentación de la API

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---