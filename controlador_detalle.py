from bd import obtener_conexion
import base64

def obtener_Detalle():
    conexion = obtener_conexion()
    productos = []
    productos_lista = []

    with conexion.cursor() as cursor:
        sql = '''
            SELECT IMP.imagen, P.nombre, DP.cantidad, DP.PRODUCTOid 
            FROM detalles_pedido DP
            INNER JOIN producto P ON P.id = DP.PRODUCTOid
            inner join pedido Pe on Pe.id=DP.PEDIDOid
            INNER JOIN img_producto IMP ON P.id = IMP.PRODUCTOid
            WHERE IMP.imgPrincipal = 1 and Pe.ESTADO_PEDIDOid=1
        '''
        cursor.execute(sql)
        productos = cursor.fetchall()
        
        for producto in productos:
            sql_precios = "SELECT price_regular, precio_online, precio_oferta FROM producto WHERE id = %s"
            cursor.execute(sql_precios, (producto[3],))  # Se debe pasar como una tuplita
            precios = cursor.fetchone()

            if precios[2] is not None:  # precio_oferta
                precio_final = precios[2]
            elif precios[1] is not None:  # precio_online
                precio_final = precios[1]
            else:  # precio_regular
                precio_final = precios[0]

            # Codificar la imagen en base64 porque está en binarie
            img_binario = producto[0] 
            if img_binario:
                imagen_base64 = base64.b64encode(img_binario).decode('utf-8')
                imagen = f"data:image/png;base64,{imagen_base64}"
            else:
                imagen = "" 

            nombre = producto[1]  
            cantidad = producto[2]  
            producto_id = producto[3]  

            productos_lista.append((imagen, nombre, precio_final, cantidad, producto_id))
    
    conexion.close()
    return productos_lista


########################################


def obtener_Detalle_por_Id(id):
    conexion = obtener_conexion()
    productos_lista = []

    try:
        with conexion.cursor() as cursor:
            # Consulta principal para obtener los productos del pedido
            sql = '''
                SELECT IMP.imagen, P.nombre, DP.cantidad, DP.PRODUCTOid 
                FROM detalles_pedido DP
                INNER JOIN producto P ON P.id = DP.PRODUCTOid
                INNER JOIN pedido PE ON PE.id = DP.PEDIDOid
                INNER JOIN img_producto IMP ON P.id = IMP.PRODUCTOid
                WHERE IMP.imgPrincipal = 1 AND PE.id = %s
            '''
            cursor.execute(sql, (id,))
            productos = cursor.fetchall()

            for producto in productos:
                sql_precios = "SELECT price_regular, precio_online, precio_oferta FROM producto WHERE id = %s"
                cursor.execute(sql_precios, (producto[3],))
                precios = cursor.fetchone()

                if precios is not None:
                    precio_final = precios[2] if precios[2] is not None else precios[1] if precios[1] is not None else precios[0]
                else:
                    precio_final = 0  

                img_binario = producto[0]
                imagen = f"data:image/png;base64,{base64.b64encode(img_binario).decode('utf-8')}" if img_binario else ""

                nombre = producto[1]
                cantidad = producto[2]
                producto_id = producto[3]

                productos_lista.append((imagen, nombre, precio_final, cantidad, producto_id))

    except Exception as e:
        print(f"Error al obtener detalles: {e}")
    finally:
        conexion.close() 

    return productos_lista

def eliminar_detalle(producto_id, pedido_id):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM detalles_pedido WHERE PRODUCTOid=%s AND PEDIDOid=%s"
            cursor.execute(sql, (producto_id, pedido_id))
            conexion.commit() 
    except Exception as e:
        print(f"Error al eliminar detalle: {e}")
    finally:
        conexion.close()

def editar_detalle(producto_id, pedido_id, nueva_cantidad):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            # Actualizamos la cantidad de un producto en un pedido específico.
            sql = "UPDATE detalles_pedido SET cantidad=%s WHERE PRODUCTOid=%s AND PEDIDOid=%s"
            cursor.execute(sql, (nueva_cantidad, producto_id, pedido_id))
            conexion.commit()
            print(f"Detalle del producto {producto_id} en el pedido {pedido_id} actualizado correctamente.")
    except Exception as e:
        print(f"Error al editar detalle: {e}")
    finally:
        conexion.close()
