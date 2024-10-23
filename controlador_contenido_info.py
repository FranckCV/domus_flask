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

def obtener_listado_tipos_contenido():
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


def insertar_tipo_contenido_info(nombre , descripcion , faicon_cont):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tipo_contenido_info (nombre, descripcion , faicon_cont) VALUES (%s, %s,%s)", (nombre, descripcion , faicon_cont))
    conexion.commit()
    conexion.close()


def eliminar_tipo_contenido_info(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tipo_contenido_info WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_tipo_contenido_info_por_id(id):
    conexion = obtener_conexion()
    tipo = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre, descripcion , faicon_cont FROM tipo_contenido_info WHERE id = %s", (id))
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def actualizar_caracteristica(nombre , descripcion , faicon_cont , id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipo_contenido_info SET nombre = %s , descripcion = %s , faicon_cont = %s WHERE id = %s",
                       (nombre , descripcion , faicon_cont , id))
    conexion.commit()
    conexion.close()







def insertar_contenido_info(campo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO caracteristica (campo, disponibilidad) VALUES (%s, 1)", (campo))
    conexion.commit()
    conexion.close()


def eliminar_caracteristica(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM caracteristica WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_caracteristica_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT car.id, car.campo, car.disponibilidad FROM caracteristica car WHERE id = %s", (id))
        marca = cursor.fetchone()
    conexion.close()
    return marca


def actualizar_caracteristica(campo, disp, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE caracteristica SET campo = %s , disponibilidad = %s WHERE id =%s",
                       (campo, disp, id))
    conexion.commit()
    conexion.close()
