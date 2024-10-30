from bd import obtener_conexion
import base64

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


def obtener_listado_tipos_usuario():
    conexion = obtener_conexion()
    tipos_usuario = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                tip.id, 
                tip.tipo, 
                tip.descripcion,
                tip.imagen,
                count(usu.id),
                tip.disponibilidad
            FROM TIPO_USUARIO tip
            left join usuario usu on tip.id = usu.tipo_usuarioid
            group by tip.id
            ORDER BY tip.id ASC
        '''
        cursor.execute(sql)
        tipos_usuario = cursor.fetchall()

    elementos_tipos = []
    for tipo in tipos_usuario:
        tip_id , tip_nom , tip_desc , tip_img , cant , tip_disp = tipo

        if tip_img:
            img_base64 = base64.b64encode(tip_img).decode('utf-8')
            img_formato = f"data:image/png;base64,{img_base64}" 
        else:
            img_formato = ''
        elementos_tipos.append((tip_id , tip_nom , tip_desc , img_formato , cant , tip_disp))

    conexion.close()
    return elementos_tipos


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
