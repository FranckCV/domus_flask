from bd import obtener_conexion

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


def buscar_datos_contenido_info_titulo(titulo):
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
                        WHERE UPPER(cont.titulo) LIKE UPPER ('%'''+str(titulo)+'''%')
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
                            tip.faicon_cont,
                            count(cont.id),
                            tip.disponibilidad
                        FROM tipo_contenido_info tip
                        left join contenido_info cont on cont.tipo_contenido_infoid = tip.id
                        group by tip.id
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def buscar_listado_tipos_contenido_nombre(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                            SELECT 
                                tip.id,
                                tip.nombre,
                                tip.descripcion,
                                tip.faicon_cont,
                                count(cont.id),
                                tip.disponibilidad
                            FROM tipo_contenido_info tip
                            left join contenido_info cont on cont.tipo_contenido_infoid = tip.id
                            WHERE UPPER(tip.nombre) LIKE UPPER ('%'''+str(nombre)+'''%')
                            group by tip.id
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


def obtener_datos_contenido_por_tipo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            cont.id,
                            cont.titulo,
                            cont.cuerpo,
                            cont.TIPO_CONTENIDO_INFOid 
                        FROM contenido_info cont
                        WHERE TIPO_CONTENIDO_INFOid = '''+str(id)+'''
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def insertar_tipo_contenido_info(nombre , descripcion , faicon_cont):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tipo_contenido_info (nombre, descripcion , faicon_cont, disponibilidad) VALUES (%s, %s,%s,1)", (nombre, descripcion , faicon_cont))
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
        cursor.execute("SELECT id, nombre, faicon_cont ,descripcion,disponibilidad FROM tipo_contenido_info WHERE id = %s", (id))
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def actualizar_tipo_contenido_info_por_id(nombre , descripcion , faicon_cont , disponibilidad , id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipo_contenido_info SET nombre = %s , descripcion = %s , faicon_cont = %s , disponibilidad = %s WHERE id = %s",
                       (nombre , descripcion , faicon_cont , disponibilidad,id))
    conexion.commit()
    conexion.close()


def insertar_contenido_info(titulo , cuerpo , tipo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO contenido_info (titulo, cuerpo , tipo_contenido_infoid) VALUES (%s, %s,%s)", (titulo , cuerpo , tipo))
    conexion.commit()
    conexion.close()


def eliminar_contenido_info(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM contenido_info WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_contenido_info_por_id(id):
    conexion = obtener_conexion()
    tipo = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, titulo, cuerpo , tipo_contenido_infoid FROM contenido_info WHERE id = %s", (id))
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def actualizar_contenido_info_por_id(titulo , cuerpo , tipo , id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE contenido_info SET titulo = %s , cuerpo = %s , tipo_contenido_infoid = %s WHERE id = %s",
                       (titulo , cuerpo , tipo , id))
    conexion.commit()
    conexion.close()
