from bd import obtener_conexion
import base64
import bd
from utils import encstringsha256

def get_usuario_id(id):
    sql = '''
        SELECT 
            u.id, 
            u.nombres, 
            u.apellidos, 
            u.doc_identidad, 
            u.img_usuario, 
            CASE 
                WHEN u.genero = 1 THEN 'Masculino'
                ELSE 'Femenino'
            END AS genero,
            u.fecha_nacimiento, 
            u.telefono, 
            u.correo,
            u.disponibilidad,
            u.tipo_usuarioid
        FROM usuario u
        WHERE u.id = %s AND u.tipo_usuarioid = 3
    '''
    return bd.sql_select_fetchone(sql,(id))


def change_password(usuario_id, contrasenia_actual, contrasenia_nueva):
    try:
        sql_s = '''
            SELECT 
                contrasenia as c
            FROM usuario
            where id = %s
        '''
        c_a = bd.sql_select_fetchone(sql_s, (usuario_id))['c']

        if c_a == encstringsha256(contrasenia_actual):
            sql_u = '''
                UPDATE usuario
                SET contrasenia = %s
                WHERE id = %s
            '''
            bd.sql_execute(sql_u, (encstringsha256(contrasenia_nueva), usuario_id))
            return 1
        return 0
    except Exception as e:
        return -1
        

def update_perfil(usuario_id, nombres, apellidos , doc_identidad , genero , telefono , correo):
    try:
        sql_u = '''
            UPDATE usuario SET 
            nombres = %s ,
            apellidos = %s ,
            doc_identidad = %s ,
            genero = %s,
            telefono = %s ,
            correo = %s 
            WHERE id = %s
        '''
        bd.sql_execute(sql_u, (nombres, apellidos , doc_identidad , genero , telefono , correo,usuario_id))
        return 1
    except Exception as e:
        return -1
        
    
def get_usuario_correo(correo):
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
            contrasenia, 
            disponibilidad, 
            fecha_registro, 
            tipo_usuarioid, 
            registro_auditoria 
        FROM usuario
        WHERE correo = %s 
    '''
    return bd.sql_select_fetchone(sql,(correo))


def get_usuario_id(id):
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
            contrasenia, 
            disponibilidad, 
            fecha_registro, 
            tipo_usuarioid, 
            registro_auditoria 
        FROM usuario
        WHERE id = %s 
    '''
    return bd.sql_select_fetchone(sql,(id))
  

def register_usuario_cliente(nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia):
    sql_s = '''
        SELECT correo FROM usuario WHERE correo = %s
    '''
    existe_correo = bd.sql_select_fetchone(sql_s,(correo)) is not None
    enc_c = encstringsha256(contrasenia)
    if not existe_correo:
        sql_i = '''
            INSERT INTO usuario (nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia, disponibilidad, TIPO_USUARIOid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1, 3)
        '''
        return bd.sql_execute_lastrowid(sql_i,(nombres, apellidos, doc_identidad, genero, telefono, correo, enc_c))
    return 0


def insertar_usuario(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, tipo_usuario):
    conexion = obtener_conexion() 
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo,))
            result = cursor.fetchone()

            if result is not None:
                return 0  # retornar un 0 pa decirle que ya existe que mejor recupere su contra XD

            cursor.execute(
                "INSERT INTO usuario (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, TIPO_USUARIOid) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, tipo_usuario)
            )

            usuario_id = cursor.lastrowid # pa mandarle mensaje de exito por pantalla maybe

            conexion.commit()  
            return 1  
    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return -1  
    finally:
        conexion.close()


def insertar_usuario_api(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, tipo_usuario):
    conexion = obtener_conexion() 
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo,))
            result = cursor.fetchone()

            if result is not None:
                return 0  # retornar un 0 pa decirle que ya existe que mejor recupere su contra XD

            cursor.execute(
                "INSERT INTO usuario (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, TIPO_USUARIOid) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, tipo_usuario)
            )

            usuario_id = cursor.lastrowid # pa mandarle mensaje de exito por pantalla maybe

            conexion.commit()  
            return usuario_id  
    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return -1  
    finally:
        conexion.close() 


def confirmarDatos(correo, contrasenia):
    conexion= obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo,contrasenia FROM usuario WHERE correo = %s , contrasenia=%s", (correo,contrasenia,))
            result = cursor.fetchone()

            if result is not None:
                return 0  
            conexion.commit()  
            return 1
    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return -1    


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
                FROM usuario
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
                    count(ped.id),
                    date(usu.fecha_registro),
                    count(com.id)
                FROM usuario usu
                LEFT JOIN pedido ped on ped.usuarioid = usu.id
                LEFT JOIN comentario com on com.usuarioid = usu.id
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
                    count(ped.id),
                    date(usu.fecha_registro),
                    count(com.id)
                FROM usuario usu
                LEFT JOIN pedido ped on ped.usuarioid = usu.id
                LEFT JOIN comentario com on com.usuarioid = usu.id
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


def obtener_usuario_cliente_por_id2(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                SELECT 
                    id,
                    correo,
                    contrasenia,
                    TIPO_USUARIOid
                FROM usuario
                WHERE id = %s
            '''
            cursor.execute(sql, (id,))
            usuario = cursor.fetchone()

            return usuario
    except Exception as e:
        print(f"Error al obtener el usuario cliente por ID: {e}")
        return None
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
                    contrasenia, 
                    disponibilidad,
                    TIPO_USUARIOid
                FROM usuario
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


def insertar_imagen(id, img):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                UPDATE usuario
                SET img_usuario = %s
                WHERE id = %s AND TIPO_USUARIOid = 3
            '''
            cursor.execute(sql, (img, id,))
            conexion.commit()
    except Exception as e:
        print(f"Error al actualizar la imagen del usuario: {e}")
    finally:
        conexion.close()
   
        
def obtener_usuario_cliente_por_email(email):
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = '''
                    SELECT 
                        id,
                        correo,
                        contrasenia,
                        TIPO_USUARIOid
                    FROM usuario
                    WHERE correo = %s 
                '''
                cursor.execute(sql, (email,))
                usuario = cursor.fetchone()
                return usuario
        except Exception as e:
            print(f"Error al obtener el usuario cliente por ID: {e}")
            return None
        finally:
            conexion.close()    


def actualizar_usuario_cliente(id, nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, disponibilidad , imagen):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                UPDATE usuario 
                SET 
                    nombres = %s, 
                    apellidos = %s, 
                    doc_identidad = %s, 
                    genero = %s, 
                    fecha_nacimiento = %s, 
                    telefono = %s, 
                    correo = %s, 
                    disponibilidad = %s,
                    img_usuario = %s
                WHERE id = %s AND TIPO_USUARIOid = 3
            '''
            cursor.execute(sql, (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, disponibilidad, imagen,id))
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
            
            sql = "DELETE FROM usuario WHERE id = %s AND TIPO_USUARIOid = 3"
            cursor.execute(sql, (id,))
            conexion.commit()

            return True
    except Exception as e:
        print(f"Error al eliminar el usuario cliente: {e}")
        return False
    finally:
        conexion.close()


def obtener_listado_imagenes_usuario_cliente():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                usu.id,
                usu.img_usuario
            FROM usuario usu
            WHERE usu.TIPO_USUARIOid = 3
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


def ver_info_usuario_cliente(id):
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
                    count(ped.id),
                    date(usu.fecha_registro),
                    count(com.id)
                FROM usuario usu
                LEFT JOIN pedido ped on ped.usuarioid = usu.id
                LEFT JOIN comentario com on com.usuarioid = usu.id
                WHERE TIPO_USUARIOid = 3 and usu.id = '''+str(id)+'''
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


def obtener_imagen_usuario_cliente_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                usu.id,
                usu.img_usuario
            FROM usuario usu
            WHERE TIPO_USUARIOid = 3 and usu.id = %s
        '''
        cursor.execute(sql,(id,))
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

def cambiar_contrasenia(usuario_id, nueva_contraseña):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                UPDATE usuario
                SET contrasenia = %s
                WHERE id = %s
            ''', (nueva_contraseña, usuario_id))
            conexion.commit()
    except Exception as e:
        print("Error al actualizar la contraseña:", e)
        conexion.rollback()
    finally:
        conexion.close()


