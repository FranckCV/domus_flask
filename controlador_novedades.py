from bd import obtener_conexion
import base64

def obtenerBannersNovedadesRecientes():
    conexion = obtener_conexion()
    elementos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    MIN(imnov.imagen) AS imagen, 
                    nov.nombre
                FROM 
                    novedad nov
                INNER JOIN 
                    img_novedad imnov ON nov.id = imnov.NOVEDADid 
                WHERE 
                    imnov.TIPO_IMG_NOVEDADid = 1 
                    AND nov.disponibilidad = 1
                GROUP BY 
                    nov.id, nov.nombre
                ORDER BY 
                    nov.fecha_registro DESC
                LIMIT 6;
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    banners_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom = dato

        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        banners_lista.append((nov_id, img_url, nov_nom))
        
    conexion.close()
    return banners_lista


def obtenerTiposNovedades():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    tn.nomTipo 
                FROM `tipo_novedad` tn
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()    
    
    conexion.close()
    return productos


def obtenerTodasLasNovedades():
    conexion = obtener_conexion()
    novedades = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                nov.id, 
                nov.nombre, 
                nov.titulo, 
                nov.fecha_inicio, 
                nov.fecha_vencimiento, 
                nov.terminos, 
                nov.fecha_registro, 
                nov.disponibilidad,
                nov.MARCAid, 
                nov.SUBCATEGORIAid, 
                nov.TIPO_NOVEDADid
            FROM 
                novedad nov
            ORDER BY 
                nov.fecha_registro DESC;
        '''
        cursor.execute(sql)
        novedades = cursor.fetchall()
    conexion.close()
    return novedades


def obtenerPromocionesTarjetas():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    MIN(imnov.imagen) AS imagen, 
                    nov.nombre
                FROM 
                    novedad nov
                INNER JOIN 
                    img_novedad imnov ON nov.id = imnov.NOVEDADid 
                WHERE 
                    imnov.TIPO_IMG_NOVEDADid = 1 
                    AND nov.disponibilidad = 1
                GROUP BY 
                    nov.id, nov.nombre
                ORDER BY 
                    nov.fecha_registro DESC
                LIMIT 6;
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    banners_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom = dato

        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        banners_lista.append((nov_id, img_url, nov_nom))
        
    conexion.close()
    return banners_lista


def obtenerNovedadesMarca(marca):
    conexion = obtener_conexion()
    elementos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    Min(imnov.imagen) as novImagen,
                    nov.nombre,
                    imnov.tipo_img_novedadid
                FROM 
                    novedad nov
                INNER JOIN 
                    img_novedad imnov ON nov.id = imnov.NOVEDADid 
                WHERE 
                    nov.disponibilidad = 1 and nov.MARCAid = '''+str(marca)+'''
                GROUP BY 
                    nov.id
                ORDER BY 
                    nov.fecha_registro DESC , imnov.tipo_img_novedadid desc
                LIMIT 4
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    novedades_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom , nov_tipo = dato

        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        novedades_lista.append((nov_id, img_url, nov_nom , nov_tipo))
        
    conexion.close()
    return novedades_lista


def obtenerNovedadesCategoria(categoria):
    conexion = obtener_conexion()
    elementos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    Min(imnov.imagen) as novImagen,
                    nov.nombre,
                    imnov.tipo_img_novedadid
                FROM 
                    novedad nov
                INNER JOIN 
                    img_novedad imnov ON nov.id = imnov.NOVEDADid
                WHERE 
                    nov.disponibilidad = 1 and nov.MARCAid in (
                        SELECT DISTINCT 
                        	m.id 
                        FROM SUBCATEGORIA s 
                        INNER JOIN PRODUCTO p ON p.SUBCATEGORIAid = s.id 
                        INNER JOIN MARCA m ON m.id = p.MARCAid 
                        WHERE s.disponibilidad = 1 AND m.disponibilidad = 1
                        and s.CATEGORIAid = '''+str(categoria)+'''
                    ) or nov.SUBCATEGORIAid in (
                    	SELECT 
                        	sub.id 
                        FROM SUBCATEGORIA sub
                        WHERE sub.disponibilidad = 1 and sub.CATEGORIAid = '''+str(categoria)+'''
                    )
                GROUP BY 
                    nov.id
                ORDER BY 
                    nov.fecha_registro DESC , imnov.tipo_img_novedadid desc
                LIMIT 4;
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    novedades_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom , nov_tipo = dato

        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        novedades_lista.append((nov_id, img_url, nov_nom , nov_tipo))
        
    conexion.close()
    return novedades_lista


def obtenerNovedadesRecientes():
    conexion = obtener_conexion()
    elementos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    Min(imnov.imagen) as novImagen,
                    nov.nombre,
                    imnov.tipo_img_novedadid
                FROM 
                    novedad nov
                INNER JOIN 
                    img_novedad imnov ON nov.id = imnov.NOVEDADid 
                WHERE 
                    nov.disponibilidad = 1 and imnov.tipo_img_novedadid != 1
                GROUP BY 
                    nov.id
                ORDER BY 
                    nov.fecha_registro DESC , imnov.tipo_img_novedadid
                LIMIT 4
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    img_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom , nov_tipo = dato

        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        img_lista.append((nov_id, img_url, nov_nom , nov_tipo))
        
    conexion.close()
    return img_lista


def mostrarNovedadesPromociones():
    conexion = obtener_conexion()
    elementos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    MIN(imgnov.imagen),
                    nov.titulo
                FROM novedad nov
                INNER JOIN img_novedad imgnov on imgnov.NOVEDADid = nov.id
                WHERE nov.disponibilidad = 1 and nov.TIPO_NOVEDADid = 3
                Group by nov.id
                order by nov.fecha_registro desc;
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    img_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom  = dato
        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        img_lista.append((nov_id, img_url, nov_nom))
    conexion.close()
    return img_lista


def promoselect(id):
    conexion = obtener_conexion()
    promo = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                nov.`id`, 
                nov.titulo,
                nov.`fecha_inicio`, 
                nov.`fecha_vencimiento`, 
                nov.`terminos`, 
                nov.`MARCAid`, 
                nov.`SUBCATEGORIAid`,
                MIN(imgnov.imagen),
                mar.marca
            FROM `novedad` nov
            INNER JOIN img_novedad imgnov on imgnov.NOVEDADid = nov.id
            INNER JOIN marca mar on mar.id = nov.MARCAid
            WHERE nov.disponibilidad = 1 AND nov.TIPO_NOVEDADid = 3 and nov.id = '''+str(id)+'''
            Group by nov.id
        '''
        cursor.execute(sql)
        promo = cursor.fetchone()

        elemento_promo = None

        if promo:
            pro_id, pro_titulo, pro_fecini, pro_fecven , pro_ter , pro_mar , pro_sub , pro_img , mar_nom = promo

            if pro_img:
                logo_base64 = base64.b64encode(pro_img).decode('utf-8')
                logo_url = f"data:image/png;base64,{logo_base64}"
            else:
                logo_url = "" 

        elemento_promo = (pro_id, pro_titulo, pro_fecini, pro_fecven , pro_ter , pro_mar , pro_sub , logo_url , mar_nom)

    conexion.close()
    return elemento_promo

def mostrarNovedadesAnuncios():
    conexion = obtener_conexion()
    elementos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    nov.id, 
                    MIN(imgnov.imagen),
                    nov.titulo
                FROM novedad nov
                INNER JOIN img_novedad imgnov on imgnov.NOVEDADid = nov.id
                WHERE nov.disponibilidad = 1 and nov.TIPO_NOVEDADid = 1
                Group by nov.id
                order by nov.fecha_registro desc;
            '''
        cursor.execute(sql)
        elementos = cursor.fetchall()   

    img_lista = []
    for dato in elementos:
        nov_id, nov_img, nov_nom  = dato
        if nov_img:
            logo_base64 = base64.b64encode(nov_img).decode('utf-8')
            img_url = f"data:image/png;base64,{logo_base64}"
        else:
            img_url = ""
        
        img_lista.append((nov_id, img_url, nov_nom))
    conexion.close()
    return img_lista


def anuncioselect(id):
    conexion = obtener_conexion()
    anuncio = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                nov.id, 
                nov.titulo,
                nov.fecha_inicio, 
                nov.fecha_vencimiento, 
                nov.terminos, 
                nov.MARCAid, 
                nov.SUBCATEGORIAid,
                MIN(imgnov.imagen),
                mar.marca
            FROM novedad nov
            INNER JOIN img_novedad imgnov on imgnov.NOVEDADid = nov.id
            INNER JOIN marca mar on mar.id = nov.MARCAid
            WHERE nov.disponibilidad = 1 AND nov.TIPO_NOVEDADid = 1 and nov.id = %s
            Group by nov.id
        '''
        cursor.execute(sql, (id,))
        anuncio = cursor.fetchone()

    conexion.close()

    if anuncio:
        pro_id, pro_titulo, pro_fecini, pro_fecven, pro_ter, pro_mar, pro_sub, pro_img, mar_nom = anuncio

        # Convertir imagen a base64 si existe
        if pro_img:
            logo_base64 = base64.b64encode(pro_img).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = "" 

        return (pro_id, pro_titulo, pro_fecini, pro_fecven, pro_ter, pro_mar, pro_sub, logo_url, mar_nom)

    return None




# Insertar una novedad
def insertarNovedad(nombre, titulo, fechaInicio, fechaVencimiento, terminos, disponibilidad, marcaId, subcategoriaId, tipoNovedadId):
    novedadId = None
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO novedad (nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, MARCAid, SUBCATEGORIAid, TIPO_NOVEDADid, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
        '''
        cursor.execute(sql, (nombre, titulo, fechaInicio, fechaVencimiento, terminos, disponibilidad, marcaId, subcategoriaId, tipoNovedadId))
        novedadId = cursor.lastrowid
    
    conexion.commit()
    conexion.close()
    return novedadId

# Actualizar una novedad
def actualizarNovedad(nombre, titulo, fechaInicio, fechaVencimiento, terminos, disponibilidad, marcaId, subcategoriaId, tipoNovedadId, imagen, novedadId):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE novedad
            SET nombre = %s, titulo = %s, fecha_inicio = %s, fecha_vencimiento = %s, terminos = %s, disponibilidad = %s, MARCAid = %s, SUBCATEGORIAid = %s, TIPO_NOVEDADid = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre, titulo, fechaInicio, fechaVencimiento, terminos, disponibilidad, marcaId, subcategoriaId, tipoNovedadId, novedadId))
        
        if imagen:
            insertarImagenNovedad(novedadId, imagen)

    conexion.commit()
    conexion.close()

# Eliminar una novedad
def eliminarNovedad(novedadId):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM novedad WHERE id = %s", (novedadId,))
    conexion.commit()
    conexion.close()

# Obtener una novedad por ID
def obtenerNovedadPorId(novedadId):
    conexion = obtener_conexion()
    novedad = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, MARCAid, SUBCATEGORIAid, TIPO_NOVEDADid FROM novedad WHERE id = %s", (novedadId,))
        novedad = cursor.fetchone()
    conexion.close()
    return novedad

# Insertar una imagen para la novedad
# def insertarImagenNovedad(novedadId, imagen):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             INSERT INTO img_novedad (imagen, NOVEDADid, TIPO_IMG_NOVEDADid)
#             VALUES (%s, %s, %s)
#         '''
#         cursor.execute(sql, (imagen, novedadId, 2))  # 2 asumiendo que 2 es el tipo de imagen para novedades
#     conexion.commit()
#     conexion.close()

# def insertarImagenNovedad(nomImagen, imagen, tipo_img_novedad_id, novedad_id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             INSERT INTO IMG_NOVEDAD (nomImagen, imagen, TIPO_IMG_NOVEDADid, NOVEDADid)
#             VALUES (%s, %s, %s, %s)
#         '''
#         cursor.execute(sql, (nomImagen, imagen, tipo_img_novedad_id, novedad_id))
#     conexion.commit()
#     conexion.close()

# def obtenerImagenesNovedad(novedad_id):
#     conexion = obtener_conexion()
#     imagenes = []
#     with conexion.cursor() as cursor:
#         sql = '''
#             SELECT 
#                 id, 
#                 nomImagen, 
#                 imagen, 
#                 TIPO_IMG_NOVEDADid 
#             FROM IMG_NOVEDAD 
#             WHERE NOVEDADid = %s
#         '''
#         cursor.execute(sql, (novedad_id,))
#         imagenes = cursor.fetchall()
    
#     conexion.close()
#     return imagenes

# def obtenerImagenNovedadPorId(id):
#     conexion = obtener_conexion()
#     imagen_novedad = None
#     with conexion.cursor() as cursor:
#         sql = '''
#             SELECT 
#                 id, 
#                 nomImagen, 
#                 imagen, 
#                 TIPO_IMG_NOVEDADid 
#             FROM IMG_NOVEDAD
#             WHERE id = %s
#         '''
#         cursor.execute(sql, (id,))
#         imagen_novedad = cursor.fetchone()
    
#     conexion.close()
#     return imagen_novedad

# def actualizarImagenNovedad(nomImagen, imagen, tipo_img_novedad_id, id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             UPDATE IMG_NOVEDAD
#             SET nomImagen = %s, imagen = %s, TIPO_IMG_NOVEDADid = %s
#             WHERE id = %s
#         '''
#         cursor.execute(sql, (nomImagen, imagen, tipo_img_novedad_id, id))
#     conexion.commit()
#     conexion.close()

# def eliminarImagenNovedad(id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             DELETE FROM IMG_NOVEDAD
#             WHERE id = %s
#         '''
#         cursor.execute(sql, (id,))
#     conexion.commit()
#     conexion.close()

# def eliminarImagenNovedad(id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             DELETE FROM IMG_NOVEDAD
#             WHERE id = %s
#         '''
#         cursor.execute(sql, (id,))
#     conexion.commit()
#     conexion.close()

# def eliminarImagenNovedad(id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             DELETE FROM IMG_NOVEDAD
#             WHERE id = %s
#         '''
#         cursor.execute(sql, (id,))
#     conexion.commit()
#     conexion.close()
