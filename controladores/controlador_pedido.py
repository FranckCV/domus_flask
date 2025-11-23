from bd import obtener_conexion
import base64
import controladores.controlador_productos as controlador_productos
tabla = 'pedido'
import bd


def get_detalle_pedido(pedidoid,productoid):
    sql = '''
        SELECT
            productoid ,
            pedidoid,
            cantidad
        FROM detalles_pedido
        where pedidoid = %s and productoid = %s
        '''
    return bd.sql_select_fetchone(sql,(pedidoid,productoid))


def get_carrito_usuarioid(usuarioid):
    sql = '''
        SELECT
            p.id,
            p.fecha_compra,
            p.subtotal,
            p.usuarioid,
            met.nombre as metodo_pago,
            est.nombre as estado,
            p.metodo_pagoid ,
            p.estado_pedidoid ,
            p.registro_auditoria
        FROM pedido p
        LEFT join metodo_pago met on p.metodo_pagoid = met.id
        LEFT join estado_pedido est on est.id = p.estado_pedidoid
        where p.usuarioid = %s and p.estado_pedidoid = 1
        '''
    return bd.sql_select_fetchone(sql,(usuarioid)) or {}


def get_pedido_id(id):
    sql = '''
        SELECT
            p.id,
            DATE_FORMAT(p.fecha_compra, '%%d/%%m/%%Y') as fecha_compra,
            p.subtotal,
            p.usuarioid,
            met.nombre as metodo_pago,
            est.nombre as estado,
            p.metodo_pagoid ,
            p.estado_pedidoid ,
            p.registro_auditoria
        FROM pedido p
        LEFT join metodo_pago met on p.metodo_pagoid = met.id
        LEFT join estado_pedido est on est.id = p.estado_pedidoid
        where p.id = %s
        '''
    return bd.sql_select_fetchone(sql,(id))


def get_pedidos_usuario_id(usuario_id):
    sql = '''
        SELECT
                p.id,
                DATE_FORMAT(p.fecha_compra, '%%d/%%m/%%Y') as fecha_compra,
                p.subtotal,
                p.usuarioid,
                met.nombre AS metodo_pago,
                est.nombre AS estado,
                p.registro_auditoria
            FROM pedido p
            INNER JOIN metodo_pago met ON p.metodo_pagoid = met.id
            INNER JOIN estado_pedido est ON p.estado_pedidoid = est.id
            WHERE p.usuarioid = %s
              AND p.estado_pedidoid != 1
            order by fecha_compra desc
        '''
    return bd.sql_select_fetchall(sql,(usuario_id,))


def insert_detalles_pedido(productoid, pedidoid, cantidad):
    sql = '''
        INSERT INTO detalles_pedido(productoid, pedidoid, cantidad) VALUES
        (%s , %s, %s)
    '''
    bd.sql_execute(sql,(productoid, pedidoid, cantidad))


def update_detalles_pedido(productoid, pedidoid, cantidad):
    sql = '''
        UPDATE detalles_pedido SET
            cantidad = %s
        WHERE productoid=%s and pedidoid=%s
    '''
    bd.sql_execute(sql,(cantidad,productoid, pedidoid))


def delete_detalles_pedido(productoid, pedidoid):
    sql = '''
        DELETE FROM detalles_pedido
        WHERE productoid=%s and pedidoid=%s
    '''
    bd.sql_execute(sql,(productoid, pedidoid))


def update_plus_detalles_pedido(productoid, pedidoid):
    sql = '''
        UPDATE detalles_pedido SET
            cantidad = cantidad + 1
        WHERE productoid=%s and pedidoid=%s
    '''
    bd.sql_execute(sql,(productoid, pedidoid))


def update_minus_detalles_pedido(productoid, pedidoid):
    sql = '''
        UPDATE detalles_pedido SET
            cantidad = cantidad - 1
        WHERE productoid=%s and pedidoid=%s
    '''
    bd.sql_execute(sql,(productoid, pedidoid))


def insert_new_pedido_carrito(usuarioid):
    sql = '''
        INSERT INTO pedido(usuarioid, estado_pedidoid) VALUES
        (%s,1)
    '''
    return bd.sql_execute_lastrowid(sql,( usuarioid ))


def update_pedido_set_estado(pedidoid, estado):
    sql = '''
        UPDATE pedido SET
            estado_pedidoid=%s
        WHERE id=%s
    '''
    bd.sql_execute(sql,( estado, pedidoid))


def pagar_pedido_carrito(pedidoid,subtotal):
    sql = '''
        UPDATE pedido SET
            estado_pedidoid=%s ,
            fecha_compra = NOW(),
            subtotal = %s
        WHERE id=%s
    '''
    bd.sql_execute(sql,( 2,subtotal , pedidoid))










def actualizarPedido(pedido_id, fecha_compra, subtotal,metodo_pago,estado,usuario_id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        query = """
            UPDATE pedido
            SET
            fecha_compra = NOW(),
            subtotal = %s ,
            METODO_PAGOid=%s,
            ESTADO_PEDIDOid=%s
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

def obtener_listado_pedidos_usuario_fecha_id(id):
    conexion = obtener_conexion()
    pedido=[]
    with conexion.cursor() as cursor:
        cursor.execute('''
                        select
                    p.id,
                    p.fecha_compra,
                    p.subtotal,
                    p.metodo_pagoid,
                    concat(u.nombres, ' ' , u.apellidos) as nombre_completo,
                    p.estado_pedidoid,
                    sum(dpe.cantidad),
                    met.disponibilidad,
                    p.usuarioid
                from pedido p
                left join usuario u on u.id = p.usuarioid
                left join detalles_pedido dpe on dpe.pedidoid = p.id
                left join producto pr on pr.id = dpe.productoid
                left join metodo_pago met on p.metodo_pagoid = met.id
                where p.usuarioid = '''+str(id)+'''
                group by p.id , dpe.pedidoid
                order by p.fecha_compra, p.id desc
        ''')
        pedido = cursor.fetchall()
    conexion.close()
    return pedido

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


######################################
def obtener_pedidos_usuario(usuario_id):
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor() as cursor:
        cursor.execute('''
            SELECT
                P.id,
                P.fecha_compra,
                P.subtotal,
                P.METODO_PAGOid,
                CONCAT(u.nombres, ' ' , u.apellidos) as nombre,
                P.ESTADO_PEDIDOid,
                sum(dpe.cantidad) as total_productos,
                met.disponibilidad,
                P.usuarioid,
                pr.imagen  -- Suponiendo que la imagen está en el campo imagen de la tabla producto
            FROM pedido P
            LEFT JOIN usuario U ON U.id = P.USUARIOid
            LEFT JOIN detalles_pedido dpe ON dpe.pedidoid = P.id
            LEFT JOIN producto pr ON pr.id = dpe.productoid
            LEFT JOIN metodo_pago met ON p.METODO_PAGOid = met.id
            WHERE P.usuarioid = %s
            GROUP BY P.id
            ORDER BY P.ESTADO_PEDIDOid, P.fecha_compra DESC
        ''', (usuario_id,))

        pedidos = cursor.fetchall()

    # Convertir las imágenes a base64
    for pedido in pedidos:
        for i, producto in enumerate(pedido['productos']):
            img_binario = producto['imagen']
            if img_binario:
                imagen_base64 = base64.b64encode(img_binario).decode('utf-8')
                imagen = f"data:image/png;base64,{imagen_base64}"
                producto['imagen_base64'] = imagen
            else:
                producto['imagen_base64'] = ""

    conexion.close()
    return pedidos


##############agrego###########
def obtener_pedidos_por_usuario_validacion_stock(usuario_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT id FROM pedido WHERE estado_pedidoid = 1 AND usuarioid = %s LIMIT 1;
            ''', (usuario_id,))
            resultado = cursor.fetchone()  # Obtiene el primer pedido encontrado

            if resultado:
                return resultado[0]  # Retorna solo el id del primer pedido
            return None  # Si no hay pedidos con estado 1, retorna None
    except Exception as e:
        print(f"Error al obtener el pedido para el usuario {usuario_id}: {e}")
        return None
    finally:
        conexion.close()


#######################################################################
def actualizar_pedido_pagado(pedido_id, metodo_pago_id, subtotal):
    productos = controlador_productos.get_productos_pedido(pedido_id)

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE pedido
                SET
                    fecha_compra = NOW(),
                    subtotal = %s,
                    metodo_pagoid = %s,
                    estado_pedidoid = 2
                WHERE id = %s
            """, (subtotal, metodo_pago_id, pedido_id))

            if len(productos) > 0:
                for p in productos:
                    if p['stock'] - p['cantidad'] >= 0:
                        cursor.execute("""
                            UPDATE producto SET
                                stock = stock - %s
                            WHERE id = %s
                        """, (p['cantidad'],p['id'])
                        )
                    else:
                        conexion.rollback()
                        return False
            else:
                conexion.rollback()
                return False

        conexion.commit()
        return True

    except Exception as e:
        print("Error al actualizar pedido:", e)
        conexion.rollback()
        return False

    finally:
        conexion.close()

