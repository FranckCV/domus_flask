from controladores.bd import obtener_conexion

def confirmarDatosAdm(username, password):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo, contrasenia FROM usuario WHERE correo = %s AND contrasenia = %s", (username, password))
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

def obtenerID(username):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (username,))  # Asegúrate de usar una tupla (username,)
        result = cursor.fetchone()
        if result:
            return result[0]  # Retorna solo el valor del tipo de usuario
        return None  # Si no se encuentra el usuario, devuelve None
    conexion.close()


