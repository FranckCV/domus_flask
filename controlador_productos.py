from bd import obtener_conexion
import base64

tabla = 'producto'

def obtener_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id, 
                pr.nombre, 
                pr.price_regular, 
                pr.precio_online, 
                pr.precio_oferta, 
                pr.calificacion, 
                pr.info_adicional, 
                pr.stock, 
                pr.fecha_registro, 
                pr.MARCAid, 
                pr.SUBCATEGORIAid
            FROM producto pr
            WHERE pr.id = %s
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_informacion_producto(id):
    return obtener_por_id(id)


def obtener_en_tarjetas_mas_recientes():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen 
                FROM producto pr 
                INNER JOIN img_producto ipr 
                ON pr.id = ipr.PRODUCTOid 
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1
                ORDER BY pr.fecha_registro
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtener_en_tarjetas_marca(marca, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen 
                FROM producto pr 
                INNER JOIN img_producto ipr 
                ON pr.id = ipr.PRODUCTOid 
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.MARCAid = %s
                ORDER BY pr.fecha_registro
            '''
        if limit > 0:
            sql += ' LIMIT %s'
            cursor.execute(sql, (marca, limit))
        else:
            cursor.execute(sql, (marca,))
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def insertar_producto(nombre, price_regular, price_online, precio_oferta, calificacion, info_adicional, stock, fecha_registro, disponibilidad, marca_id, subcategoria_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO producto(nombre, price_regular, precio_online, precio_oferta, calificacion, info_adicional, stock, fecha_registro, disponibilidad, MARCAid, SUBCATEGORIAid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, calificacion, info_adicional, stock, fecha_registro, disponibilidad, marca_id, subcategoria_id))
    conexion.commit()
    conexion.close()


def obtener_productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT id, nombre, price_regular, precio_online, precio_oferta, calificacion, info_adicional, stock, fecha_registro, disponibilidad, MARCAid, SUBCATEGORIAid 
            FROM producto
        '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM producto WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()


def actualizar_producto(nombre, price_regular, price_online, precio_oferta, calificacion, info_adicional, stock, fecha_registro, disponibilidad, marca_id, subcategoria_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE producto 
            SET nombre = %s, price_regular = %s, precio_online = %s, precio_oferta = %s, calificacion = %s, info_adicional = %s, stock = %s, fecha_registro = %s, disponibilidad = %s, MARCAid = %s, SUBCATEGORIAid = %s 
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, calificacion, info_adicional, stock, fecha_registro, disponibilidad, marca_id, subcategoria_id, id))
    conexion.commit()
    conexion.close()
