from bd import obtener_conexion

def registrar_bitacora(usuarioid):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO bitacora (usuarioid) VALUES (%s);", (usuarioid,))
        id_bitacora = cursor.lastrowid

    conexion.commit()
    conexion.close()
    return id_bitacora
