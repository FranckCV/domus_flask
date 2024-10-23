from bd import obtener_conexion
import base64
import controlador_productos
tabla = 'pedido'

def actualizar_MetPago_Pedido(pedido_id, metodo):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        query = """
            UPDATE pedido
            SET metodo_pagoid = %s  
            WHERE id = %s
        """
        cursor.execute(query, (metodo, pedido_id))
    conexion.commit()
    conexion.close()

def actualizarPedido(pedido_id, fecha_compra, subtotal):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        query = """
            UPDATE pedido
            SET fecha_compra = %s, subtotal = %s  
            WHERE id = %s
        """
        cursor.execute(query, (fecha_compra, subtotal, pedido_id))
    conexion.commit()
    conexion.close()

def obtener_listado_pedidos():
    conexion = obtener_conexion()
    pedido=[]
    with conexion.cursor() as cursor:
        cursor.execute('''
            SELECT 
                P.id,
                P.fecha_compra,
                P.subtotal,
                P.METODO_PAGOid,
                U.nombres,
                P.ESTADO_PEDIDOid
            FROM pedido P
            inner join usuario U on U.id=P.USUARIOid
        ''')
        pedido = cursor.fetchall()
    
    conexion.close()
    return pedido


def eliminar_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM pedido WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()



def actualizar_pedido(pedido,logo, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE pedido SET pedido = %s ,img_logo = %s WHERE id =%s",
                       (pedido,logo, id))
    conexion.commit()
    conexion.close()

def obtener_id_pedido(pedido):
    conexion = obtener_conexion()
    pedido_id = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM pedido WHERE pedido = %s", (pedido,))
        resultado = cursor.fetchone()
        if resultado:
            pedido_id = resultado[0]
    conexion.close()
    return pedido_id

def obtenerUsuarioPedido(id):
    conexion = obtener_conexion()
    pedido_id = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT U.nombres 
                FROM pedido P 
                INNER JOIN usuario U ON U.id = P.USUARIOid 
                WHERE P.id = %s
            ''', (id,)) 
            resultado = cursor.fetchone()
            
            if resultado:
                pedido_id = resultado[0] 
    except Exception as e:
        print(f"Error al obtener el nombre del usuario: {e}")
    finally:
        conexion.close()
    
    return pedido_id

def buscar_pedido_por_id(id_pedido):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        query = '''
            SELECT 
                P.id,
                P.fecha_compra,
                P.subtotal,
                P.METODO_PAGOid,
                U.nombres AS nombre_usuario,
                P.ESTADO_PEDIDOid
            FROM pedido P
            INNER JOIN usuario U ON U.id = P.USUARIOid
            WHERE P.id = %s
        '''
        cursor.execute(query, (id_pedido,))
        pedido = cursor.fetchone()

    conexion.close()

    if pedido:
        return True
    else:
        return False 


