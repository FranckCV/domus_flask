from bd import obtener_conexion

def obtenerCaracteristicasDisponiblesxProducto(id,valor):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                car.campo,
                cpr.valor,
                car.disponibilidad
            FROM caracteristica_producto cpr
            inner join caracteristica car on car.id = cpr.CARACTERISTICAid
            inner join caracteristica_subcategoria csc on csc.CARACTERISTICAid = cpr.CARACTERISTICAid
            where cpr.productoid = '''+str(id)+''' and cpr.principal = '''+str(valor)+''' and car.disponibilidad = 1
            order by car.campo
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas

def obtenerCaracteristicasxProducto(id,valor):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                car.campo,
                cpr.valor,
                car.disponibilidad
            FROM caracteristica_producto cpr
            inner join caracteristica car on car.id = cpr.CARACTERISTICAid
            inner join caracteristica_subcategoria csc on csc.CARACTERISTICAid = cpr.CARACTERISTICAid
            where cpr.productoid = '''+str(id)+''' and cpr.principal = '''+str(valor)+'''
            order by car.campo
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas


def insertar_caracteristica_producto(caracteristica_producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO caracteristica_producto (caracteristicaid, productoid, valor, principal)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(sql, (caracteristica_producto.CARACTERISTICAid, caracteristica_producto.PRODUCTOid,
                             caracteristica_producto.valor, caracteristica_producto.principal))
    conexion.commit()
    conexion.close()


def obtener_caracteristicas_producto(producto_id):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT caracteristicaid, productoid, valor, principal
            FROM caracteristica_producto
            WHERE productoid = %s
        '''
        cursor.execute(sql, (producto_id,))
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas

def actualizar_caracteristica_producto(caracteristica_producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE caracteristica_producto
            SET valor = %s, principal = %s
            WHERE caracteristicaid = %s AND productoid = %s
        '''
        cursor.execute(sql, (caracteristica_producto.valor, caracteristica_producto.principal,
                             caracteristica_producto.CARACTERISTICAid, caracteristica_producto.PRODUCTOid))
    conexion.commit()
    conexion.close()

def eliminar_caracteristica_producto(caracteristica_id, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM caracteristica_producto
            WHERE caracteristicaid = %s AND productoid = %s
        '''
        cursor.execute(sql, (caracteristica_id, producto_id))
    conexion.commit()
    conexion.close()

def obtener_caracteristica_producto(caracteristica_id, producto_id):
    conexion = obtener_conexion()
    caracteristica = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT caracteristicaid, productoid, valor, principal
            FROM caracteristica_producto
            WHERE caracteristicaid = %s AND productoid = %s
        '''
        cursor.execute(sql, (caracteristica_id, producto_id))
        caracteristica = cursor.fetchone()
    conexion.close()
    return caracteristica


