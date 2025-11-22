import pymysql
from pymysql.cursors import DictCursor
# domusmarket2024@gmail.com
# SOMOSDOMUS2024

# BD_HOST = 'DomusMarket.mysql.pythonanywhere-services.com'
# BD_USER = 'DomusMarket'
# BD_PSWD = 'SOMOSDOMUS2024'
# BD_DBNM = 'DomusMarket$domus_market'

BD_HOST = 'localhost'
BD_USER = 'root'
BD_PSWD = ''
BD_DBNM = 'domus_market2'

# BD_PORT = 3306

def obtener_conexion():
    return pymysql.connect(
        host = BD_HOST,
        # port = BD_PORT,
        user = BD_USER,
        password = BD_PSWD,
        db = BD_DBNM ,
        # cursorclass = DictCursor
        )


def sql_select_fetchall(sql , args = None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute(sql , args)
            resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except Exception as e:
        return e


def sql_select_fetchone(sql , args = None):
    conexion = obtener_conexion()
    try: 
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute(sql, args)
            resultados = cursor.fetchone()
        conexion.close()
        return resultados
    except Exception as e:
        return e


def sql_execute(sql , args = None):
    conexion = obtener_conexion()
    with conexion.cursor(DictCursor) as cursor:
        cursor.execute( sql , args)
    conexion.commit()
    conexion.close()


def sql_execute_lastrowid(sql , args = None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute( sql , args )
            last_id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return last_id
    except Exception as e:
        return e


def sql_execute_transaction(list_sql):
    conexion = obtener_conexion()
    list_data = []
    try:
        with conexion.cursor(DictCursor) as cursor:
            for sql in list_sql:
                data = None
                cursor.execute( sql[0] , sql[1] )
                if sql[2] == 'all':
                    data = cursor.fetchall()
                elif sql[2] == 'one':
                    data = cursor.fetchone()
                elif sql[2] == 'id':
                    data = cursor.lastrowid
                else:
                    data = None
                list_data.append(data)
            conexion.commit()
        return list_data
    except Exception as e:
        conexion.rollback()
        return e


def bd_insert(tabla, columnas, valores):
    """
    tabla: str, nombre de la tabla
    columnas: list[str], nombres de columnas
    valores: list, valores a insertar (en el mismo orden de columnas)
    """
    cols_str = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(valores))
    
    sql = f'''
        INSERT INTO {tabla} ({cols_str})
        VALUES ({placeholders})
    '''
    return sql_execute(sql, valores)


def bd_insert_lastrowid(tabla, columnas, valores):
    """
    tabla: str, nombre de la tabla
    columnas: list[str], nombres de columnas
    valores: list, valores a insertar (en el mismo orden de columnas)
    """
    cols_str = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(valores))
    
    sql = f'''
        INSERT INTO {tabla} ({cols_str})
        VALUES ({placeholders})
    '''
    return sql_execute_lastrowid(sql, valores)


def bd_update(tabla, columnas, valores, where, where_valores):
    """
    Actualiza registros en la tabla de forma segura.

    tabla: str - nombre de la tabla
    columnas: list[str] - columnas a actualizar
    valores: list - valores de columnas a actualizar
    where: str - cláusula WHERE (sin 'WHERE')
    where_valores: list - valores para la cláusula WHERE

    Retorna:
        int - número de filas afectadas

    filas_afectadas = bd_update(
        "usuario",
        ["correo", "edad"],
        ["nuevo@mail.com", 30],
        "id = %s",
        [usuario_id]
    )
    """
    set_clause = ", ".join([f"{col} = %s" for col in columnas])
    sql = f'''
        UPDATE {tabla}
        SET {set_clause}
        WHERE {where}
    '''
    all_values = valores + where_valores
    return sql_execute(sql, all_values)


def bd_delete(tabla, where, where_valores):
    """
    Elimina registros de forma segura.

    tabla: str - nombre de la tabla
    where: str - cláusula WHERE (sin 'WHERE')
    where_valores: list - valores para la cláusula WHERE

    Retorna:
        int - número de filas afectadas
    """
    sql = f'''
        DELETE FROM {tabla}
        WHERE {where}
    '''
    return sql_execute(sql, where_valores)


def bd_select(tabla, columnas, where=None, where_valores=None, extra=""):
    """
    Realiza un SELECT seguro y flexible.

    tabla: str - nombre de la tabla
    columnas: list[str] - columnas a obtener
    where: str | None - cláusula WHERE (sin 'WHERE')
    where_valores: list | None - valores para WHERE
    extra: str - texto adicional (ORDER BY, LIMIT, etc.)

    Retorna:
        list[dict] - resultados
    """
    cols_str = ", ".join(columnas)
    sql = f'''
        SELECT {cols_str}
        FROM {tabla}
    '''
    if where:
        sql += f" WHERE {where} "
    sql += f" {extra} "

    return sql_select_fetchall(sql, where_valores if where_valores else [])




def update_column_table_id(tabla, columna , valor , id):
    return bd_update(tabla, [columna], [valor], " id = %s ", [id])







def show_columns(table_name):
    sql= f'''
        SHOW COLUMNS FROM 
        {table_name}
    '''
    columnas = sql_select_fetchall(sql)
    
    return columnas


def show_primary_key(tabla):
    keys = []
    for row in show_columns(tabla):
        if row['Key'] == 'PRI':
            keys.append(row['Field'])

    if len(keys) == 1:
        return keys[0]
    else:
        return keys


def find_column_table(column_name, tabla):
    for row in show_columns(tabla):
        # print(row)
        if row['Field'] == column_name:
            return row
    return None


def delete_row_table( table_name , id ):
    sql = f'''
        delete from {table_name}
        where {show_primary_key(table_name)} = {id}
    '''
    sql_execute(sql)


def exists_column_Activo(tabla):
    row = find_column_table('activo' , tabla)
    # print(row)
    return row is not None


def unactive_row_table(table , pk):
    sql = f'''
        update {table} set 
        activo = NOT activo
        where {show_primary_key(table)} = {pk}
    '''
    sql_execute(sql)
    # return 0


def include_data_search(where = None, column_search = None , value_search = None):
    strSQL = ' '
    if where is not None and column_search is not None and value_search is not None:
        if where is True:
            strSQL += 'where'
        strSQL += f'''
            UPPER({column_search}) LIKE UPPER ('%{str(value_search)}%')
        '''
    return strSQL


def include_list_search(where = None, list_columns = [] , value_search = None):
    strSQL = ' '
    if where is not None and list_columns is not [] and value_search is not None:
        for column in list_columns:
            if list_columns[0] == column:
                strSQL += f'''{include_data_search(where,column,value_search)}'''
            else:
                strSQL += f''' or {include_data_search(False,column,value_search)}'''
    return strSQL



