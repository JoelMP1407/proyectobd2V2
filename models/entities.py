# models/entities.py
# Definición declarativa de cada entidad del esquema del gimnasio.
# Esto alimenta un controlador CRUD genérico (una sola vista/lógica
# para todas las tablas) en lugar de repetir código por cada una.
#
# Estructura de cada columna:
#   name      -> nombre real de la columna en Oracle
#   label     -> etiqueta legible para mostrar en HTML
#   type      -> 'number' | 'text' | 'date' | 'select' | 'fk'
#   pk        -> True si forma parte de la clave primaria
#   auto      -> True si el sistema genera el valor (id surrogado, MAX+1)
#   required  -> True si es NOT NULL
#   options   -> lista de valores válidos (para type='select')
#   ref       -> clave de la entidad referenciada (para type='fk')
#
# Cada entidad además define:
#   table     -> nombre real de la tabla en Oracle
#   label     -> nombre humano singular
#   plural    -> nombre humano plural (para menús/listas)
#   pk        -> lista de columnas que forman la clave primaria
#   display   -> columnas (aparte de la PK) usadas para mostrar la fila
#                de forma legible en los <select> de FK

ENTITIES = {

    "usuario": {
        "table": "USUARIO", "label": "Usuario del Sistema", "plural": "Usuarios del Sistema",
        "pk": ["ID_USUARIO"], "display": ["USERNAME"],
        "columns": [
            {"name": "ID_USUARIO", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI", "label": "Persona asociada (CI)", "type": "fk", "ref": "persona"},
            {"name": "USERNAME", "label": "Usuario", "type": "text", "required": True},
            {"name": "PASSWORD", "label": "Contraseña", "type": "password"},
            {"name": "ROL", "label": "Rol", "type": "select",
             "options": ["ADMIN", "INSTRUCTOR", "RECEPCIONISTA", "MANTENIMIENTO", "CLIENTE"], "required": True},
            {"name": "ACTIVO", "label": "Activo", "type": "select", "options": ["1", "0"], "required": True},
        ],
    },

    "persona": {
        "table": "PERSONA", "label": "Persona", "plural": "Personas",
        "pk": ["CI"], "display": ["NOMBRE", "PATERNO"],
        "columns": [
            {"name": "CI", "label": "CI", "type": "number", "pk": True, "required": True},
            {"name": "NOMBRE", "label": "Nombre", "type": "text", "required": True},
            {"name": "PATERNO", "label": "Apellido Paterno", "type": "text", "required": True},
            {"name": "MATERNO", "label": "Apellido Materno", "type": "text"},
            {"name": "FECHA_NAC", "label": "Fecha de Nacimiento", "type": "date", "required": True},
            {"name": "SEXO", "label": "Sexo", "type": "select", "options": ["M", "F"], "required": True},
        ],
    },

    "fono_persona": {
        "table": "FONO_PERSONA", "label": "Teléfono de Persona", "plural": "Teléfonos",
        "pk": ["ID_FONO_PERSONA"], "display": ["FONO"],
        "columns": [
            {"name": "ID_FONO_PERSONA", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI", "label": "Persona", "type": "fk", "ref": "persona", "required": True},
            {"name": "FONO", "label": "Teléfono", "type": "number", "required": True},
        ],
    },

    "trabajador": {
        "table": "TRABAJADOR", "label": "Trabajador", "plural": "Trabajadores",
        "pk": ["CI"], "display": [],
        "columns": [
            {"name": "CI", "label": "Persona (CI)", "type": "fk", "ref": "persona", "pk": True, "required": True},
            {"name": "SALIDA", "label": "Hora de Salida", "type": "text"},
            {"name": "ENTRADA", "label": "Hora de Entrada", "type": "text"},
            {"name": "SUELDO", "label": "Sueldo", "type": "number"},
        ],
    },

    "instructor": {
        "table": "INSTRUCTOR", "label": "Instructor", "plural": "Instructores",
        "pk": ["CI"], "display": ["CERTIFICACION"],
        "columns": [
            {"name": "CI", "label": "Trabajador (CI)", "type": "fk", "ref": "trabajador", "pk": True, "required": True},
            {"name": "CERTIFICACION", "label": "Certificación", "type": "text"},
            {"name": "ANIOS_EXPERIENCIA", "label": "Años de Experiencia", "type": "number"},
        ],
    },

    "mantenimiento": {
        "table": "MANTENIMIENTO", "label": "Personal de Mantenimiento", "plural": "Mantenimiento (Personal)",
        "pk": ["CI"], "display": [],
        "columns": [
            {"name": "CI", "label": "Trabajador (CI)", "type": "fk", "ref": "trabajador", "pk": True, "required": True},
        ],
    },

    "material_mantenimiento": {
        "table": "MATERIAL_MANTENIMIENTO", "label": "Material de Mantenimiento", "plural": "Materiales de Mantenimiento",
        "pk": ["ID_MATERIAL_MANTENIMIENTO"], "display": ["MATERIAL"],
        "columns": [
            {"name": "ID_MATERIAL_MANTENIMIENTO", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI", "label": "Encargado de Mantenimiento", "type": "fk", "ref": "mantenimiento", "required": True},
            {"name": "MATERIAL", "label": "Material", "type": "text", "required": True},
        ],
    },

    "recepcionista": {
        "table": "RECEPCIONISTA", "label": "Recepcionista", "plural": "Recepcionistas",
        "pk": ["CI"], "display": [],
        "columns": [
            {"name": "CI", "label": "Trabajador (CI)", "type": "fk", "ref": "trabajador", "pk": True, "required": True},
            {"name": "NRO_CAJA", "label": "Nro. de Caja", "type": "number"},
        ],
    },

    "cliente": {
        "table": "CLIENTE", "label": "Cliente", "plural": "Clientes",
        "pk": ["CI"], "display": [],
        "columns": [
            {"name": "CI", "label": "Persona (CI)", "type": "fk", "ref": "persona", "pk": True, "required": True},
            {"name": "CI_ENTRENADOR", "label": "Entrenador Asignado", "type": "fk", "ref": "instructor"},
            {"name": "ALTURA", "label": "Altura (m)", "type": "number"},
            {"name": "PESO", "label": "Peso (kg)", "type": "number"},
        ],
    },

    "area": {
        "table": "AREA", "label": "Área", "plural": "Áreas",
        "pk": ["ID_AREA"], "display": ["DESCRIPCION"],
        "columns": [
            {"name": "ID_AREA", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "DESCRIPCION", "label": "Descripción", "type": "text"},
            {"name": "CAPACIDAD", "label": "Capacidad", "type": "number"},
        ],
    },

    "membresia": {
        "table": "MEMBRESIA", "label": "Membresía", "plural": "Membresías",
        "pk": ["ID_MEMBRESIA"], "display": ["TIPO"],
        "columns": [
            {"name": "ID_MEMBRESIA", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "TIPO", "label": "Tipo", "type": "text", "required": True},
            {"name": "PRECIO", "label": "Precio", "type": "number"},
            {"name": "CI", "label": "Recepcionista que la registró", "type": "fk", "ref": "recepcionista"},
        ],
    },

    "paga": {
        "table": "PAGA", "label": "Pago de Membresía", "plural": "Pagos de Membresía",
        "pk": ["CI_CLIENTE", "ID_MEMBRESIA", "FECHA_INI"], "display": [],
        "columns": [
            {"name": "CI_CLIENTE", "label": "Cliente", "type": "fk", "ref": "cliente", "pk": True, "required": True},
            {"name": "ID_MEMBRESIA", "label": "Membresía", "type": "fk", "ref": "membresia", "pk": True, "required": True},
            {"name": "FECHA_INI", "label": "Fecha Inicio", "type": "date", "pk": True, "required": True},
            {"name": "FECHA_FIN", "label": "Fecha Fin", "type": "date"},
            {"name": "TURNO", "label": "Turno", "type": "select", "options": ["Tarde", "Mañana", "Noche"]},
        ],
    },

    "maquina": {
        "table": "MAQUINA", "label": "Máquina", "plural": "Máquinas",
        "pk": ["ID_MAQUINA"], "display": ["NOMBRE"],
        "columns": [
            {"name": "ID_MAQUINA", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "NOMBRE", "label": "Nombre", "type": "text", "required": True},
            {"name": "MUSCULO_OBJETIVO", "label": "Músculo Objetivo", "type": "text"},
            {"name": "MARCA", "label": "Marca", "type": "text"},
            {"name": "ID_AREA", "label": "Área", "type": "fk", "ref": "area"},
        ],
    },

    "actividad": {
        "table": "ACTIVIDAD", "label": "Actividad", "plural": "Actividades",
        "pk": ["ID_ACTIVIDAD"], "display": ["NOMBRE"],
        "columns": [
            {"name": "ID_ACTIVIDAD", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "DESCRIPCION", "label": "Descripción", "type": "text"},
            {"name": "CAPACIDAD", "label": "Capacidad", "type": "number"},
            {"name": "NOMBRE", "label": "Nombre", "type": "text", "required": True},
            {"name": "ID_AREA", "label": "Área", "type": "fk", "ref": "area"},
        ],
    },

    "organiza": {
        "table": "ORGANIZA", "label": "Organización de Actividad", "plural": "Actividades Organizadas",
        "pk": ["CI", "ID_ACTIVIDAD"], "display": [],
        "columns": [
            {"name": "CI", "label": "Instructor", "type": "fk", "ref": "instructor", "pk": True, "required": True},
            {"name": "ID_ACTIVIDAD", "label": "Actividad", "type": "fk", "ref": "actividad", "pk": True, "required": True},
            {"name": "FECHA", "label": "Fecha", "type": "date", "required": True},
            {"name": "HORA", "label": "Hora", "type": "text"},
        ],
    },

    "casillero": {
        "table": "CASILLERO", "label": "Casillero", "plural": "Casilleros",
        "pk": ["ID_CASILLERO"], "display": ["TAMANIO"],
        "columns": [
            {"name": "ID_CASILLERO", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "TAMANIO", "label": "Tamaño", "type": "text"},
            {"name": "CI", "label": "Cliente", "type": "fk", "ref": "cliente"},
        ],
    },

    "condicion_medica_cliente": {
        "table": "CONDICION_MEDICA_CLIENTE", "label": "Condición Médica", "plural": "Condiciones Médicas",
        "pk": ["ID_CONDICION"], "display": ["CONDICION_MEDICA"],
        "columns": [
            {"name": "ID_CONDICION", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI", "label": "Cliente", "type": "fk", "ref": "cliente"},
            {"name": "CONDICION_MEDICA", "label": "Condición Médica", "type": "text"},
        ],
    },

    "suplemento": {
        "table": "SUPLEMENTO", "label": "Suplemento", "plural": "Suplementos",
        "pk": ["ID_SUPLEMENTO"], "display": ["NOMBRE"],
        "columns": [
            {"name": "ID_SUPLEMENTO", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "PESO", "label": "Peso", "type": "number"},
            {"name": "NOMBRE", "label": "Nombre", "type": "text", "required": True},
            {"name": "PRECIO", "label": "Precio", "type": "number"},
        ],
    },

    "compra": {
        "table": "COMPRA", "label": "Compra", "plural": "Compras",
        "pk": ["ID_COMPRA"], "display": [],
        "columns": [
            {"name": "ID_COMPRA", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI", "label": "Cliente", "type": "fk", "ref": "cliente"},
            {"name": "ID_SUPLEMENTO", "label": "Suplemento", "type": "fk", "ref": "suplemento"},
        ],
    },

    "vende": {
        "table": "VENDE", "label": "Venta", "plural": "Ventas",
        "pk": ["ID_VENDE"], "display": [],
        "columns": [
            {"name": "ID_VENDE", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "FECHA_VENTA", "label": "Fecha de Venta", "type": "date"},
            {"name": "CI", "label": "Recepcionista", "type": "fk", "ref": "recepcionista"},
            {"name": "ID_SUPLEMENTO", "label": "Suplemento", "type": "fk", "ref": "suplemento"},
        ],
    },

    "ofrece_sesion": {
        "table": "OFRECE_SESION", "label": "Sesión Ofrecida", "plural": "Sesiones Ofrecidas",
        "pk": ["ID_OFRECE"], "display": [],
        "columns": [
            {"name": "ID_OFRECE", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI_C", "label": "Cliente", "type": "fk", "ref": "cliente"},
            {"name": "CI_R", "label": "Recepcionista", "type": "fk", "ref": "recepcionista"},
            {"name": "HORA", "label": "Hora", "type": "text"},
            {"name": "COSTO", "label": "Costo", "type": "number"},
            {"name": "FECHA", "label": "Fecha", "type": "date"},
        ],
    },

    "mantiene": {
        "table": "MANTIENE", "label": "Mantenimiento de Área", "plural": "Mantenimientos de Área",
        "pk": ["ID_MANTIENE"], "display": [],
        "columns": [
            {"name": "ID_MANTIENE", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "CI", "label": "Encargado de Mantenimiento", "type": "fk", "ref": "mantenimiento"},
            {"name": "ID_AREA", "label": "Área", "type": "fk", "ref": "area"},
        ],
    },

    "asiste": {
        "table": "ASISTE", "label": "Asistencia", "plural": "Asistencias",
        "pk": ["ID_ASISTE"], "display": [],
        "columns": [
            {"name": "ID_ASISTE", "label": "ID", "type": "number", "pk": True, "auto": True},
            {"name": "ID_ACTIVIDAD", "label": "Actividad", "type": "fk", "ref": "actividad"},
            {"name": "CI", "label": "Cliente", "type": "fk", "ref": "cliente"},
        ],
    },
}


def get_entity(key):
    """Devuelve la config de la entidad o None si no existe."""
    return ENTITIES.get(key)
