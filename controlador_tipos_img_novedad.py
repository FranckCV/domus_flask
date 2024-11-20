from bd import obtener_conexion

def obtener_tipos_img_novedad():
    conexion = obtener_conexion()
    tipos_img = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                tipo, 
                disponibilidad 
            FROM TIPO_IMG_NOVEDAD
            ORDER BY id asc
        '''
        cursor.execute(sql)
        tipos_img = cursor.fetchall()

    conexion.close()
    return tipos_img


def obtener_listado_tipos_img_novedad():
    conexion = obtener_conexion()
    tipos_img = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                tin.id, 
                tin.tipo, 
                tin.disponibilidad,
                count(img.id)
            FROM TIPO_IMG_NOVEDAD tin
            left join img_novedad img on img.tipo_img_novedadid = tin.id
            group by tin.id
        '''
        cursor.execute(sql)
        tipos_img = cursor.fetchall()

    conexion.close()
    return tipos_img


def obtener_tipo_img_novedad_por_id(id):
    conexion = obtener_conexion()
    tipo_img = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                tipo, 
                disponibilidad 
            FROM TIPO_IMG_NOVEDAD
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
        tipo_img = cursor.fetchone()

    conexion.close()
    return tipo_img


def insertar_tipo_img_novedad(tipo, disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO TIPO_IMG_NOVEDAD (tipo, disponibilidad)
            VALUES (%s, %s)
        '''
        cursor.execute(sql, (tipo, disponibilidad))
    conexion.commit()
    conexion.close()


def actualizar_tipo_img_novedad(id, tipo, disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE TIPO_IMG_NOVEDAD
            SET tipo = %s, disponibilidad = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (tipo, disponibilidad, id))
    conexion.commit()
    conexion.close()


def eliminar_tipo_img_novedad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM TIPO_IMG_NOVEDAD
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()


def obtener_tipos_img_novedad_disponibles():
    conexion = obtener_conexion()
    tipos_img = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                tipo 
            FROM TIPO_IMG_NOVEDAD
            WHERE disponibilidad = 1
            ORDER BY id DESC
        '''
        cursor.execute(sql)
        tipos_img = cursor.fetchall()

    conexion.close()
    return tipos_img






