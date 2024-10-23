from bd import obtener_conexion
import base64
import controlador_productos
tabla = 'pedido'


def actualizarPedido(pedido_id, fecha_compra, subtotal):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        query = """
            UPDATE pedido
            SET fecha_compra = %s, subtotal = %s
            WHERE id = %s
        """
        cursor.execute(query, fecha_compra, subtotal, pedido_id)
    cursor.commit()



def obtener_pedido_disponible_por_id(id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ma.id, 
                ma.pedido, 
                ma.img_logo,
                ma.img_banner,
                ma.disponibilidad
            FROM pedido ma
            where ma.disponibilidad = 1 and ma.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        pedido = cursor.fetchone()

    pedido_elemento = None

    if pedido:
        pedido_id, pedido_nombre, logo_binario, banner_binario , pedido_disp = pedido

        if logo_binario:
            logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = ""  # Placeholder en caso de que no haya logo

        if banner_binario:
            banner_base64 = base64.b64encode(banner_binario).decode('utf-8')
            banner_url = f"data:image/png;base64,{banner_base64}"
        else:
            banner_url = ""  # Placeholder en caso de que no haya banner

        pedido_elemento = (pedido_id, pedido_nombre, logo_url, banner_url , pedido_disp)

    conexion.close()
    return pedido_elemento


def obtener_todas_pedidos_recientes():
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    id,
                    pedido, 
                    img_logo, 
                    img_banner,
                    fecha_registro,
                    disponibilidad
                FROM pedido 
                where disponibilidad = 1
                order by fecha_registro desc
                '''
        cursor.execute(sql)
        pedidos = cursor.fetchall()
    
    pedidos_lista = []
    for pedido in pedidos:
        pedido_id, pedido_nombre, logo_binario, img_bin , fec , disp= pedido
        if logo_binario:
            logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = ""  
        pedidos_lista.append((pedido_id, pedido_nombre, logo_url))
    
    conexion.close()
    return pedidos_lista


def obtener_pedidosXnombre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, pedido, img_logo FROM pedido order by pedido")
        pedidos = cursor.fetchall()
        
        # Convertir el logo binario a base64 para cada pedido
        pedidos_procesadas = []
        for pedido in pedidos:
            id_pedido = pedido[0]
            nombre_pedido = pedido[1]
            logo_binario = pedido[2]
            
            # Convertir el logo binario a una cadena base64
            if logo_binario:
                logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
                logo_formato = f"data:image/png;base64,{logo_base64}" 
            else:
                logo_formato = None 
            
            pedidos_procesadas.append((id_pedido, nombre_pedido, logo_formato))
    
    conexion.close()
    return pedidos_procesadas






def insertar_pedido(pedido, logo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO pedido(pedido, img_logo) VALUES (%s, %s)", (pedido, logo))
    conexion.commit()
    conexion.close()


def obtener_listado_pedidos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    m.id,
                    m.pedido, 
                    m.img_logo, 
                    m.img_banner,
                    m.fecha_registro,
                    m.disponibilidad,
                    COUNT(DISTINCT p.id) AS cantidad_productos,
                    COUNT(DISTINCT n.id) AS cantidad_novedades
                FROM 
                    pedido m
                LEFT JOIN 
                    producto p ON m.id = p.pedidoid
                LEFT JOIN 
                    novedad n ON m.id = n.pedidoid
                GROUP BY 
                    m.id, m.pedido, m.img_logo, m.img_banner, m.fecha_registro, m.disponibilidad;
                ''')
        pedidos = cursor.fetchall()
        
        # Convertir el logo binario a base64 para cada pedido
        pedidos_procesadas = []
        for pedido in pedidos:
            id_pedido = pedido[0]
            nombre_pedido = pedido[1]
            logo_binario = pedido[2]
            banner_binario = pedido[3]
            fecha = pedido[4]
            disp = pedido[5]
            cantPro = pedido[6]
            cantNov = pedido[7]
            
            if logo_binario:
                logo_base64 = base64.b64encode(logo_binario).decode('utf-8')
                logo_formato = f"data:image/png;base64,{logo_base64}" 
            else:
                logo_formato = None

            if banner_binario:
                logo_base64 = base64.b64encode(banner_binario).decode('utf-8')
                banner_formato = f"data:image/png;base64,{logo_base64}" 
            else:
                banner_formato = "" 
            
            pedidos_procesadas.append((id_pedido, nombre_pedido, logo_formato,banner_formato,fecha,disp,cantPro , cantNov))
    
    conexion.close()
    return pedidos_procesadas


def eliminar_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM pedido WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_pedido_por_id(id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, pedido,img_logo FROM pedido WHERE id = %s", (id,))
        pedido = cursor.fetchone()
    conexion.close()
    return pedido


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

def pedidos_para_novedad():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, pedido FROM pedido")
        pedidos = cursor.fetchall()  # Esto debe devolver una lista de tuplas o diccionarios
    conexion.close()
    return pedidos
