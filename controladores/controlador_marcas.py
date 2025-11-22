from bd import obtener_conexion
import bd



def get_marcas_recientes(limit=4):
    sql = '''
        SELECT 
            ma.id, 
            ma.nombre, 
            ma.img_logo as ruta
        FROM 
            marca ma
        WHERE 
            ma.disponibilidad = 1 
        ORDER BY 
            ma.fecha_registro DESC
        LIMIT %s
        '''
    return bd.sql_select_fetchall(sql,(limit))







def obtener_marcas_menu(valor):
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nombre as marca, 
                img_logo 
            FROM marca
            where disponibilidad = 1 
            order by fecha_registro desc
            LIMIT '''+str(valor)
        cursor.execute(sql)
        marcas = cursor.fetchall()
    
    conexion.close()
    return marcas


def obtener_marcas_index(cant):
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.nombre, 
                ma.img_logo, 
                nov.id AS novedad_id, 
                nov.tipo_novedadid, 
                ino.img
            FROM 
                marca ma
            INNER JOIN 
                novedad nov ON nov.marcaid = ma.id
            INNER JOIN 
                img_novedad ino ON ino.novedadid = nov.id
            WHERE 
                ma.disponibilidad = 1 
                AND nov.disponibilidad = 1 
                AND ino.tipo_img_novedadid = 2
                AND   
                    (SELECT COUNT(*) 
                    FROM producto p 
                    WHERE p.marcaid = ma.id) > 4
            ORDER BY 
                ma.fecha_registro DESC, nov.fecha_registro DESC
            LIMIT 3;
            '''
        cursor.execute(sql)
        marcas = cursor.fetchall()
    
    conexion.close()
    return marcas


def obtener_marca_disponible_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.nombre, 
                ma.img_logo,
                ma.img_banner,
                ma.disponibilidad
            FROM marca ma
            where ma.disponibilidad = 1 and ma.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        marca = cursor.fetchone()
  
    conexion.close()
    return marca


def obtener_listado_marca_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.nombre, 
                ma.img_logo,
                ma.img_banner,
                ma.disponibilidad
            FROM marca ma
            where ma.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        marca = cursor.fetchone()

    marca_elemento = None

    conexion.close()
    return marca


def obtener_imgs_marca_disponible_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.img_logo,
                ma.img_banner
            FROM marca ma
            where ma.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        marca = cursor.fetchone()

    conexion.close()
    return marca


def obtener_todas_marcas_recientes():
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    id,
                    nombre, 
                    img_logo, 
                    img_banner,
                    date(fecha_registro),
                    disponibilidad
                FROM marca 
                where disponibilidad = 1
                order by fecha_registro desc
                '''
        cursor.execute(sql)
        marcas = cursor.fetchall()

    conexion.close()
    return marcas


def obtener_todas_marcas_alfabetico(orden):
    conexion = obtener_conexion()
    marcas = []

    if orden == 0 :
        ordenar = 'asc'
    elif orden == 1: 
        ordenar = 'desc'

    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    id,
                    nombre, 
                    img_logo, 
                    img_banner,
                    date(fecha_registro),
                    disponibilidad
                FROM marca 
                where disponibilidad = 1
                order by nombre '''+ordenar+'''
                '''
        cursor.execute(sql)
        marcas = cursor.fetchall()
  
    conexion.close()
    return marcas


def obtener_marcasXnombre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, marca, img_logo FROM marca order by marca")
        marcas = cursor.fetchall()
        
    conexion.close()
    return marcas


def insertar_marca(marca, logo, banner):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO marca(marca, img_logo,img_banner,disponibilidad) VALUES (%s, %s, %s,1)", (marca, logo,banner))
    conexion.commit()
    conexion.close()


def obtener_listado_marcas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    m.id,
                    m.nombre, 
                    m.img_logo, 
                    m.img_banner,
                    date(m.fecha_registro),
                    m.disponibilidad,
                    COUNT(DISTINCT p.id) AS cantidad_productos,
                    COUNT(DISTINCT n.id) AS cantidad_novedades
                FROM 
                    marca m
                LEFT JOIN 
                    producto p ON m.id = p.MARCAid
                LEFT JOIN 
                    novedad n ON m.id = n.MARCAid
                GROUP BY 
                    m.id, m.nombre, m.img_logo, m.img_banner, m.fecha_registro, m.disponibilidad
                order by m.id
                ''')
        marcas = cursor.fetchall()
      
    conexion.close()
    return marcas


def obtener_listado_marcas_nombre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    m.id,
                    m.nombre, 
                    m.img_logo, 
                    m.img_banner,
                    date(m.fecha_registro),
                    m.disponibilidad,
                    COUNT(DISTINCT p.id) AS cantidad_productos,
                    COUNT(DISTINCT n.id) AS cantidad_novedades
                FROM 
                    marca m
                LEFT JOIN 
                    producto p ON m.id = p.MARCAid
                LEFT JOIN 
                    novedad n ON m.id = n.MARCAid
                GROUP BY 
                    m.id, m.nombre, m.img_logo, m.img_banner, m.fecha_registro, m.disponibilidad
                order by m.nombre
                ''')
        marcas = cursor.fetchall()
        
    conexion.close()
    return marcas


def buscar_listado_marcas_nombre(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    m.id,
                    m.nombre, 
                    m.img_logo, 
                    m.img_banner,
                    date(m.fecha_registro),
                    m.disponibilidad,
                    COUNT(DISTINCT p.id) AS cantidad_productos,
                    COUNT(DISTINCT n.id) AS cantidad_novedades
                FROM 
                    marca m
                LEFT JOIN 
                    producto p ON m.id = p.MARCAid
                LEFT JOIN 
                    novedad n ON m.id = n.MARCAid
                WHERE UPPER(m.nombre) LIKE UPPER ('%'''+str(nombre)+'''%')
                GROUP BY 
                    m.id, m.nombre, m.img_logo, m.img_banner, m.fecha_registro, m.disponibilidad;
                ''')
        marcas = cursor.fetchall()
        
    conexion.close()
    return marcas


def eliminar_marca(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM marca WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_marca_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, marca,img_logo,img_banner,disponibilidad FROM marca WHERE id = %s", (id,))
        marca = cursor.fetchone()
    conexion.close()
    return marca


def actualizar_marca(marca,logo,banner, disponibilidad,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE marca SET marca = %s ,img_logo = %s,img_banner = %s,disponibilidad = %s WHERE id =%s",
                       (marca,logo,banner,disponibilidad,id))
    conexion.commit()
    conexion.close()


def obtener_id_marca(marca):
    conexion = obtener_conexion()
    marca_id = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM marca WHERE marca = %s", (marca,))
        resultado = cursor.fetchone()
        if resultado:
            marca_id = resultado[0]
    conexion.close()
    return marca_id


def marcas_para_novedad():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, marca FROM marca")
        marcas = cursor.fetchall()  # Esto debe devolver una lista de tuplas o diccionarios
    conexion.close()
    return marcas




################## PRUEBITA JWT ##############3

