from bd import obtener_conexion

def obtener_tipos_usuario():
    conexion = obtener_conexion()
    tipos_usuario = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                tipo, 
                descripcion
            FROM TIPO_USUARIO
            ORDER BY id ASC
        '''
        cursor.execute(sql)
        tipos_usuario = cursor.fetchall()

    conexion.close()
    return tipos_usuario


def obtener_tipo_usuario_por_id(id):
    conexion = obtener_conexion()
    tipo_usuario = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                tipo, 
                descripcion 
            FROM TIPO_USUARIO
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
        tipo_usuario = cursor.fetchone()

    conexion.close()
    return tipo_usuario


def insertar_tipo_usuario(tipo, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO TIPO_USUARIO (tipo, descripcion)
            VALUES (%s, %s)
        '''
        cursor.execute(sql, (tipo, descripcion))
    conexion.commit()
    conexion.close()


def actualizar_tipo_usuario(id, tipo, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE TIPO_USUARIO
            SET tipo = %s, descripcion = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (tipo, descripcion, id))
    conexion.commit()
    conexion.close()


def eliminar_tipo_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM TIPO_USUARIO
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()
