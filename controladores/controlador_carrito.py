from controladores.bd import obtener_conexion

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
    try:
        with conexion.cursor() as cursor:
            query = "SELECT * FROM detalles_pedido WHERE PRODUCTOid = %s AND PEDIDOid = %s"
            cursor.execute(query, (producto_id, pedido_id))
            result = cursor.fetchone() 
            
            if result:
                sql = "UPDATE detalles_pedido SET cantidad = cantidad + 1 WHERE PRODUCTOid = %s AND PEDIDOid = %s"
            else:
                sql = '''
                    INSERT INTO detalles_pedido (PRODUCTOid, PEDIDOid, cantidad)
                    VALUES (%s, %s, 1)
                '''
            
            cursor.execute(sql, (producto_id, pedido_id))
            conexion.commit()
            
            return True
    except Exception as e:
        print(f"Error en la base de datos: {e}") 
        return False
    finally:
        if conexion:
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
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE detalles_pedido SET cantidad = cantidad + 1 WHERE PRODUCTOid = %s AND PEDIDOid = %s"
            cursor.execute(sql, (producto_id, pedido_id))
            # print(f"Filas afectadas: {cursor.rowcount}")
        
        conexion.commit()
        return None 
    except Exception as e:
        return e 
    finally:
        if conexion:
            conexion.close()

#Ultimo pedido
def ultimoPedido(usuario_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT MAX(id) FROM pedido WHERE USUARIOid = %s and ESTADO_PEDIDOid=1"
            cursor.execute(sql, (usuario_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener el último pedido: {e}")
        return None
    finally:
        conexion.close()
#CANCELAR PEDIDO

def cancelar_pedido(usuario_id, estado_pedido_id,pedido_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE pedido
            SET ESTADO_PEDIDOid = %s
            WHERE USUARIOid = %s AND id = %s
        '''
        cursor.execute(sql, (estado_pedido_id, usuario_id,pedido_id))

     
    conexion.commit()
    conexion.close()

#####################
def validar_stock(producto_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT stock FROM producto WHERE id = %s"
            cursor.execute(sql, (producto_id,))
            result = cursor.fetchone()
            if result:
                return result[0] 
            return 0  
    except Exception as e:
        return e
    finally:
        if conexion:
            conexion.close()

def obtener_cantidad_en_carrito(pedido_id, producto_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = '''
                SELECT cantidad
                FROM detalles_pedido
                WHERE pedidoid = %s AND productoid = %s
            '''
            cursor.execute(sql, (pedido_id, producto_id))
            result = cursor.fetchone()  # Esto devuelve la cantidad actual del producto en el carrito
            if result:
                return result[0]  # Retorna la cantidad
            return 0  # Si no hay cantidad, retorna 0
    except Exception as e:
        return e
    finally:
        if conexion:
            conexion.close()

def obtener_cantidad_en_carrito_v2(pedido_id, producto_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(''' 
                SELECT cantidad FROM detalles_pedido WHERE pedidoid = %s AND productoid = %s 
            ''', (pedido_id, producto_id))
            result = cursor.fetchone()
            if result:
                return result[0]  # Devuelve la cantidad actual del producto en el carrito
            return 0  # Si no hay el producto en el carrito, devuelve 0
    except Exception as e:
        print(f"Error al obtener cantidad en carrito: {e}")
        return 0  # Retorna 0 en caso de error
    finally:
        conexion.close()


