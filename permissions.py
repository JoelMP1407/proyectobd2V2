# permissions.py
# Matriz de permisos por rol para el sistema del gimnasio.
#
# Cada rol tiene un diccionario {entity_key: {acciones permitidas}}.
# Acciones posibles: "view", "create", "edit", "delete".
# El rol "ADMIN" usa la clave especial "*" -> significa "todas las entidades".
#
# OWNER_COLUMN indica, para el rol CLIENTE, qué columna de cada tabla
# identifica al "dueño" del registro (su propio CI). Así, un cliente
# que entra al sistema solo ve SUS propias filas, no las de los demás.

ALL_ACTIONS = {"view", "create", "edit", "delete"}
RW = {"view", "create", "edit", "delete"}
RO = {"view"}

ROLES = ["ADMIN", "INSTRUCTOR", "RECEPCIONISTA", "MANTENIMIENTO", "CLIENTE"]

PERMISSIONS = {

    "ADMIN": {
        "*": ALL_ACTIONS,  # acceso total a todas las entidades, incluida "usuario"
    },

    # Entrenador: gestiona actividades/clases y asistencia; puede ver a
    # sus clientes y editar su propio perfil de instructor.
    "INSTRUCTOR": {
        "instructor": {"view", "edit"},
        "cliente": RO,
        "area": RO,
        "maquina": RO,
        "actividad": RW,
        "organiza": RW,
        "asiste": RW,
    },

    # Recepcionista: atiende a los clientes en mostrador (altas, membresías,
    # pagos, casilleros, venta de suplementos, sesiones).
    "RECEPCIONISTA": {
        "persona": RW,
        "fono_persona": RW,
        "cliente": RW,
        "membresia": RW,
        "paga": RW,
        "casillero": RW,
        "suplemento": RW,
        "compra": RW,
        "vende": RW,
        "ofrece_sesion": RW,
        "area": RO,
        "maquina": RO,
        "actividad": RO,
        "instructor": RO,
    },

    # Mantenimiento: administra materiales y el mantenimiento de áreas/máquinas.
    "MANTENIMIENTO": {
        "material_mantenimiento": RW,
        "mantiene": RW,
        "area": RO,
        "maquina": RO,
    },

    # Cliente: solo lectura, y únicamente de SUS propios registros
    # (ver OWNER_COLUMN), más catálogos generales de solo consulta.
    "CLIENTE": {
        "persona": RO,
        "cliente": RO,
        "paga": RO,
        "casillero": RO,
        "compra": RO,
        "asiste": RO,
        "ofrece_sesion": RO,
        "condicion_medica_cliente": RO,
        "membresia": RO,
        "suplemento": RO,
        "actividad": RO,
        "area": RO,
        "maquina": RO,
    },
}

# Columna que identifica al cliente dueño del registro, usada para filtrar
# filas cuando el rol es CLIENTE. Las entidades que no aparecen aquí (p.ej.
# membresia, suplemento, actividad, area, maquina) se muestran sin filtrar
# porque son catálogos generales, no datos privados de un cliente.
OWNER_COLUMN = {
    "persona": "CI",
    "cliente": "CI",
    "paga": "CI_CLIENTE",
    "casillero": "CI",
    "compra": "CI",
    "asiste": "CI",
    "ofrece_sesion": "CI_C",
    "condicion_medica_cliente": "CI",
}


def get_entity_permissions(rol, entity_key):
    """Devuelve el set de acciones permitidas para (rol, entidad)."""
    perms = PERMISSIONS.get(rol, {})
    if "*" in perms:
        return perms["*"]
    return perms.get(entity_key, set())


def can(rol, entity_key, action):
    return action in get_entity_permissions(rol, entity_key)


def allowed_entities(rol):
    """
    Devuelve la lista de entity_key visibles para el rol (con permiso "view").
    Devuelve None si el rol tiene acceso total (ADMIN) -> el llamador debe
    interpretar None como "todas las entidades registradas".
    """
    perms = PERMISSIONS.get(rol, {})
    if "*" in perms:
        return None
    return [key for key, actions in perms.items() if "view" in actions]


def owner_column_for(entity_key):
    return OWNER_COLUMN.get(entity_key)
