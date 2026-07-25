# cambiar_password_admin.py
# Actualiza la contraseña del usuario "admin" ya existente en la tabla USUARIO.
#
#   python cambiar_password_admin.py
#
# Si falla por bloqueo: cierra la app Flask (python app.py) y termina
# terminales python colgadas (Ctrl+C). Luego vuelve a ejecutar.

import sys

import oracledb
from werkzeug.security import generate_password_hash

from config import DB_DSN, DB_PASSWORD, DB_USER

USERNAME = "admin"
NUEVA_PASSWORD = "A12%$%BGfdas"  # cámbiala aquí
TIMEOUT_MS = 15000


def _listar_sesiones_activas(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sid, serial#, status, program
        FROM v$session
        WHERE username = UPPER(:1)
        ORDER BY sid
        """,
        [DB_USER],
    )
    return cur.fetchall()


def main():
    print(f"Conectando a Oracle ({DB_DSN})...", flush=True)
    conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    conn.callTimeout = TIMEOUT_MS

    try:
        cur = conn.cursor()
        print(f"Buscando usuario '{USERNAME}'...", flush=True)
        cur.execute(
            "SELECT ID_USUARIO FROM USUARIO WHERE UPPER(USERNAME) = UPPER(:1)",
            [USERNAME],
        )
        row = cur.fetchone()
        if not row:
            print(f"No existe un usuario con username '{USERNAME}'.")
            return 1

        id_usuario = row[0]
        nuevo_hash = generate_password_hash(NUEVA_PASSWORD)
        print("Actualizando contraseña...", flush=True)
        cur.execute(
            "UPDATE USUARIO SET PASSWORD_HASH = :1 WHERE ID_USUARIO = :2",
            [nuevo_hash, id_usuario],
        )
        conn.commit()
        print(f"OK: contraseña de '{USERNAME}' actualizada.")
        print(f"Inicia sesión en /login con usuario '{USERNAME}' y la nueva contraseña.")
        return 0
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error de Oracle: {error.message}", file=sys.stderr)
        if "timeout" in error.message.lower() or getattr(error, "code", None) == 12170:
            print(
                "\nLa fila de 'admin' está bloqueada por otra sesión de Oracle.",
                file=sys.stderr,
            )
            print("Sesiones abiertas con tu usuario de BD:", file=sys.stderr)
            for sid, serial, status, program in _listar_sesiones_activas(conn):
                print(f"  SID {sid}, serial {serial}, {status}, {program}", file=sys.stderr)
            print(
                "\nQué hacer:\n"
                "  1. Cierra la app Flask si está corriendo (python app.py).\n"
                "  2. En Git Bash/terminal, pulsa Ctrl+C en scripts python colgados.\n"
                "  3. En SQL Developer, haz Commit o Rollback si editaste USUARIO.\n"
                "  4. Vuelve a ejecutar: python cambiar_password_admin.py",
                file=sys.stderr,
            )
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
