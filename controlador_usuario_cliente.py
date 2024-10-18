from bd import obtener_conexion
import base64

def insertar_usuario(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad):
    conexion = obtener_conexion()  
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuario(nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, contraseña, disponibilidad)
        )
    conexion.commit() 
    conexion.close()  
