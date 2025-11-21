# Consuming the Horarios API

Esta guía explica cómo consumir la API de Horarios desde el frontend. Incluye endpoints clave, ejemplos (curl, fetch, axios), formato de autenticación y recomendaciones para manejo de tokens.

Base URL (desarrollo)
- http://localhost:8000

Documentación interactiva
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Variables de entorno para el front
- Archivo sugerido: `.env.example` (en la raíz del repositorio)
- Variables importantes:
  - VITE_API_URL=http://localhost:8000  # o REACT_APP_API_URL según tu stack

- La API usa JWT (Bearer token).
- Pasos:
  1. Registrar usuario (si aplica): `POST /auth/register` (JSON)
  2. Hacer login: `POST /auth/login` (form-urlencoded) — devuelve `access_token`.
  3. Incluir en requests protegidos: header `Authorization: Bearer <ACCESS_TOKEN>`.
  
  Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`.

- La API usa JWT (Bearer token).
- Pasos:
  1. Registrar usuario (si aplica): `POST /auth/register` (JSON)
  2. Hacer login: `POST /auth/login` (form-urlencoded) — devuelve `access_token`.
  3. Incluir en requests protegidos: header `Authorization: Bearer <ACCESS_TOKEN>`.

Endpoints clave (resumen)
- POST /auth/register — registrar usuario
  - Body JSON (ejemplo):
    ```json
    { "username": "juan", "email": "juan@example.com", "password": "mipass123", "role": "SECRETARIA" }
    ```
  - Nota: el campo `role` sólo admite los valores: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`.
  - Respuesta 201: `UserRead` (id, username, email, role, is_active)

- POST /auth/login — obtener token
  - Form (application/x-www-form-urlencoded): `username`, `password` (OAuth2 standard)
  - Respuesta 200:
    ```json
    { "access_token": "<JWT>", "token_type": "bearer" }
    ```

- GET /auth/me — ver usuario actual
  - Header: `Authorization: Bearer <TOKEN>`
  - Respuesta: `UserRead` (sin contraseña)

Ejemplos prácticos

- cURL: registrar
```bash
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"juan","email":"juan@example.com","password":"mipass123","role":"user"}'
```

- cURL: login (form)
```bash
curl -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=juan&password=mipass123'
```

- cURL: endpoint protegido
```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://localhost:8000/auth/me
```

- fetch (login + usar token)
```javascript
const form = new URLSearchParams();
form.append('username', 'juan');
form.append('password', 'mipass123');

const loginRes = await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
  method: 'POST',
  body: form,
});
const { access_token } = await loginRes.json();

const meRes = await fetch(`${import.meta.env.VITE_API_URL}/auth/me`, {
  headers: { Authorization: `Bearer ${access_token}` },
});
const me = await meRes.json();
console.log(me);
```

- axios (ejemplo con interceptor)
```javascript
import axios from 'axios';

const api = axios.create({ baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000' });

// ejemplo: setear token manualmente
api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

// o usar interceptor para refrescar token en el futuro
```

Recomendaciones para el frontend
- Almacenar token con cuidado: usar cookies HttpOnly+Secure cuando sea posible. Evitar `localStorage` si puedes.
- Manejar expiración: si obtienes 401 por token expirado, redirigir a login o implementar flujo de refresh tokens (no disponible actualmente).
- Probar con Swagger UI en desarrollo para ver esquemas y ejemplos automáticos.

Errores comunes y cómo interpretarlos
- 400 Bad Request: datos inválidos o usuario ya existe.
- 401 Unauthorized: token inválido o expirado.
- 500 Internal Server Error: revisar logs del backend (p. ej. errores de hashing, BD, etc.).

Testing y herramientas
- Puedes importar una colección Postman (no incluida por defecto). Si la quieres, puedo generarla.
- Para tests automáticos del frontend, apuntar a una instancia local (`VITE_API_URL=http://localhost:8000`) o a un entorno de staging.

Contacto
- Si falta algún endpoint, cambia el contrato o quieres ejemplos en otro formato (Postman/Insomnia/CPP), dime y lo agrego.
