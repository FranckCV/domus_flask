from bd import obtener_conexion
import base64

def obtener_datos_contenido_info():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    tip.id,
                    tip.nombre,
                    tip.faicon_cont,
                    tip.descripcion,
                    cont.id,
                    cont.titulo,
                    cont.cuerpo
                FROM tipo_contenido_info tip
                LEFT JOIN contenido_info cont on cont.TIPO_CONTENIDO_INFOid = tip.id
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos



def obtener_tipos_contenido():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    tip.id,
                    tip.nombre,
                    tip.descripcion,
                    tip.faicon_cont
                FROM tipo_contenido_info tip
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def obtener_datos_contenido():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    cont.id,
                    cont.titulo,
                    cont.cuerpo,
                    cont.TIPO_CONTENIDO_INFOid 
                FROM contenido_info cont
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos

