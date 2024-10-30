from bd import obtener_conexion
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
                    usu.contraseña
                FROM USUARIO usu
                WHERE usu.TIPO_USUARIOid = 2
        '''
        cursor.execute(sql)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


