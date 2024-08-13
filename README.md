## BACK de Magic Tricks

### Descripción

El presente código fue confeccionado para servir de soporte a las operaciones de importancia que ocurren detrás del proyecto "Magic Tricks" alojado en "(URL del proyecto)". Fue desarrollado con FastAPI, bajo el lenguaje Python, y cuenta con dos bases de datos: una no relacional y otra relacional.

### Bases de Datos

#### No Relacional

La primera base de datos está alojada en MongoDB (con un clúster en San Pablo) y almacena los datos de los usuarios (nombre, contraseña, ID, etc.).

#### Relacional

La segunda base de datos fue confeccionada en MySQL y está encargada de almacenar los datos para el análisis (con asiento en París).

### Documentación Específica

Los modelos, endpoints y esquemas de interrelación están resumidos en el siguiente URL: [Documentación de la API](URL_de_acceso_a_la_aplicacion/docs).

## Endpoints

### **/login/on** (POST)
- **Descripción:** Inicia sesión y devuelve un token.
- **Request Body:**
  ```json
  {
    "id": "string",
    "username": "string",
    "email": "string",
    "disable": false,
    "password": "string"
  }
- **Responses:**
    - **201 Created:**

    {
    "id": "string",
    "username": "string",
    "email": "string",
    "disable": false
    }

    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }

### **/login/** (POST)
- **Descripción:** Autenticación de usuario mediante application/x-www-form-urlencoded.
- **Request Body:**
    grant_type: string
    username: string (requerido)
    password: string (requerido)
    scope: string
    client_id: string
    client_secret: string
- **Responses:**
    - **200 OK:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }

### /login/verify-token (GET)
- **Descripción:** Verifica el token de autenticación.
- **Responses:**
    - **200 OK:**
    "string"
    - **404 Not Found:**
    "string"

### **/number/all** (GET)
- **Descripción:** Obtiene todos los números.
- **Responses:**
    - **200 OK:**
    "string"
    - **404 Not Found:**
    "string"

### **/number/call_ua** (GET)
- **Descripción:** Obtiene datos por unidad y año.
- **Parameters:**
    uni: string (query)
    año: integer (query)
- **Responses:**
    - **200 OK:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }
### **/number/call_uad** (GET)
- **Descripción:** Obtiene datos por unidad, año y día.
- **Parameters:**
    uni: string (query)
    año: integer (query)
    dia: integer (query)
- **Responses:**
    - **200 OK:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }
### **/number/on_numbers** (POST)
- **Descripción:** Inserta un nuevo número.
- **Request Body:**
    {
    "id_accion": 0,
    "ronda": 0,
    "hora": 0,
    "votos": 0,
    "propios": 0,
    "uni": "string",
    "año": 0,
    "dia": 0
    }
- **Responses:**
    - **201 Created:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }
### **/number/up_numbers** (PUT)
- **Descripción:** Actualiza un número existente.
- **Request Body:**
    {
    "id_accion": 0,
    "ronda": 0,
    "hora": 0,
    "votos": 0,
    "propios": 0,
    "uni": "string",
    "año": 0,
    "dia": 0
    }
- **Responses:**
    - **200 OK:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }
### **/number/del_numbers** (DELETE)
- **Descripción:** Elimina un número.
- **Request Body:**
    {
    "id_accion": 0,
    "ronda": 0,
    "hora": 0,
    "votos": 0,
    "propios": 0,
    "uni": "string",
    "año": 0,
    "dia": 0
    }
- **Responses:**
    - **204 No Content:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }
### **/number/del_numbers_ronda** (DELETE)
- **Descripción:** Elimina números basados en unidad, año, día y ronda.
- **Parameters:**
    uni: string (query)
    año: integer (query)
    dia: integer (query)
    ronda: integer (query)
- **Responses:**
    - **204 No Content:**
    "string"
    - **404 Not Found:**
    "string"
    - **422 Unprocessable Entity:**
    {
    "detail": [
        {
        "loc": [
            "string",
            0
        ],
        "msg": "string",
        "type": "string"
        }
    ]
    }
### **/** (GET)
- **Descripción:** Raíz del servicio.
- **Responses:**
    - **200 OK:**
    "string"

## Esquemas

### Body_login_login__post
    grant_type: string | null
    username: string
    password: string
    scope: string
    client_id: string | null
    client_secret: string | null

### Dias
    id_accion: integer | null
    ronda: integer
    hora: number
    votos: integer
    propios: integer
    uni: string
    año: integer
    dia: integer

### HTTPValidationError
    detail: array of objects
    loc: array of (string | integer)
    msg: string
    type: string

### User
    id: string | null
    username: string
    email: string

