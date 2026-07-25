import time
from flask import Blueprint, render_template, request, flash
from models.db import get_connection # Asegúrate de importar tu función de conexión a Oracle

terminal_bp = Blueprint('terminal', __name__)

@terminal_bp.route('/terminal', methods=['GET', 'POST'])
def consola_sql():
    sql_query = ""
    columnas = []
    resultados = []
    filas_afectadas = 0
    tiempo_ms = 0
    error_msg = None
    es_select = False

    if request.method == 'POST':
        sql_query = request.form.get('sql', '').strip()
        
        if sql_query:
            conn = get_connection()
            cursor = conn.cursor()
            inicio = time.time()
            
            try:
                cursor.execute(sql_query)
                tiempo_ms = round((time.time() - inicio) * 1000, 2)
                
                # Si la consulta devuelve filas (SELECT)
                if cursor.description:
                    es_select = True
                    columnas = [col[0] for col in cursor.description]
                    resultados = cursor.fetchall()
                else:
                    # Es una sentencia DML (INSERT, UPDATE, DELETE)
                    filas_afectadas = cursor.rowcount
                    conn.commit()
                    
            except Exception as e:
                error_msg = str(e)
            finally:
                cursor.close()
                conn.close()

    return render_template(
        'terminal.html',
        sql_query=sql_query,
        columnas=columnas,
        resultados=resultados,
        filas_afectadas=filas_afectadas,
        tiempo_ms=tiempo_ms,
        error_msg=error_msg,
        es_select=es_select
    )