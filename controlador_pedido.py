from bd import obtener_conexion
import base64
import controlador_productos
tabla = 'pedido'

# def actualizar_MetPago_Pedido(pedido_id, metodo):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         query = """
#             UPDATE pedido
#             SET METODO_PAGOid = %s  
#             WHERE id = %s
#         """
#         cursor.execute(query, (metodo, pedido_id))
#     conexion.commit()
#     conexion.close()


def actualizarPedido(pedido_id, fecha_compra, subtotal,metodo_pago,estado,usuario_id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        query = """
            UPDATE pedido
            SET fecha_compra = %s, subtotal = %s , METODO_PAGOid=%s, ESTADO_PEDIDOid=%s 
            WHERE USUARIOid=%s and id = %s
        """
        cursor.execute(query, (fecha_compra, subtotal,metodo_pago,estado,usuario_id,pedido_id))
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
                            CONCAT(u.nombres, ' ' , u.apellidos) as nombre,
                            P.ESTADO_PEDIDOid,
                            sum(dpe.cantidad),
                            met.disponibilidad,
                            P.usuarioid
                        FROM pedido P
                        left join usuario U on U.id = P.USUARIOid
                        left join detalles_pedido dpe on dpe.pedidoid = P.id
                        left join producto pr on pr.id = dpe.productoid
                        left join metodo_pago met on p.METODO_PAGOid = met.id
                        group by p.id , dpe.pedidoid
                        order by P.ESTADO_PEDIDOid , P.fecha_compra desc
        ''')
        pedido = cursor.fetchall()
    
    conexion.close()
    return pedido


def obtener_pedido_id(id):
    conexion = obtener_conexion()
    pedido=[]
    with conexion.cursor() as cursor:
        cursor.execute('''
                            SELECT 
                                P.id,
                                P.fecha_compra,
                                P.subtotal,
                                P.METODO_PAGOid,
                                CONCAT(u.nombres, ' ' , u.apellidos) as nombre,
                                P.ESTADO_PEDIDOid,
                                sum(dpe.cantidad),
                                met.disponibilidad,
                                P.usuarioid
                            FROM pedido P
                            left join usuario U on U.id = P.USUARIOid
                            left join detalles_pedido dpe on dpe.pedidoid = P.id
                            left join producto pr on pr.id = dpe.productoid
                            left join metodo_pago met on p.METODO_PAGOid = met.id
                            where  P.id = '''+str(id)+'''
                            group by p.id , dpe.pedidoid
                            order by P.ESTADO_PEDIDOid , P.fecha_compra desc
        ''')
        pedido = cursor.fetchone()
    
    conexion.close()
    return pedido


def buscar_listado_pedidos_usuario(nombre):
    conexion = obtener_conexion()
    pedido=[]
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            P.id,
                            P.fecha_compra,
                            P.subtotal,
                            P.METODO_PAGOid,
                            CONCAT(u.nombres, ' ' , u.apellidos) as nombre_completo,
                            P.ESTADO_PEDIDOid,
                            sum(dpe.cantidad),
                            met.disponibilidad
                        FROM pedido P
                        left join usuario U on U.id = P.USUARIOid
                        left join detalles_pedido dpe on dpe.pedidoid = P.id
                        left join producto pr on pr.id = dpe.productoid
                        left join metodo_pago met on p.METODO_PAGOid = met.id
                        where UPPER(CONCAT(u.nombres, ' ' , u.apellidos)) LIKE UPPER ('%'''+nombre+'''%')
                        group by p.id , dpe.pedidoid
                        order by P.ESTADO_PEDIDOid , nombre_completo
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


def obtener_listado_pedidos_usuario_id(id):
    conexion = obtener_conexion()
    pedido=[]
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            P.id,
                            P.fecha_compra,
                            P.subtotal,
                            P.METODO_PAGOid,
                            CONCAT(u.nombres, ' ' , u.apellidos) as nombre_completo,
                            P.ESTADO_PEDIDOid,
                            sum(dpe.cantidad),
                            met.disponibilidad,
                            P.usuarioid
                        FROM pedido P
                        left join usuario U on U.id = P.USUARIOid
                        left join detalles_pedido dpe on dpe.pedidoid = P.id
                        left join producto pr on pr.id = dpe.productoid
                        left join metodo_pago met on p.METODO_PAGOid = met.id
                        where P.USUARIOid = '''+str(id)+'''
                        group by p.id , dpe.pedidoid
                        order by P.ESTADO_PEDIDOid , nombre_completo
        ''')
        pedido = cursor.fetchall()
    
    conexion.close()
    return pedido

