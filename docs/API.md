# Documentación de la API

Guía completa y navegable con descripción de endpoints, parámetros, cuerpos, respuestas, códigos HTTP y ejemplos funcionales.

Base URL local: `http://localhost:8000`

- OpenAPI/Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Autenticación

JWT basado en `Bearer`.

### POST `/auth/register`
Registra un nuevo usuario.

- Headers:
  - `Content-Type: application/json`
- Body (JSON):
```json
{
  "username": "juan",
  "email": "juan@example.com",
  "password": "MiPasswordSegura123",
  "role": "SECRETARIA"
}
```
- Respuestas:
  - 201 Created:
```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@example.com",
  "role": "SECRETARIA",
  "is_active": true,
  "created_at": "2025-11-28T14:18:27.419Z"
}
```
  - 400 Bad Request: datos inválidos
  - 409 Conflict: usuario ya existe

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"juan","email":"juan@example.com","password":"MiPasswordSegura123","role":"SECRETARIA"}'
```

### POST `/auth/login`
Obtiene token de acceso.

- Headers:
  - `Content-Type: application/x-www-form-urlencoded`
- Body (form):
  - `username`: string
  - `password`: string
- Respuestas:
  - 200 OK:
```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```
  - 401 Unauthorized: credenciales inválidas

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan&password=MiPasswordSegura123"
```

### GET `/auth/me`
Perfil del usuario autenticado.

- Headers:
  - `Authorization: Bearer <jwt>`
- Respuestas:
  - 200 OK:
```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@example.com",
  "role": "SECRETARIA",
  "is_active": true,
  "created_at": "2025-11-28T14:18:27.419Z"
}
```
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <jwt>"
```

---

## Exámenes

Endpoints para consultar y sembrar datos de exámenes.

### GET `/examenes/exams`
Lista de exámenes programados.

- Respuestas:
  - 200 OK:
```json
[
  {
    "id": 1,
    "course": "Diseño Estructurado de Algoritmos",
    "group": "106-A",
    "professor": "Mtro. Irving Ulises Hernández Miguel",
    "classroom": "CETI-S.O.",
    "date": "2025-10-28",
    "start": "17:00:00",
    "end": "19:00:00"
  }
]
```
  - 200 OK vacío: `[]`

- Ejemplo curl:
```bash
curl http://localhost:8000/examenes/exams
```

### POST `/examenes/seed-pdf-data`
Carga datos de ejemplo del PDF (grupo 106-A). Idempotente: si ya existen, avisa.

- Headers:
  - `Authorization: Bearer <jwt>` (si el proyecto exige auth para escribir; en esta versión puede estar abierto)
- Respuestas:
  - 200 OK:
```json
{ "message": "Datos del PDF (Grupo 106-A) cargados exitosamente" }
```
  - 200 OK (ya cargados):
```json
{ "message": "Los datos ya fueron cargados previamente." }
```

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/examenes/seed-pdf-data
```

---

## Códigos HTTP

- 200 OK: Operación exitosa.
- 201 Created: Recurso creado (registro de usuario).
- 400 Bad Request: Validación de entrada fallida.
- 401 Unauthorized: Autenticación requerida o inválida.
- 403 Forbidden: Autorización insuficiente (si se aplica control de roles).
- 404 Not Found: Recurso inexistente.
- 409 Conflict: Conflicto de recursos (usuario existente).
- 500 Internal Server Error: Error inesperado del servidor.

---

## Notas de uso

- Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`.
- El backend corre por defecto en `0.0.0.0:8000` (Docker) o `localhost:8000` local.
- Para consumir desde un frontend, asegúrate de configurar CORS si el origen es distinto.

---

## Ejemplos rápidos

Registrar, loguear y consultar perfil:
```bash
# Registro
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"Pass1234","role":"SECRETARIA"}'

# Login
TOKEN=(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=Pass1234" | jq -r .access_token)

# Perfil
curl http://localhost:8000/auth/me -H "Authorization: Bearer $TOKEN"
```

Listar exámenes y sembrar datos:
```bash
curl http://localhost:8000/examenes/exams
curl -X POST http://localhost:8000/examenes/seed-pdf-data
```
