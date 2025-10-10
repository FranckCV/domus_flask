from bd import obtener_conexion

# def confirmarDatosAdm(username, password):
#     conexion = obtener_conexion()
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute("SELECT correo, contrasenia FROM usuario WHERE correo = %s AND contrasenia = %s", (username, password))
#             result = cursor.fetchone()
#             if result:
#                 return True
#             return False
#     except Exception as e:
#         print(f"Error al consultar usuario: {e}")
#         return False
#     finally:
#         conexion.close()


# def obtenerTipoU(username):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT tipo_usuarioid FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
#         result = cursor.fetchone()
#         if result:
#             return result[0]  # Retorna solo el valor del tipo de usuario
#         return None  # Si no se encuentra el usuario, devuelve None
#     conexion.close()

# def obtenerNombresC(username):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT CONCAT(nombres, ' ', apellidos) AS nombre_completo FROM usuario where correo = %s", (username))
#         result = cursor.fetchone()
#         return result
#     conexion.close()

# def registrarTrabajador(nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, tipo_usuarioid):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#         INSERT INTO usuario (nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento,
#                              telefono, correo, contrasenia, disponibilidad, tipo_usuarioid)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         '''
#         cursor.execute(sql, (nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento,
#                              telefono, correo, contrasenia, disponibilidad, tipo_usuarioid))
#     conexion.commit()
#     conexion.close()

# def cambiarContraseniaT(id, contrasenia):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#         UPDATE usuario SET contrasenia = %s WHERE id = %s
#         '''
#         cursor.execute(sql, (contrasenia, id))
#     conexion.commit()
#     conexion.close()

# def obtenerContrasenia(username):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT contrasenia FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
#         result = cursor.fetchone()
#         if result:
#             return result[0]  # Retorna solo el valor del tipo de usuario
#         return None  # Si no se encuentra el usuario, devuelve None
#     conexion.close()

# def obtenerID(username):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT id FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
#         result = cursor.fetchone()
#         if result:
#             return result[0]  # Retorna solo el valor del tipo de usuario
#         return None  # Si no se encuentra el usuario, devuelve None
#     conexion.close()


def obtener_usuario_por_id(user_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = "SELECT id, nombres, contrasenia, correo FROM usuario WHERE id = %s"
            cursor.execute(query, (user_id,))
            resultado = cursor.fetchone()

            if resultado:
                # Transforma la tupla en un diccionario
                usuario = {
                    'id': resultado[0],
                    'nombres': resultado[1],
                    'contrasenia': resultado[2],
                    'correo': resultado[3]
                }
                return usuario
            return None
    finally:
        conexion.close()

def obtener_usuario_por_id2(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                SELECT
                    id,
                    CONCAT(nombres, ' ', apellidos) AS nombre_completo,
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
        print(f"Error al obtener el usuario admin por ID: {e}")
        return None
    finally:
        conexion.close()


def cambiar_contrasenia(user_id, nueva_contrasenia):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = "UPDATE usuario SET contrasenia = %s WHERE id = %s"
            cursor.execute(query, (nueva_contrasenia, user_id))
        conexion.commit()
    finally:
        conexion.close()

def confirmarDatosAdm(username, password):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo, contrasenia FROM usuario WHERE correo = %s AND contrasenia = %s and tipo_usuarioid in (1,2)", (username, password))
            result = cursor.fetchone()
            if result:
                return True
            return False
    except Exception as e:
        print(f"Error al consultar usuario: {e}")
        return False
    finally:
        conexion.close()


def obtenerTipoU(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT tipo_usuarioid FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()

def obtenerNombresC(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT CONCAT(nombres, ' ', apellidos) AS nombre_completo FROM usuario where correo = %s", (username))
        result = cursor.fetchone()
        return result
    conexion.close()

def registrarTrabajador(nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento, telefono, correo, contrasenia, disponibilidad, tipo_usuarioid):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
        INSERT INTO usuario (nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento,
                             telefono, correo, contrasenia, disponibilidad, tipo_usuarioid)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombres, apellidos, doc_identidad, img_usuario, genero, fecha_nacimiento,
                             telefono, correo, contrasenia, disponibilidad, tipo_usuarioid))
    conexion.commit()
    conexion.close()

def cambiarContraseniaT(id, contrasenia):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
        UPDATE usuario SET contrasenia = %s WHERE id = %s
        '''
        cursor.execute(sql, (contrasenia, id))
    conexion.commit()
    conexion.close()

def obtenerContrasenia(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT contrasenia FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()

def obtenerdoc(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT doc_identidad FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()

def obtenergenero(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT genero FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()

def obtenerfecha_nacimiento(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fecha_nacimiento FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()

def obtenertelefono(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT telefono FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()


def obtenerID(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()

def obtenerDataU(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT doc_identidad,genero,fecha_nacimiento,telefono,correo FROM usuario WHERE correo = %s", (username,))
        results = cursor.fetchall()  # Devuelve una lista de tuplas
        return results if results else []  # Si no hay resultados, devuelve una lista vacía
    conexion.close()

