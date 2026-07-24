# Sistema de Gestión de Gimnasio — Flask + Oracle (estructura MVC)

CRUD tradicional (HTML/Jinja2) para las 21 tablas del esquema del gimnasio,
usando Oracle 23c (`OraDB23Home1`, servicio `FREEPDB1`).

## Estructura de carpetas

```
gimnasio_flask/
├── app.py                        # Punto de entrada: crea la app y registra el controlador
├── config.py                     # Credenciales de conexión a Oracle
├── requirements.txt
├── README.md
├── models/
│   ├── __init__.py
│   ├── db.py                     # Acceso a datos: SELECT/INSERT/UPDATE/DELETE genéricos
│   └── entities.py               # Definición de las 21 tablas (columnas, tipos, FKs)
├── controllers/
│   ├── __init__.py
│   └── crud_controller.py        # Blueprint: TODAS las rutas (listar/crear/editar/borrar)
├── templates/
│   ├── base.html                 # Layout con navbar (Bootstrap 5 vía CDN)
│   ├── index.html                # Menú principal con las 21 entidades
│   ├── list.html                 # Tabla genérica de cualquier entidad
│   └── form.html                 # Formulario genérico (number/text/date/select/fk)
└── static/
    └── style.css                 # Para tus estilos propios (opcional)
```

## 1. Instalación (primera vez)

Abre una terminal DENTRO de la carpeta `gimnasio_flask`:

```bash
cd ruta\donde\descargaste\gimnasio_flask
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno virtual (Windows):

```bash
venv\Scripts\activate
```

Activar entorno virtual (Linux/Mac):

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 2. Configurar conexión a Oracle

Editar `config.py`:

```python
DB_USER = "bd272"
DB_PASSWORD = "12345"
DB_DSN = "localhost:1521/FREEPDB1"
```

## 3. Crear las tablas en Oracle

Antes de correr la app, ejecuta el script `.sql` con los `CREATE TABLE`
(el que ya tienes) sobre el esquema `bd272`, usando SQL Developer,
SQL*Plus o tu cliente preferido. La app NO crea las tablas, asume que
ya existen.

## 4. Ejecutar la aplicación

```bash
python app.py
```

Deberías ver:

```
 * Running on http://127.0.0.1:5000
```

Abrir en el navegador: **http://127.0.0.1:5000**

## 5. Las próximas veces (ya instalado)

Solo necesitas:

```bash
cd ruta\donde\descargaste\gimnasio_flask
venv\Scripts\activate
python app.py
```

## 6. Cómo funciona el patrón MVC aquí

- **Modelo (`models/`)**: `entities.py` describe QUÉ es cada tabla
  (columnas, tipos, PK, FK). `db.py` sabe CÓMO hablar con Oracle
  (SQL genérico parametrizado).
- **Controlador (`controllers/crud_controller.py`)**: un Blueprint con
  4 rutas genéricas (`/<entidad>/`, `/new`, `/edit/<pk>`, `/delete/<pk>`)
  que sirven para las 21 tablas — no hay que escribir un controlador
  por tabla.
- **Vista (`templates/`)**: `list.html` y `form.html` se adaptan según
  la configuración de la entidad (number/text/date/select/fk).

Si necesitas agregar una tabla nueva o cambiar una columna, **no tocas
el controlador ni los templates** — solo agregas/editas la entrada
correspondiente en `models/entities.py`.

## 7. Detalles importantes

- **FK como `<select>`:** al crear un `Instructor` puedes elegir entre
  los `Trabajador` ya existentes (respeta la jerarquía
  Persona → Trabajador → Instructor/Recepcionista/Mantenimiento).
- **PK compuestas** (`PAGA`, `ORGANIZA`): se codifican en la URL
  separadas por `~` (ej. `/paga/edit/10~3~2026-01-15`).
- **IDs autogenerados** (`ID_AREA`, `ID_MEMBRESIA`, etc.): usan
  `NVL(MAX(id),0)+1`. Válido para uso académico de un solo usuario.
  Para producción con varios usuarios concurrentes, usar
  `SEQUENCE` + `TRIGGER` de Oracle en su lugar.
- **Eliminar con relaciones:** si un registro tiene hijos, Oracle
  rechaza el `DELETE` y la app muestra el error tal cual.
