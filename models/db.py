# models/db.py
# Conexión a Oracle y funciones genéricas de acceso a datos (CRUD dinámico)

import oracledb
from config import DB_USER, DB_PASSWORD, DB_DSN


def get_connection():
    try:
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        return connection
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al conectar a Oracle: {error.message}")
        raise


def fetch_all(table, order_by=None, filter_col=None, filter_value=None):
    """
    Devuelve todas las filas de una tabla como lista de dicts.
    Si se pasan filter_col/filter_value, agrega un WHERE col = :1
    (se usa para que el rol CLIENTE solo vea SUS propias filas).
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"SELECT * FROM {table}"
        params = []
        if filter_col is not None:
            sql += f" WHERE {filter_col} = :1"
            params.append(filter_value)
        if order_by:
            sql += f" ORDER BY {order_by}"
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        return rows
    finally:
        conn.close()


def get_usuario_by_username(username):
    """Busca un usuario de la tabla USUARIO por su username (login)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT ID_USUARIO, CI, USERNAME, PASSWORD_HASH, ROL, ACTIVO "
            "FROM USUARIO WHERE UPPER(USERNAME) = UPPER(:1)",
            [username],
        )
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        return dict(zip(cols, row)) if row else None
    finally:
        conn.close()


def fetch_one(table, pk_cols, pk_values):
    """Devuelve una fila específica según su(s) columna(s) de PK."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        where = " AND ".join([f"{c} = :{i+1}" for i, c in enumerate(pk_cols)])
        sql = f"SELECT * FROM {table} WHERE {where}"
        cur.execute(sql, pk_values)
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        return dict(zip(cols, row)) if row else None
    finally:
        conn.close()


def next_id(table, id_col):
    """
    Genera un siguiente ID simple usando MAX(col)+1.
    Nota: válido para uso académico/monousuario. Para producción real
    se recomienda usar SEQUENCE + TRIGGER en Oracle.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT NVL(MAX({id_col}), 0) + 1 FROM {table}")
        return cur.fetchone()[0]
    finally:
        conn.close()


def insert_row(table, data: dict):
    """Inserta una fila. data = {columna: valor}."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cols = list(data.keys())
        placeholders = [f":{i+1}" for i in range(len(cols))]
        sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
        cur.execute(sql, list(data.values()))
        conn.commit()
    finally:
        conn.close()


def update_row(table, data: dict, pk_cols, pk_values):
    """Actualiza una fila según su(s) columna(s) de PK."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        set_clause = ", ".join([f"{c} = :{i+1}" for i, c in enumerate(data.keys())])
        offset = len(data)
        where_clause = " AND ".join([f"{c} = :{offset+i+1}" for i, c in enumerate(pk_cols)])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        cur.execute(sql, list(data.values()) + list(pk_values))
        conn.commit()
    finally:
        conn.close()


def delete_row(table, pk_cols, pk_values):
    conn = get_connection()
    try:
        cur = conn.cursor()
        where_clause = " AND ".join([f"{c} = :{i+1}" for i, c in enumerate(pk_cols)])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        cur.execute(sql, pk_values)
        conn.commit()
    finally:
        conn.close()


def fetch_fk_options(ref_table, value_col, display_cols):
    """
    Devuelve lista de tuplas (valor, etiqueta) para poblar un <select>
    a partir de una tabla referenciada por FK.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cols_sql = ", ".join([value_col] + display_cols)
        cur.execute(f"SELECT {cols_sql} FROM {ref_table} ORDER BY {value_col}")
        options = []
        for row in cur.fetchall():
            value = row[0]
            label_parts = [str(x) for x in row[1:] if x is not None]
            label = f"{value} - {' '.join(label_parts)}" if label_parts else str(value)
            options.append((value, label))
        return options
    finally:
        conn.close()

def run_query(sql, params=None):
    """
    Ejecuta cualquier sentencia SQL/PL-SQL.
    Si es un SELECT, devuelve (columnas, filas).
    Si es DDL/DML (CREATE, INSERT, UPDATE, DELETE, etc.), la ejecuta,
    hace commit y devuelve ([], []).
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or {})
        if cur.description is None:
            conn.commit()
            return [], []
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        return cols, rows
    finally:
        conn.close()