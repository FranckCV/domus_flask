from bd import obtener_conexion
import base64
tabla = 'producto'

def obtener_imagenes_por_producto(id):
    conexion = obtener_conexion()
    imagenes = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ipr.id ,
                ipr.imagen,
                ipr.imgPrincipal
            FROM img_producto ipr
            where ipr.productoid = '''+str(id)+'''
            order by ipr.imgPrincipal desc
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        id, img , prin= imagen
        if imagen:
            img_base64 = base64.b64encode(img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        imagenes_lista.append((id, img_url , prin))

    conexion.close()
    return imagenes_lista


def obtener_img_principal_por_producto(id):
    conexion = obtener_conexion()
    imagenes = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ipr.id ,
                ipr.imagen
            FROM img_producto ipr
            where ipr.productoid = '''+str(id)+''' and ipr.imgPrincipal = 1
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchone()
    conexion.close()
    return imagenes


def insertar_img_producto(nombre, imagen, principal, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO img_producto(img_nombre, imagen, imgprincipal, productoid)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, imagen, principal, producto_id))
    conexion.commit()
    conexion.close()


def actualizar_img_producto(imagen, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE img_producto 
            SET imagen = %s 
            WHERE productoid = %s and imgPrincipal = 1
        '''
        cursor.execute(sql, (imagen, id))
    conexion.commit()
    conexion.close()






# def obtenerEnTarjetasxMarca(marca):
#     conexion = obtener_conexion()
#     productos = []
#     with conexion.cursor() as cursor:
#         sql = '''
#                 SELECT pr.id , pr.nombre , pr.price_regular , pr.precio_online , pr.precio_oferta ,  
#                 pr.MARCAid , pr.SUBCATEGORIAid , ipr.imagen 
#                 FROM `producto` pr 
#                 inner join img_producto ipr on pr.id = ipr.PRODUCTOid 
#                 where ipr.imgPrincipal = 1 and pr.marcaid = '''+str(marca)+'''
#             '''
#         cursor.execute(sql)
#         productos = cursor.fetchall()
    
#     productos_lista = []
#     for producto in productos:
#         pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_binario = producto
#         if img_binario:
#             img_base64 = base64.b64encode(img_binario).decode('utf-8')
#             img_url = f"data:image/png;base64,{img_base64}"
#         else:
#             img_url = ""  # Placeholder en caso de que no haya logo
#         productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar , pr_sub, img_url))
    
#     conexion.close()
#     return productos_lista


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


