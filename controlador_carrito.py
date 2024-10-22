from bd import obtener_conexion


#PARA INSERTAR EN PEDIDO
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

#PARA INSERTAR EN DETALLE
def insertar_detalle(producto_id, pedido_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        query = "SELECT * FROM detalles_pedido WHERE PRODUCTOid = %s AND PEDIDOid = %s"
        cursor.execute(query, (producto_id, pedido_id))
        result = cursor.fetchone()  # Obtener el resultado de la consulta. Usamos fetchOne para obtener solo un valor
        
        if result:  
            sql = "UPDATE detalles_pedido SET cantidad = cantidad + 1 WHERE PRODUCTOid = %s AND PEDIDOid = %s"
            cursor.execute(sql, (producto_id, pedido_id))
        else:
            sql = '''
                INSERT INTO detalles_pedido (PRODUCTOid, PEDIDOid, cantidad)
                VALUES (%s, %s, 1)
            '''
            cursor.execute(sql, (producto_id, pedido_id))
    
    # Confirmar los cambios
    conexion.commit()
    conexion.close()

 #PARA CAMBIAR DE ESTADO 1 A 2   
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
    
#Para eliminar del carre
def eliminar_producto(pedido_id, producto_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor: 
             
            query = "SELECT cantidad FROM detalles_pedido WHERE PEDIDOid = %s AND PRODUCTOid = %s"
            cursor.execute(query, (pedido_id, producto_id))
            resultado = cursor.fetchone()
            
            if resultado:
                cantidad = resultado[0] #Aquí extraemos lo que no devolvió la tupla del fetchOne

                if cantidad == 1:
                    query = "DELETE FROM detalles_pedido WHERE PEDIDOid = %s AND PRODUCTOid = %s"
                    cursor.execute(query, (pedido_id, producto_id))
                    #Verificamos si quedan más productos en el carro
                    query = "SELECT COUNT(*) FROM detalles_pedido WHERE PEDIDOid = %s"
                    cursor.execute(query, (pedido_id,))
                    resultado = cursor.fetchone()

                    if resultado[0] == 0:
                        query = "DELETE FROM pedido WHERE id = %s"
                        cursor.execute(query, (pedido_id,))
                else:
                    
                    query = "UPDATE detalles_pedido SET cantidad = cantidad - 1 WHERE PEDIDOid = %s AND PRODUCTOid = %s"
                    cursor.execute(query, (pedido_id, producto_id))
            
        # Confirmar los cambios en la base de datos
        conexion.commit()
    
    except Exception as e:
        conexion.rollback()  
        raise e
    
    finally:
        conexion.close() 
#CONFIRMAR QUE YA NO HAYA UN PEDIDO
def verificarIdPedido(usuario_id, estado_pedido):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = "SELECT id FROM pedido WHERE USUARIOid = %s AND ESTADO_PEDIDOid = %s"
            cursor.execute(query, (usuario_id, estado_pedido))
            resultado = cursor.fetchone() 

            return resultado[0] if resultado else None
    except Exception as e:
        conexion.rollback() 
        raise e
    finally:
        conexion.close()


    
#PARA AUMENTAR CANTIDAD
def aumentar_producto(pedido_id, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE detalles_pedido SET cantidad = cantidad + 1 WHERE PRODUCTOid = %s AND PEDIDOid = %s"
        cursor.execute(sql, (producto_id, pedido_id))
        print(f"Filas afectadas: {cursor.rowcount}") 
    
    conexion.commit()
    conexion.close()

#Ultimo pedido
def ultimoPedido(usuario_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT MAX(id) FROM pedido WHERE USUARIOid = %s"
            cursor.execute(sql, (usuario_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener el último pedido: {e}")
        return None
    finally:
        conexion.close()
