# Consumo de la API de Horarios

Guía práctica para integrar el frontend con la API: endpoints clave, ejemplos (curl, fetch, axios), autenticación y manejo de tokens.

Base URL (desarrollo)
- http://localhost:8000

Documentación interactiva
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Variables de entorno (frontend)
- Archivo sugerido: `.env.example` (en la raíz del repositorio)
- Variables importantes:
  - VITE_API_URL=http://localhost:8000  # o REACT_APP_API_URL según tu stack

Autenticación (JWT Bearer)
- 1) Registrar usuario: `POST /auth/register` (JSON)
- 2) Login: `POST /auth/login` (x-www-form-urlencoded) — devuelve `access_token`.
- 3) Usar el token en endpoints protegidos: `Authorization: Bearer <ACCESS_TOKEN>`.
- Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`.

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
  -d '{"username":"juan","email":"juan@example.com","password":"mipass123","role":"SECRETARIA"}'
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

// si implementas refresh tokens, aquí puedes manejar la renovación
```

Recomendaciones
- Token: preferir cookies HttpOnly+Secure cuando sea viable. Evitar `localStorage` si es posible.
- Expiración: ante 401 por token expirado, redirige a login o implementa refresh tokens (no incluido por defecto).
- Desarrollo: usa Swagger UI para validar contratos y probar rápidamente.

Errores comunes y cómo interpretarlos
- 400 Bad Request: datos inválidos o usuario ya existe.
- 401 Unauthorized: token inválido o expirado.
- 500 Internal Server Error: revisar logs del backend (p. ej. errores de hashing, BD, etc.).

Testing
- Para tests del frontend, apunta a una instancia local (`VITE_API_URL=http://localhost:8000`) o a un entorno de staging.

Contacto
- Si necesitas otros ejemplos (Postman/Insomnia) o detectar cambios de contrato, abre un issue en el repositorio.
