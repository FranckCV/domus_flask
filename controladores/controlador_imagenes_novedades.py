from controladores.bd import obtener_conexion
import base64
tabla = 'producto'

def obtener_imagenes_disponibles_por_novedad(id):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                img.id, 
                img.nomImagen, 
                img.imagen, 
                img.tipo_img_novedadid, 
                img.NOVEDADid 
            FROM img_novedad img
            LEFT join tipo_img_novedad tip on tip.id = img.TIPO_IMG_NOVEDADid
            WHERE NOVEDADid = %s and tip.disponibilidad = 1
            ORDER BY OCTET_LENGTH(img.imagen) DESC 
        '''
        cursor.execute(sql, (id))
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        img_id, img_nombre, img_binario, tipo_img_id, novedad_id = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = "" 

        imagenes_lista.append((img_id, img_nombre, img_url, tipo_img_id, novedad_id))
    
    conexion.close()
    return imagenes_lista


def obtener_imagenes_novedades_por_marca(marca):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ino.id ,
                ino.imagen
            FROM img_novedad ino
            inner join novedad nov on nov.id = ino.novedadid
            where nov.marcaid = '''+str(marca)+'''
            limit 1
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        id, img , prin= imagen
        if imagen:
            img_base64 = base64.b64encode(img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        imagenes_lista.append((id, img_url , prin))

    conexion.close()
    return imagenes_lista


##################################Esto es para novedades#######################333

def obtener_imagen_novedad_por_tipo(novedad_id, tipo_img_id):
    conexion = obtener_conexion()
    imagen = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nomImagen, 
                imagen 
            FROM img_novedad 
            WHERE NOVEDADid = %s AND TIPO_IMG_NOVEDADid = %s
        '''
        cursor.execute(sql, (novedad_id, tipo_img_id))
        imagen = cursor.fetchone()

    img_elemento = None
    if imagen:
        img_id, img_nombre, img_binario = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder si no hay imagen

        img_elemento = (img_id, img_nombre, img_url)
    
    conexion.close()
    return img_elemento


def insertar_imagen_novedad(nomImagen, imagen_binaria, tipo_img_id, novedad_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO img_novedad (nomImagen, imagen, TIPO_IMG_NOVEDADid, NOVEDADid)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(sql, (nomImagen, imagen_binaria, tipo_img_id, novedad_id))
    conexion.commit()
    conexion.close()


def actualizar_imagen_novedad(id, nomImagen, tipo_img_id, novedad_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE img_novedad 
            SET nomImagen = %s, TIPO_IMG_NOVEDADid = %s, NOVEDADid = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nomImagen, tipo_img_id, novedad_id, id))
    conexion.commit()
    conexion.close()


def eliminar_imagen_novedad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM img_novedad WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_todas_imagenes_novedad():
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nomImagen, 
                imagen, 
                TIPO_IMG_NOVEDADid, 
                NOVEDADid 
            FROM img_novedad
            ORDER BY id DESC
        '''
        cursor.execute(sql)
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        img_id, img_nombre, img_binario, tipo_img_id, novedad_id = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = "" 

        imagenes_lista.append((img_id, img_nombre, img_url, tipo_img_id, novedad_id))
    
    conexion.close()
    return imagenes_lista


def obtener_imagenes_novedad_por_id(novedad_id):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                img.id, 
                img.nomImagen, 
                img.imagen, 
                tip.tipo,  
                img.NOVEDADid,
                tip.id
            FROM img_novedad img
            LEFT join tipo_img_novedad tip on tip.id = img.TIPO_IMG_NOVEDADid
            WHERE NOVEDADid = %s
            ORDER BY nomImagen ASC
        '''
        cursor.execute(sql, (novedad_id,))
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        img_id, img_nombre, img_binario, tipo_img_id, novedad_id , tipo_id = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = "" 

        imagenes_lista.append((img_id, img_nombre, img_url, tipo_img_id, novedad_id,tipo_id))
    
    conexion.close()
    return imagenes_lista


def obtener_novedad_id_por_imagen_id(imagen_id):
    conexion = obtener_conexion()
    novedad_id = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                NOVEDADid 
            FROM img_novedad
            WHERE id = %s
        '''
        cursor.execute(sql, (imagen_id,))
        resultado = cursor.fetchone()

        if resultado:
            novedad_id = resultado[0]

    conexion.close()
    return novedad_id


def obtener_imagenes_novedad_id(id):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                img.id, 
                img.nomImagen, 
                img.imagen, 
                img.tipo_img_novedadid, 
                img.NOVEDADid,
                tip.tipo,
                tip.disponibilidad
            FROM img_novedad img
            LEFT join tipo_img_novedad tip on tip.id = img.TIPO_IMG_NOVEDADid
            WHERE NOVEDADid = %s
            ORDER BY OCTET_LENGTH(img.imagen) DESC 
        '''
        cursor.execute(sql, (id))
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        img_id, img_nombre, img_binario, tipo_img_id, novedad_id , tipo , tip_dip = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = "" 

        imagenes_lista.append((img_id, img_nombre, img_url, tipo_img_id, novedad_id, tipo , tip_dip))
    
    conexion.close()
    return imagenes_lista



def obtener_imagen_novedad_por_img_id(img_id):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                img.id, 
                img.nomImagen, 
                img.imagen, 
                tip.tipo,  
                img.NOVEDADid,
                tip.id
            FROM img_novedad img
            LEFT join tipo_img_novedad tip on tip.id = img.TIPO_IMG_NOVEDADid
            WHERE img.id = %s
            ORDER BY nomImagen ASC
        '''
        cursor.execute(sql, (img_id))
        imagenes = cursor.fetchone()

    img_id, img_nombre, img_binario, tipo_nov, novedad_id , tipo_id = imagenes
    if img_binario:
        img_base64 = base64.b64encode(img_binario).decode('utf-8')
        img_url = f"data:image/png;base64,{img_base64}"
    else:
        img_url = "" 

    imagenes_lista = (img_id, img_nombre, img_url, tipo_nov, novedad_id,tipo_id)
    
    conexion.close()
    return imagenes_lista

