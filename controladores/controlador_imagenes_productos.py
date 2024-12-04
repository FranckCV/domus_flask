from controladores.bd import obtener_conexion
import base64
tabla = 'producto'

def obtener_imagenes_por_producto(id):
    conexion = obtener_conexion()
    imagenes = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                ipr.id ,
                ipr.imagen,
                ipr.imgPrincipal,
                ipr.productoid
            FROM img_producto ipr
            where ipr.productoid = '''+str(id)+'''
            order by ipr.imgPrincipal desc
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        id, img , prin , pro = imagen
        if imagen:
            img_base64 = base64.b64encode(img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        imagenes_lista.append((id, img_url , prin , pro))

    conexion.close()
    return imagenes_lista


def obtener_img_principal_por_producto(id):
    conexion = obtener_conexion()
    imagenes = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ipr.id ,
                ipr.imagen
            FROM img_producto ipr
            where ipr.productoid = '''+str(id)+''' and ipr.imgPrincipal = 1
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchone()
    conexion.close()
    return imagenes


def insertar_img_producto(nombre, imagen, principal, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO img_producto(img_nombre, imagen, imgprincipal, productoid)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, imagen, principal, producto_id))
    conexion.commit()
    conexion.close()


def actualizar_img_producto(imagen, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE img_producto 
            SET imagen = %s 
            WHERE productoid = %s and imgPrincipal = 1
        '''
        cursor.execute(sql, (imagen, id))
    conexion.commit()
    conexion.close()


def eliminar_img_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM img_producto 
            WHERE productoid = %s and imgPrincipal = 1
        '''
        cursor.execute(sql, (id))
    conexion.commit()
    conexion.close()


def validar_img_principal_por_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                count(ipr.id)
            FROM img_producto ipr
            where ipr.productoid = '''+str(id)+''' and ipr.imgPrincipal = 1
            '''
        cursor.execute(sql)
        cant = cursor.fetchone()[0]
        conexion.close()
        return cant


def obtener_listado_imagenes_por_producto(id):
    conexion = obtener_conexion()
    imagenes = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                ipr.id ,
                ipr.imagen,
                ipr.imgPrincipal,
                ipr.productoid
            FROM img_producto ipr
            where ipr.productoid = '''+str(id)+'''
            order by ipr.imgPrincipal desc
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        id, img , prin , pro = imagen
        if imagen:
            img_base64 = base64.b64encode(img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        imagenes_lista.append((id, img_url , prin , pro))

    conexion.close()
    return imagenes_lista

