from bd import obtener_conexion
tabla = 'motivo_comentario'

def obtener_motivos_disponibles():
    conexion = obtener_conexion()
    motivos = []
    with conexion.cursor() as cursor:
        sql = 'SELECT id, motivo, disponibilidad FROM ' + tabla + ' WHERE disponibilidad = 1'
        cursor.execute(sql)
        motivos = cursor.fetchall()
    conexion.close()
    return motivos

def obtener_motivo_por_id(id):
    conexion = obtener_conexion()
    motivo = None
    with conexion.cursor() as cursor:
        sql = 'SELECT id, motivo, disponibilidad FROM ' + tabla + ' WHERE id = %s'
        cursor.execute(sql, (id,))
        motivo = cursor.fetchone()
    conexion.close()
    return motivo

def insertar_motivo(motivo, disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO " + tabla + "(motivo, disponibilidad) VALUES (%s, %s)", (motivo, disponibilidad))
    conexion.commit()
    conexion.close()

def obtener_motivos():
    conexion = obtener_conexion()
    motivos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, motivo, disponibilidad FROM " + tabla)
        motivos = cursor.fetchall()
    conexion.close()
    return motivos

def eliminar_motivo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM " + tabla + " WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def actualizar_motivo(motivo, disponibilidad, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE " + tabla + " SET motivo = %s, disponibilidad = %s WHERE id = %s", (motivo, disponibilidad, id))
    conexion.commit()
    conexion.close()


def obtener_listado_motivos():
    conexion = obtener_conexion()
    motivos = []
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            mot.id, 
                            mot.motivo, 
                            disponibilidad,
                            count(com.id)
                       FROM motivo_comentario mot
                       Left join comentario com on com.motivo_comentarioid = mot.id
                       group by mot.id
                       ''')
        motivos = cursor.fetchall()
    conexion.close()
    return motivos


