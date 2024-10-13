from bd import obtener_conexion
import base64
tabla = 'producto'



def obtener_por_id(id):
    conexion = obtener_conexion()
    productos = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id , 
                pr.nombre , 
                pr.price_regular , 
                pr.precio_online , 
                pr.precio_oferta , 
                pr.calificacion , 
                pr.info_adicional, 
                pr.stock , 
                pr.fecha_registro , 
                pr.MARCAid , 
                pr.SUBCATEGORIAid
            FROM producto pr
            where pr.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        productos = cursor.fetchone()
    conexion.close()
    return productos


def obtenerInformacionProducto(id):
    conexion = obtener_conexion()
    productos = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id , 
                pr.nombre , 
                pr.price_regular , 
                pr.precio_online , 
                pr.precio_oferta , 
                pr.calificacion , 
                pr.info_adicional, 
                pr.stock , 
                pr.fecha_registro , 
                pr.MARCAid , 
                pr.SUBCATEGORIAid
            FROM producto pr
            where pr.id = '''+ str(id) +'''
            '''
        cursor.execute(sql)
        productos = cursor.fetchone()
    conexion.close()
    return productos


def obtenerEnTarjetasMasRecientes():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id , 
                    pr.nombre , 
                    pr.price_regular , 
                    pr.precio_online , 
                    pr.precio_oferta ,  
                    pr.MARCAid , 
                    pr.SUBCATEGORIAid , 
                    ipr.imagen 
                FROM `producto` pr 
                inner join img_producto ipr 
                on pr.id = ipr.PRODUCTOid 
                where ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                order by pr.fecha_registro
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_binario = producto
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_url))
    
    conexion.close()
    return productos_lista



def obtenerEnTarjetas_Marca(marca, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id , 
                    pr.nombre , 
                    pr.price_regular , 
                    pr.precio_online , 
                    pr.precio_oferta ,  
                    pr.MARCAid , 
                    pr.SUBCATEGORIAid , 
                    ipr.imagen 
                FROM `producto` pr 
                inner join img_producto ipr 
                on pr.id = ipr.PRODUCTOid 
                where ipr.imgPrincipal = 1 and pr.disponibilidad = 1 and pr.marcaid = '''+str(marca)+'''
                order by pr.fecha_registro
                limit '''+str(limit)+''' 
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_binario = producto
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_url))
    
    conexion.close()
    return productos_lista



# def obtener():
#     conexion = obtener_conexion()
#     productos = []
#     with conexion.cursor() as cursor:
#         sql = ''' 
#         SELECT 
#         id , 
#         nombre , 
#         price_regular , 
#         precio_online , 
#         precio_oferta , 
#         calificacion , 
#         info_adicional, 
#         stock , 
#         fecha_registro , MARCAid , SUBCATEGORIAid FROM '''+tabla
#         cursor.execute(sql)
#         productos = cursor.fetchall()
#     conexion.close()
#     return productos





def obtenerEnTarjetasxMarca(marca):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id , 
                    pr.nombre , 
                    pr.price_regular , 
                    pr.precio_online , 
                    pr.precio_oferta ,  
                    pr.MARCAid , 
                    pr.SUBCATEGORIAid , 
                    ipr.imagen 
                FROM `producto` pr 
                inner join img_producto ipr 
                on pr.id = ipr.PRODUCTOid 
                where ipr.imgPrincipal = 1 and pr.disponibilidad = 1 and pr.marcaid = '''+str(marca)+'''
                order by pr.fecha_registro
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_binario = producto
        if img_binario:
            img_base64 = base64.b64encode(img_binario).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_url))
    
    conexion.close()
    return productos_lista


# def obtenerEnTarjetasxCategoria(categoria):
#     conexion = obtener_conexion()
#     productos = []
#     with conexion.cursor() as cursor:
#         sql = 'SELECT pr.id , pr.nombre , pr.price_regular , pr.precio_online , pr.precio_oferta , pr.calificacion , pr.infoAdicional , pr.stock , pr.fecha_registro , pr.MARCAid , pr.SUBCATEGORIAid , ipr.imgPrincipal, ipr.imagen FROM `producto` pr inner join imagenes_producto ipr on pr.id = ipr.PRODUCTOid where ipr.imgPrincipal = 1'
#         cursor.execute(sql)
#         productos = cursor.fetchall()
    
#     productos_lista = []
#     for producto in productos:
#         pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_cal , pr_info , pr_st , pr_fr , pr_mar , pr_sub, ipr_imgp, img_binario = producto
#         if img_binario:
#             img_base64 = base64.b64encode(img_binario).decode('utf-8')
#             img_url = f"data:image/png;base64,{img_base64}"
#         else:
#             img_url = ""  # Placeholder en caso de que no haya logo
#         productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_cal , pr_info , pr_st , pr_fr , pr_mar , pr_sub, ipr_imgp, img_url))
    
#     conexion.close()
#     return productos_lista


# def obtenerEnTarjetasMasPopulares():
#     conexion = obtener_conexion()
#     productos = []
#     with conexion.cursor() as cursor:
#         sql = 'SELECT pr.id , pr.nombre , pr.price_regular , pr.precio_online , pr.precio_oferta , pr.calificacion , pr.infoAdicional , pr.stock , pr.fecha_registro , pr.MARCAid , pr.SUBCATEGORIAid , ipr.imgPrincipal, ipr.imagen FROM `producto` pr inner join imagenes_producto ipr on pr.id = ipr.PRODUCTOid where ipr.imgPrincipal = 1'
#         cursor.execute(sql)
#         productos = cursor.fetchall()
    
#     productos_lista = []
#     for producto in productos:
#         pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_cal , pr_info , pr_st , pr_fr , pr_mar , pr_sub, ipr_imgp, img_binario = producto
#         if img_binario:
#             img_base64 = base64.b64encode(img_binario).decode('utf-8')
#             img_url = f"data:image/png;base64,{img_base64}"
#         else:
#             img_url = ""  # Placeholder en caso de que no haya logo
#         productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_cal , pr_info , pr_st , pr_fr , pr_mar , pr_sub, ipr_imgp, img_url))
    
#     conexion.close()
#     return productos_lista


# def obtenerEnTarjetasMasRecientes():
#     conexion = obtener_conexion()
#     productos = []
#     with conexion.cursor() as cursor:
#         sql = 'SELECT pr.id , pr.nombre , pr.price_regular , pr.precio_online , pr.precio_oferta , pr.calificacion , pr.infoAdicional , pr.stock , pr.fecha_registro , pr.MARCAid , pr.SUBCATEGORIAid , ipr.imgPrincipal, ipr.imagen FROM `producto` pr inner join imagenes_producto ipr on pr.id = ipr.PRODUCTOid where ipr.imgPrincipal = 1'
#         cursor.execute(sql)
#         productos = cursor.fetchall()
    
#     productos_lista = []
#     for producto in productos:
#         pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_cal , pr_info , pr_st , pr_fr , pr_mar , pr_sub, ipr_imgp, img_binario = producto
#         if img_binario:
#             img_base64 = base64.b64encode(img_binario).decode('utf-8')
#             img_url = f"data:image/png;base64,{img_base64}"
#         else:
#             img_url = ""  # Placeholder en caso de que no haya logo
#         productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_cal , pr_info , pr_st , pr_fr , pr_mar , pr_sub, ipr_imgp, img_url))
    
#     conexion.close()
#     return productos_lista












# def insertar_disco(codigo, nombre, artista, precio, genero):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("INSERT INTO discos(codigo, nombre, artista, precio, genero) VALUES (%s, %s, %s, %s, %s)",
#                        (codigo, nombre, artista, precio, genero))
#     conexion.commit()
#     conexion.close()



# def eliminar_disco(id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("DELETE FROM discos WHERE id = %s", (id,))
#     conexion.commit()
#     conexion.close()


# def obtener_disco_por_id(id):
#     conexion = obtener_conexion()
#     juego = None
#     with conexion.cursor() as cursor:
#         cursor.execute(
#             "SELECT id, codigo, nombre, artista, precio, genero FROM discos WHERE id = %s", (id,))
#         juego = cursor.fetchone()
#     conexion.close()
#     return juego


# def actualizar_disco(codigo, nombre, artista, precio, genero, id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("UPDATE discos SET codigo = %s, nombre = %s, artista = %s, precio = %s, genero = %s WHERE id = %s",
#                        (codigo, nombre, artista, precio, genero, id))
#     conexion.commit()
#     conexion.close()
