from bd import obtener_conexion
import base64


def insertar_usuario(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, tipo_usuario):
    conexion = obtener_conexion() 
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo,))
            result = cursor.fetchone()

            if result is not None:
                return 0  # retornar un 0 pa decirle que ya existe que mejor recupere su contra XD

            cursor.execute(
                "INSERT INTO usuario (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, TIPO_USUARIOid) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, tipo_usuario)
            )

            usuario_id = cursor.lastrowid # pa mandarle mensaje de exito por pantalla maybe

            conexion.commit()  
            return 1  
    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return -1  
    finally:
        conexion.close() 


def confirmarDatos(correo, contraseña):
    conexion= obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo,contraseña FROM usuario WHERE correo = %s , contraseña=%s", (correo,contraseña,))
            result = cursor.fetchone()

            if result is not None:
                return 0  
            conexion.commit()  
            return 1
    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return -1    


########## aqui haré cositas jasdjajsdas ####

def obtener_usuarios_clientes():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                SELECT 
                    id, 
                    nombres, 
                    apellidos, 
                    doc_identidad, 
                    img_usuario, 
                    genero, 
                    fecha_nacimiento, 
                    telefono, 
                    correo, 
                    disponibilidad
                FROM USUARIO
                WHERE TIPO_USUARIOid = 3
            '''
            cursor.execute(sql)
            usuarios = cursor.fetchall() 

            return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        conexion.close()


def obtener_listado_usuarios_clientes():
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
                    count(ped.id)
                FROM USUARIO usu
                LEFT JOIN pedido ped on ped.usuarioid = usu.id
                WHERE TIPO_USUARIOid = 3
                GROUP by usu.id
            '''
            cursor.execute(sql)
            usuarios = cursor.fetchall() 

            return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        conexion.close()


def buscar_listado_usuarios_clientes_nombre(nombre):
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
                    count(ped.id)
                FROM USUARIO usu
                LEFT JOIN pedido ped on ped.usuarioid = usu.id
                WHERE TIPO_USUARIOid = 3 and 
                UPPER(CONCAT(usu.nombres, ' ' , usu.apellidos)) LIKE UPPER ('%'''+nombre+'''%')
                GROUP by usu.id
            '''
            cursor.execute(sql)
            usuarios = cursor.fetchall() 

            return usuarios
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        conexion.close()



def obtener_usuario_cliente_por_id(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                SELECT 
                    id, 
                    nombres, 
                    apellidos, 
                    doc_identidad, 
                    img_usuario, 
                    genero, 
                    fecha_nacimiento, 
                    telefono, 
                    correo, 
                    disponibilidad
                FROM USUARIO
                WHERE id = %s AND TIPO_USUARIOid = 3
            '''
            cursor.execute(sql, (id,))
            usuario = cursor.fetchone()

            return usuario
    except Exception as e:
        print(f"Error al obtener el usuario cliente por ID: {e}")
        return None
    finally:
        conexion.close()


def actualizar_usuario_cliente(id, nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, disponibilidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                UPDATE USUARIO 
                SET 
                    nombres = %s, 
                    apellidos = %s, 
                    doc_identidad = %s, 
                    genero = %s, 
                    fecha_nacimiento = %s, 
                    telefono = %s, 
                    correo = %s, 
                    disponibilidad = %s
                WHERE id = %s AND TIPO_USUARIOid = 3
            '''
            cursor.execute(sql, (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, disponibilidad, id))
            conexion.commit()

            return True
    except Exception as e:
        print(f"Error al actualizar el usuario cliente: {e}")
        return False
    finally:
        conexion.close()


def eliminar_usuario_cliente(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            
            sql = "DELETE FROM USUARIO WHERE id = %s AND TIPO_USUARIOid = 3"
            cursor.execute(sql, (id,))
            conexion.commit()

            return True
    except Exception as e:
        print(f"Error al eliminar el usuario cliente: {e}")
        return False
    finally:
        conexion.close()
