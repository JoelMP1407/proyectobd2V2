# seed_usuarios.py
# Crea usuarios iniciales en la tabla USUARIO con la contraseña ya
# hasheada (nunca se guarda en texto plano). Ejecutar UNA vez, después
# de correr codigo.sql, con:
#
#   python seed_usuarios.py
#
# Puedes editar la lista USUARIOS_INICIALES de más abajo antes de
# ejecutarlo, o volver a llamar crear_usuario(...) para agregar más.

from werkzeug.security import generate_password_hash
from models import db

# Si el usuario representa a un empleado/cliente ya cargado en PERSONA,
# pon su CI aquí (respeta la FK). Si es una cuenta "de sistema" sin
# persona asociada (p. ej. el admin), deja ci=None.
USUARIOS_INICIALES = [
    # (ci, username, password, rol)
    # (None, "admin", "A12%$%BGfdas", "ADMIN"),
    (None, "instructor1", "AUSH16$%21d3", "INSTRUCTOR"),
    (None, "recepcionista1", "dasjiYD628$%", "RECEPCIONISTA"),
    (None, "mantenimiento1", "uh(aUIH123ed", "MANTENIMIENTO"),
    (None, "cliente1", "87HIShydas%&", "CLIENTE"),
]


def crear_usuario(ci, username, password_plano, rol):
    pw_hash = generate_password_hash(password_plano)
    id_usuario = db.next_id("USUARIO", "ID_USUARIO")
    db.insert_row("USUARIO", {
        "ID_USUARIO": id_usuario,
        "CI": ci,
        "USERNAME": username,
        "PASSWORD_HASH": pw_hash,
        "ROL": rol,
        "ACTIVO": 1,
    })
    print(f"OK: usuario '{username}' creado con rol {rol}.")


if __name__ == "__main__":
    for ci, username, password, rol in USUARIOS_INICIALES:
        try:
            crear_usuario(ci, username, password, rol)
        except Exception as e:
            print(f"ERROR creando '{username}': {e}")

    print("\nListo. Inicia sesión en /login con las credenciales de arriba")
    print("y cámbialas cuanto antes (esto es solo para el primer arranque).")
