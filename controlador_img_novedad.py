from bd import obtener_conexion
import base64

def obtener_imagenes_novedad_por_id(novedad_id):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nomImagen, 
                imagen, 
                TIPO_IMG_NOVEDADid 
            FROM IMG_NOVEDAD 
            WHERE NOVEDADid = %s
        '''
        cursor.execute(sql, (novedad_id,))
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        img_id, img_nombre, img_binario, tipo_img_id = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder si no hay imagen

        imagenes_lista.append((img_id, img_nombre, img_url, tipo_img_id))
    
    conexion.close()
    return imagenes_lista


def obtener_imagen_novedad_por_tipo(novedad_id, tipo_img_id):
    conexion = obtener_conexion()
    imagen = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nomImagen, 
                imagen 
            FROM IMG_NOVEDAD 
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
            INSERT INTO IMG_NOVEDAD (nomImagen, imagen, TIPO_IMG_NOVEDADid, NOVEDADid)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(sql, (nomImagen, imagen_binaria, tipo_img_id, novedad_id))
    conexion.commit()
    conexion.close()


def actualizar_imagen_novedad(id, nomImagen, imagen_binaria, tipo_img_id, novedad_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE IMG_NOVEDAD 
            SET nomImagen = %s, imagen = %s, TIPO_IMG_NOVEDADid = %s, NOVEDADid = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nomImagen, imagen_binaria, tipo_img_id, novedad_id, id))
    conexion.commit()
    conexion.close()


def eliminar_imagen_novedad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM IMG_NOVEDAD WHERE id = %s", (id,))
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
            FROM IMG_NOVEDAD
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
                id, 
                nomImagen, 
                imagen, 
                TIPO_IMG_NOVEDADid, 
                NOVEDADid 
            FROM IMG_NOVEDAD
            WHERE NOVEDADid = %s
            ORDER BY id DESC
        '''
        cursor.execute(sql, (novedad_id,))
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        img_id, img_nombre, img_binario, tipo_img_id, novedad_id = imagen
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder si no hay imagen

        imagenes_lista.append((img_id, img_nombre, img_url, tipo_img_id, novedad_id))
    
    conexion.close()
    return imagenes_lista


