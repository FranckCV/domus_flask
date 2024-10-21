from bd import obtener_conexion

def insertar_pedido(usuario, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO pedido (USUARIOid, ESTADO_PEDIDOid)
            VALUES (%s, %s)
        '''
        cursor.execute(sql, (usuario, estado))
        
        # Obtener el ID generado por la inserción
        pedido_id = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return pedido_id

def insertar_detalle(producto_id,pedido_id,cantidad):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO detalles_pedido (PRODUCTOid,PEDIDOid	,cantidad)
            VALUES (%s, %s,%s)
        '''
        cursor.execute(sql, (producto_id,pedido_id,cantidad))
    conexion.commit()
    conexion.close()
    
    
def actualizar_estado_pedido(usuario_id, estado_pedido_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE pedido
            SET ESTADO_PEDIDOid = %s
            WHERE USUARIOid = %s AND ESTADO_PEDIDOid = 1
        '''
        cursor.execute(sql, (estado_pedido_id, usuario_id))
    conexion.commit()
    conexion.close()

def eliminar_producto(pedido_id, producto_id):
    conexion= obtener_conexion()
    try:
        with conexion.cursor() as cursor:  
            query = "DELETE FROM detalle_pedido WHERE pedido_id = %s AND producto_id = %s"
            cursor.execute(query, (pedido_id, producto_id))
        conexion.commit()
    
    except Exception as e:
        conexion.rollback()
        raise e
