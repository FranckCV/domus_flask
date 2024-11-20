from bd import obtener_conexion
import base64
tabla = 'usuario'

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        sql = """
        SELECT id, nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, TIPO_USUARIOid
        FROM """ + tabla + """ WHERE id = %s
        """
        cursor.execute(sql, (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario


def insertar_usuario(nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Si hay imagen, insertar con ella
        if img_usuario is not None:
            cursor.execute("INSERT INTO " + tabla + "(nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, TIPO_USUARIOid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 2)", 
                           (nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad))
        else:
            cursor.execute("INSERT INTO " + tabla + "(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, TIPO_USUARIOid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 2)", 
                           (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad))
    conexion.commit()
    conexion.close()


def actualizar_usuario(nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        if img_usuario is not None:
            cursor.execute("UPDATE " + tabla + " SET nombres = %s, apellidos = %s, doc_identidad = %s, img_usuario = %s, genero = %s, fecha_nacimiento = %s, telefono = %s, correo = %s, contraseña = %s, disponibilidad = %s WHERE id = %s", 
                           (nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, id))
        else:
            cursor.execute("UPDATE " + tabla + " SET nombres = %s, apellidos = %s, doc_identidad = %s, genero = %s, fecha_nacimiento = %s, telefono = %s, correo = %s, contraseña = %s, disponibilidad = %s WHERE id = %s", 
                           (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, id))
    conexion.commit()
    conexion.close()


def obtener_usuarios_emp():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        sql = """
        SELECT u.id, u.nombres, u.apellidos, u.doc_identidad, u.img_usuario, u.genero, u.fecha_nacimiento, u.telefono, u.correo, u.contraseña, u.disponibilidad, tu.tipo
        FROM usuario u
        JOIN tipo_usuario tu ON u.TIPO_USUARIOid = tu.id WHERE TIPO_USUARIOid = 2
        """
        cursor.execute(sql)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM " + tabla + " WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def verificar_correo_existente(correo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
        resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None  # Retorna True si el correo ya existe


def obtener_listado_usuarios_empleados():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    usu.id, 
                    usu.nombres, 
                    usu.apellidos, 
                    usu.doc_identidad, 
                    usu.img_usuario, 
                    usu.genero, 
                    usu.fecha_nacimiento, 
                    usu.telefono, 
                    usu.correo,
                    usu.disponibilidad,
                    usu.contraseña,
                    usu.fecha_registro
                FROM USUARIO usu
                WHERE usu.TIPO_USUARIOid = 2
        '''
        cursor.execute(sql)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def buscar_listado_usuarios_empleados_nombre(nombre):
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    usu.id, 
                    usu.nombres, 
                    usu.apellidos, 
                    usu.doc_identidad, 
                    usu.img_usuario, 
                    usu.genero, 
                    usu.fecha_nacimiento, 
                    usu.telefono, 
                    usu.correo,
                    usu.disponibilidad,
                    usu.contraseña
                FROM USUARIO usu
                WHERE UPPER(CONCAT(usu.nombres, ' ' , usu.apellidos)) LIKE UPPER ('%'''+str(nombre)+'''%') and usu.TIPO_USUARIOid = 2
        '''
        cursor.execute(sql)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def obtener_listado_imagenes_usuario_empleado():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                usu.id,
                usu.img_usuario
            FROM USUARIO usu
            WHERE usu.TIPO_USUARIOid = 2
        '''
        cursor.execute(sql)
        usuarios = cursor.fetchall()

    elemento = []

    for user in usuarios:
        usu_id , img_usu = user
        if img_usu:
            img_base64 = base64.b64encode(img_usu).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""
        elemento.append((usu_id , img_url))

    conexion.close()
    return elemento


def ver_info_usuario_empleado(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                SELECT 
                    usu.id, 
                    usu.nombres, 
                    usu.apellidos, 
                    usu.doc_identidad, 
                    usu.img_usuario, 
                    usu.genero, 
                    usu.fecha_nacimiento, 
                    usu.telefono, 
                    usu.correo, 
                    usu.disponibilidad,
                    usu.contraseña,
                    usu.fecha_registro,
                    count(com.id),
                    usu.contraseña
                FROM USUARIO usu
                LEFT JOIN pedido ped on ped.usuarioid = usu.id
                LEFT JOIN comentario com on com.usuarioid = usu.id
                WHERE TIPO_USUARIOid = 2 and usu.id = '''+str(id)+'''
                GROUP by usu.id
            '''
            cursor.execute(sql)
            usuarios = cursor.fetchone() 

            return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        conexion.close()


def obtener_imagen_usuario_empleado_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                usu.id,
                usu.img_usuario
            FROM USUARIO usu
            WHERE TIPO_USUARIOid = 2 and usu.id = '''+str(id)+'''
        '''
        cursor.execute(sql)
        usuario = cursor.fetchone()

    elemento = None

    if usuario:
        usu_id , img_usu = usuario
        if img_usu:
            img_base64 = base64.b64encode(img_usu).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = None
    
        elemento = (usu_id , img_url)
        
    conexion.close()
    return elemento


