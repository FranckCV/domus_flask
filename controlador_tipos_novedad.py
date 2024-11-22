from controladores.bd import obtener_conexion

def insertar_tipo_novedad(nombre_tipo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO tipo_novedad (nomTipo , disponibilidad) 
            VALUES (%s,1)
        '''
        cursor.execute(sql, (nombre_tipo))
    conexion.commit()
    conexion.close()


def obtener_tipos_novedad():
    conexion = obtener_conexion()
    tipos_novedad = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nomTipo,
                disponibilidad
            FROM tipo_novedad
            ORDER BY id
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
            SELECT 
                id, 
                nomTipo,
                disponibilidad
            FROM tipo_novedad
            WHERE id = %s
        '''
        cursor.execute(sql, (id))
        tipo_novedad = cursor.fetchone()
    conexion.close()
    return tipo_novedad


def actualizar_tipo_novedad(nombre_tipo, disp, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE tipo_novedad
            SET nomTipo = %s ,
            disponibilidad = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre_tipo, disp , id))
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


def obtener_listado_tipos_novedad():
    conexion = obtener_conexion()
    tipos_novedad = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                tip.id, 
                tip.nomTipo,
                count(nov.id),
                tip.disponibilidad
            FROM tipo_novedad tip
            left join novedad nov on nov.tipo_novedadid = tip.id
            group by tip.id
        '''
        cursor.execute(sql)
        tipos_novedad = cursor.fetchall()
    conexion.close()
    return tipos_novedad



