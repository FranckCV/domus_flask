from bd import obtener_conexion
import base64

def obtener_Detalle():
    conexion = obtener_conexion()
    productos = []
    productos_lista = []

    with conexion.cursor() as cursor:
        # Consulta para obtener los productos y su imagen principal
        sql = '''
            SELECT IMP.imagen, P.nombre, DP.cantidad, DP.PRODUCTOid 
            FROM detalles_pedido DP
            INNER JOIN producto P ON P.id = DP.PRODUCTOid
            INNER JOIN img_producto IMP ON P.id = IMP.PRODUCTOid
            WHERE IMP.imgPrincipal = 1
        '''
        cursor.execute(sql)
        productos = cursor.fetchall()
        
        # Iterar sobre los productos obtenidos
        for producto in productos:
            sql_precios = "SELECT price_regular, precio_online, precio_oferta FROM producto WHERE id = %s"
            cursor.execute(sql_precios, (producto[3],))  # Nota: Se debe pasar como una tupla
            precios = cursor.fetchone()

            if precios[2] is not None:  # precio_oferta
                precio_final = precios[2]
            elif precios[1] is not None:  # precio_online
                precio_final = precios[1]
            else:  # precio_regular
                precio_final = precios[0]

            # Codificar la imagen en base64 (si está en formato binario)
            img_binario = producto[0] 
            if img_binario:
                imagen_base64 = base64.b64encode(img_binario).decode('utf-8')
                imagen = f"data:image/png;base64,{imagen_base64}"
            else:
                imagen = ""  # Si no hay imagen

            nombre = producto[1]  
            cantidad = producto[2]  
            producto_id = producto[3]  

            # Agregar a la lista de productos
            productos_lista.append((imagen, nombre, precio_final, cantidad, producto_id))
    
    conexion.close()
    return productos_lista
