## Correr la aplicacion 

```
uvicorn main:app --reload
```

### Api
**Endpoints o rutas**

### Sevices
**Logica para generar examenes, validaciones, etc**

### Repositories
**Acceso a datos o operaciones sobre la bd, crear, get, update, etc**

### Models
**Modelos de la bd (las tablas)**

### Schemas
**Esquemas de la bd (formatos de datos para entrada/salida de la api)**

### Core
**Conexion y configuraciones de/a la bd, etc**

### Ejemplo
`peticion(crear examen) -> api(recibe peticion) -> schemas(valida formato datos) -> services(genera examen) -> repositories (guarda en bd) -> models(tabla bd) -> schemas(formato respuesta) -> respuesta`


