from controladores.bd import obtener_conexion
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
            FROM tipo_usuario
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
            FROM tipo_usuario tip
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
                descripcion,
                imagen,
                disponibilidad
            FROM tipo_usuario
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
        tipo_usuario = cursor.fetchone()

    elemento = None

    if tipo_usuario:
        usu_id, usu_tipo, usu_desc, usu_img, disp = tipo_usuario

        if usu_img:
            img_base64 = base64.b64encode(usu_img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo

        elemento = (usu_id, usu_tipo, usu_desc, img_url , disp)


    conexion.close()
    return elemento


def insertar_tipo_usuario(tipo, descripcion,img_user):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO tipo_usuario (tipo, descripcion, imagen,disponibilidad)
            VALUES (%s, %s, %s,1)
        '''
        cursor.execute(sql, (tipo, descripcion,img_user))
    conexion.commit()
    conexion.close()


def actualizar_tipo_usuario(id, tipo, descripcion , imagen , disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE tipo_usuario SET 
            tipo = %s, 
            descripcion = %s,
            imagen = %s ,
            disponibilidad = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (tipo, descripcion, imagen, disponibilidad ,id))
    conexion.commit()
    conexion.close()


def eliminar_tipo_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM tipo_usuario
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()


def obtener_img_tipo_usuario_por_id(id):
    conexion = obtener_conexion()
    tipo_usuario = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                imagen
            FROM tipo_usuario
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
        tipo_usuario = cursor.fetchone()

    conexion.close()
    return tipo_usuario


