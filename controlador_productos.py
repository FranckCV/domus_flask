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
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                pr.fecha_registro, 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr
            WHERE pr.id = %s
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_info_por_id(id):
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
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                pr.fecha_registro, 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr

            WHERE pr.id = %s
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_informacion_producto(id):
    return obtener_por_id(id)


def obtenerEnTarjetasMasRecientes():
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
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid 
                where ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                order by pr.fecha_registro desc
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


def obtenerEnTarjetasMasPopulares():
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
                    ipr.imagen,
                    COUNT(dp.PRODUCTOid) AS total_compras
                FROM 
                    PRODUCTO pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN detalles_pedido dp ON pr.id = dp.PRODUCTOid
                GROUP BY 
                    pr.id
                ORDER BY 
                    total_compras DESC;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cant = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasOfertas():
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
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid 
                where ipr.imgPrincipal = 1 and pr.disponibilidad = 1 and pr.precio_oferta > 0
                order by pr.fecha_registro desc
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


def obtener_en_tarjetas_marca(id,marca, limit):
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
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' AND pr.MARCAid = '''+str(marca)+'''
                ORDER BY pr.fecha_registro desc
            '''
        
        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""

        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtener_en_tarjetas_subcategoria(id,subcategoria, limit):
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
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' AND pr.SUBCATEGORIAid = '''+str(subcategoria)+'''
                ORDER BY pr.fecha_registro desc
            '''
        
        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""

        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtener_en_tarjetas_categoria(id,categoria, limit):
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
                INNER JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' 
                AND sub.CATEGORIAid = '''+str(categoria)+'''
                ORDER BY pr.fecha_registro desc
            '''
        
        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""

        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


# CRUD

def insertar_producto(nombre, price_regular, price_online, precio_oferta, info_adicional, stock, marca_id, subcategoria_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO producto(nombre, price_regular, precio_online, precio_oferta, info_adicional, stock, disponibilidad, MARCAid, SUBCATEGORIAid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, info_adicional, stock, 1, marca_id, subcategoria_id))

        cursor.execute('SELECT LAST_INSERT_ID();')
        id_producto = cursor.fetchone()[0]

    conexion.commit()
    conexion.close()

    return id_producto


def obtener_productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nombre, 
                price_regular, 
                precio_online, 
                precio_oferta, 
                id, 
                info_adicional, 
                stock, 
                fecha_registro, 
                disponibilidad,
                MARCAid, 
                SUBCATEGORIAid 
            FROM producto
        '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_listado_productos():
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
                    pr.id,
                    pr.info_adicional, 
                    pr.stock, 
                    pr.fecha_registro, 
                    pr.disponibilidad,
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid,
                    ipr.imagen 
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid 
                where ipr.imgPrincipal = 1
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_id, pr_info, pr_stock, pr_fec, pr_disp,pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_id, pr_info, pr_stock, pr_fec, pr_disp,pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista





def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM producto WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()


def actualizar_producto(nombre, price_regular, price_online, precio_oferta, info_adicional, stock, disponibilidad, marca_id, subcategoria_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE producto 
            SET nombre = %s, price_regular = %s, precio_online = %s, precio_oferta = %s, info_adicional = %s, stock = %s, disponibilidad = %s, MARCAid = %s, SUBCATEGORIAid = %s 
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, info_adicional, stock, disponibilidad, marca_id, subcategoria_id, id))
    conexion.commit()
    conexion.close()


def obtener_por_nombre(nombre):
    conexion = obtener_conexion()
    producto = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id, 
                pr.nombre, 
                pr.price_regular, 
                pr.precio_online, 
                pr.precio_oferta, 
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                pr.fecha_registro, 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr
            WHERE pr.nombre LIKE '%'''+str(nombre)+'''%' and pr.disponibilidad = 1
        '''
        cursor.execute(sql)
        producto = cursor.fetchall()
    conexion.close()
    return producto


##validar las eliminaciones físicas

def buscar_en_caracteristica_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM CARACTERISTICA_PRODUCTO WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result

def buscar_en_img_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM img_producto WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result

def buscar_en_lista_deseos(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM lista_deseos WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_detalles_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM detalles_pedido WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result



