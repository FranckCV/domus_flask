from bd import obtener_conexion

def insertar_tipo_novedad(nombre_tipo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO tipo_novedad (nomTipo) 
            VALUES (%s)
        '''
        cursor.execute(sql, (nombre_tipo,))
    conexion.commit()
    conexion.close()

def obtener_tipos_novedad():
    conexion = obtener_conexion()
    tipos_novedad = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT id, nomTipo 
            FROM tipo_novedad
            ORDER BY nomTipo
        '''
        cursor.execute(sql)
        tipos_novedad = cursor.fetchall()
    conexion.close()
    return tipos_novedad

def obtener_tipo_novedad_por_id(id):
    conexion = obtener_conexion()
    tipo_novedad = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT id, nomTipo 
            FROM tipo_novedad
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
        tipo_novedad = cursor.fetchone()
    conexion.close()
    return tipo_novedad

def actualizar_tipo_novedad(nombre_tipo, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE tipo_novedad
            SET nomTipo = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre_tipo, id))
    conexion.commit()
    conexion.close()

def eliminar_tipo_novedad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM tipo_novedad 
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()

def obtener_id_tipo_novedad(tipo_novedad):
    conexion = obtener_conexion()
    tipo_novedad_id = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM tipo_novedad WHERE nomTipo = %s", (tipo_novedad,))
        resultado = cursor.fetchone()
        if resultado:
            tipo_novedad_id = resultado[0]
    conexion.close()
    return tipo_novedad_id
