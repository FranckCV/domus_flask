from bd import obtener_conexion
import base64
import controlador_productos
tabla = 'marca'

def obtener_marcas_menu(valor):
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                marca, 
                img_logo 
            FROM '''+tabla+''' 
            where disponibilidad = 1 
            order by fecha_registro desc
            LIMIT '''+str(valor)
        cursor.execute(sql)
        marcas = cursor.fetchall()
    
    marcas_lista = []
    for marca in marcas:
        marca_id, marca_nombre, logo_binario = marca
        if logo_binario:
            logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = ""  # Placeholder en caso de que no haya logo
        marcas_lista.append((marca_id, marca_nombre, logo_url))
    
    conexion.close()
    return marcas_lista


def obtener_marcas_index(cant):
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.marca, 
                ma.img_logo, 
                nov.id AS novedad_id, 
                nov.tipo_novedadid, 
                ino.imagen
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
    
    marcas_lista = []
    for marca in marcas:
        marca_id, marca_nombre, logo_binario , nov_id, nov_tip, img_nov = marca

        productosMarca = controlador_productos.obtener_en_tarjetas_marca(0 , marca_id , cant)

        if logo_binario:
            logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = ""

        if img_nov:
            img_nov_base64 = base64.b64encode(img_nov).decode('utf-8')
            img_nov_url = f"data:image/png;base64,{img_nov_base64}"
        else:
            img_nov_url = "" 

        
        marcas_lista.append((marca_id, marca_nombre, logo_url, nov_id, nov_tip, img_nov_url, productosMarca))
    
    conexion.close()
    return marcas_lista


def obtener_marca_disponible_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.marca, 
                ma.img_logo,
                ma.img_banner,
                ma.disponibilidad
            FROM marca ma
            where ma.disponibilidad = 1 and ma.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        marca = cursor.fetchone()

    marca_elemento = None

    if marca:
        marca_id, marca_nombre, logo_binario, banner_binario , marca_disp = marca

        if logo_binario:
            logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = ""  # Placeholder en caso de que no haya logo

        if banner_binario:
            banner_base64 = base64.b64encode(banner_binario).decode('utf-8')
            banner_url = f"data:image/png;base64,{banner_base64}"
        else:
            banner_url = ""  # Placeholder en caso de que no haya banner

        marca_elemento = (marca_id, marca_nombre, logo_url, banner_url , marca_disp)

    conexion.close()
    return marca_elemento


def obtener_todas_marcas_recientes():
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    id,
                    marca, 
                    img_logo 
                FROM marca 
                where disponibilidad = 1
                order by fecha_registro desc
                '''
        cursor.execute(sql)
        marcas = cursor.fetchall()
    
    marcas_lista = []
    for marca in marcas:
        marca_id, marca_nombre, logo_binario = marca
        if logo_binario:
            logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = ""  
        marcas_lista.append((marca_id, marca_nombre, logo_url))
    
    conexion.close()
    return marcas_lista






def insertar_marca(marca, logo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO marca(marca, img_logo) VALUES (%s, %s)", (marca, logo))
    conexion.commit()
    conexion.close()


def obtener_marcas():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, marca, img_logo FROM marca")
        marcas = cursor.fetchall()
        
        # Convertir el logo binario a base64 para cada marca
        marcas_procesadas = []
        for marca in marcas:
            id_marca = marca[0]
            nombre_marca = marca[1]
            logo_binario = marca[2]
            
            # Convertir el logo binario a una cadena base64
            if logo_binario:
                logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
                logo_formato = f"data:image/png;base64,{logo_base64}" 
            else:
                logo_formato = None 
            
            marcas_procesadas.append((id_marca, nombre_marca, logo_formato))
    
    conexion.close()
    return marcas_procesadas


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
        cursor.execute("SELECT id, marca,img_logo FROM marca WHERE id = %s", (id,))
        marca = cursor.fetchone()
    conexion.close()
    return marca


def actualizar_marca(marca,logo, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE marca SET marca = %s ,img_logo = %s WHERE id =%s",
                       (marca,logo, id))
    conexion.commit()
    conexion.close()
