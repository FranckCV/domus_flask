from bd import obtener_conexion
tabla = 'comentario'

def obtener_comentarios_disponibles():
    conexion = obtener_conexion()
    comentarios = []
    with conexion.cursor() as cursor:
        sql = 'SELECT id, nombres, apellidos, email, celular, mensaje, fecha_registro, estado, MOTIVO_COMENTARIOid, USUARIOid FROM ' + tabla + ' WHERE estado = 1'
        cursor.execute(sql)
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios


def obtener_comentario_por_id(id):
    conexion = obtener_conexion()
    comentario = None
    with conexion.cursor() as cursor:
        sql = 'SELECT id, nombres, apellidos, email, celular, mensaje, fecha_registro, estado, MOTIVO_COMENTARIOid, USUARIOid FROM ' + tabla + ' WHERE id = %s'
        cursor.execute(sql, (id,))
        comentario = cursor.fetchone()
    conexion.close()
    return comentario


def insertar_comentario(nombres, apellidos, email, celular, mensaje, estado, MOTIVO_COMENTARIOid, USUARIOid):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Usar CURDATE() para guardar solo la fecha actual
        cursor.execute("INSERT INTO " + tabla + "(nombres, apellidos, email, celular, mensaje, fecha_registro, estado, MOTIVO_COMENTARIOid, USUARIOid) VALUES (%s, %s, %s, %s, %s, CURDATE(), %s, %s, %s)", 
                       (nombres, apellidos, email, celular, mensaje, estado, MOTIVO_COMENTARIOid, USUARIOid))
    conexion.commit()
    conexion.close()


def obtener_comentarios():
    conexion = obtener_conexion()
    comentarios = []
    with conexion.cursor() as cursor:
        
        sql = """
        SELECT 
            c.id, c.nombres, c.apellidos, c.email, c.celular, c.mensaje, c.fecha_registro, c.estado, 
            mc.motivo
        FROM comentario c
        JOIN motivo_comentario mc ON c.MOTIVO_COMENTARIOid = mc.id
        """
        cursor.execute(sql)
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios


def obtener_listado_comentarios():
    conexion = obtener_conexion()
    comentarios = []
    with conexion.cursor() as cursor:
        
        sql = '''
            SELECT 
                c.id, 
                c.nombres, 
                c.apellidos, 
                c.email, 
                c.celular, 
                c.mensaje, 
                c.fecha_registro, 
                c.estado, 
                mc.motivo,
                mc.id
            FROM comentario c
            left JOIN motivo_comentario mc ON c.MOTIVO_COMENTARIOid = mc.id
            order by c.estado asc, c.fecha_registro desc
        '''
        cursor.execute(sql)
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios


def buscar_listado_comentarios_mensaje(mensaje):
    conexion = obtener_conexion()
    comentarios = []
    with conexion.cursor() as cursor:
        
        sql = '''
            SELECT 
                c.id, 
                c.nombres, 
                c.apellidos, 
                c.email, 
                c.celular, 
                c.mensaje, 
                c.fecha_registro, 
                c.estado, 
                mc.motivo,
                mc.id
            FROM comentario c
            left JOIN motivo_comentario mc ON c.MOTIVO_COMENTARIOid = mc.id
            WHERE UPPER(c.mensaje) LIKE UPPER ('%'''+str(mensaje)+'''%')
            order by c.estado asc, c.fecha_registro desc
        '''
        cursor.execute(sql)
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios


def buscar_listado_comentarios_nombre(nombre):
    conexion = obtener_conexion()
    comentarios = []
    with conexion.cursor() as cursor:
        
        sql = '''
            SELECT 
                c.id, 
                c.nombres, 
                c.apellidos, 
                c.email, 
                c.celular, 
                c.mensaje, 
                c.fecha_registro, 
                c.estado, 
                mc.motivo,
                mc.id
            FROM comentario c
            left JOIN motivo_comentario mc ON c.MOTIVO_COMENTARIOid = mc.id
            WHERE UPPER(CONCAT(c.nombres, ' ' , c.apellidos)) LIKE UPPER ('%'''+nombre+'''%')
            order by c.estado asc, c.fecha_registro desc;
        '''
        cursor.execute(sql)
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios


def buscar_listado_comentarios_palabra(palabra):
    conexion = obtener_conexion()
    comentarios = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                c.id, 
                c.nombres, 
                c.apellidos, 
                c.email, 
                c.celular, 
                c.mensaje, 
                c.fecha_registro, 
                c.estado, 
                mc.motivo,
                mc.id
            FROM comentario c
            left JOIN motivo_comentario mc ON c.MOTIVO_COMENTARIOid = mc.id
            WHERE 
                (UPPER(CONCAT(c.nombres, ' ' , c.apellidos)) LIKE UPPER ('%'''+palabra+'''%'))
                or (UPPER(c.mensaje) LIKE UPPER ('%'''+str(palabra)+'''%'))
            order by c.estado asc, c.fecha_registro desc;
        '''
        cursor.execute(sql)
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios



def eliminar_comentario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM " + tabla + " WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def estado_comentario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE " + tabla + " SET estado = 1 WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def actualizar_comentario(nombres, apellidos, email, celular, mensaje, estado, MOTIVO_COMENTARIOid, USUARIOid, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE " + tabla + " SET nombres = %s, apellidos = %s, email = %s, celular = %s, mensaje = %s, estado = %s, MOTIVO_COMENTARIOid = %s, USUARIOid = %s WHERE id = %s", 
                       (nombres, apellidos, email, celular, mensaje, estado, MOTIVO_COMENTARIOid, USUARIOid, id))
    conexion.commit()
    conexion.close()
