from bd import obtener_conexion
import base64


def insertar_usuario(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad):
    conexion = obtener_conexion() 
    try:
        with conexion.cursor() as cursor:
            # Verificar si el correo ya está registrado
            cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo,))
            result = cursor.fetchone()

            if result is not None:
                return 0  

            cursor.execute(
                "INSERT INTO usuario (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad)
            )
            conexion.commit()  
            return 1
    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return -1
    finally:
        conexion.close()  # Asegurarse de cerrar la conexión

