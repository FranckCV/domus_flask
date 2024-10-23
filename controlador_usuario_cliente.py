from bd import obtener_conexion
import base64


def insertar_usuario(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, tipo_usuario):
    conexion = obtener_conexion() 
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo,))
            result = cursor.fetchone()

            if result is not None:
                return 0  

            cursor.execute(
                "INSERT INTO usuario (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, TIPO_USUARIOid) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad, tipo_usuario)
            )

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

