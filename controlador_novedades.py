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
                INNER JOIN img_novedad imnov ON nov.id = imnov.NOVEDADid
                Left join tipo_img_novedad tip on tip.id = imnov.tipo_img_novedadid
                WHERE 
                    imnov.TIPO_IMG_NOVEDADid = 1 
                    AND nov.disponibilidad = 1
                    and tip.disponibilidad = 1
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


def obtener_listado_novedades():
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
                tip.id,
                sub.disponibilidad,
                cat.disponibilidad,
                mar.disponibilidad,
                count(img.id),
                (
                    SELECT 
                        img_n.id
                    FROM 
                        img_novedad img_n
                    left join tipo_img_novedad tip on tip.id = img_n.tipo_img_novedadid
                    WHERE 
                        img_n.NOVEDADid = nov.id
                        and tip.disponibilidad = 1
                    ORDER BY 
                        OCTET_LENGTH(img_n.imagen) DESC 
                    LIMIT 1
                ),
                tip.disponibilidad
            FROM novedad nov
            left join img_novedad img on img.NOVEDADid = nov.id
            left join tipo_novedad tip on tip.id = nov.TIPO_NOVEDADid
            left join subcategoria sub on sub.id = nov.subcategoriaid
            left join categoria cat on cat.id = sub.categoriaid
            left join marca mar on mar.id = nov.marcaid
            GROUP by nov.id;
        '''
        cursor.execute(sql)
        novedades = cursor.fetchall()
    conexion.close()
    return novedades


def obtener_info_novedad_id(id):
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
                tip.id,
                sub.disponibilidad,
                cat.disponibilidad,
                mar.disponibilidad,
                count(img.id) as cant_imgs,
                (
                    SELECT 
                        img_n.id
                    FROM 
                        img_novedad img_n
                    WHERE 
                        img_n.NOVEDADid = nov.id 
                    ORDER BY 
                        OCTET_LENGTH(img_n.imagen) DESC 
                    LIMIT 1
                )
            FROM novedad nov
            left join img_novedad img on img.NOVEDADid = nov.id
            left join tipo_novedad tip on tip.id = nov.TIPO_NOVEDADid
            left join subcategoria sub on sub.id = nov.subcategoriaid
            left join categoria cat on cat.id = sub.categoriaid
            left join marca mar on mar.id = nov.marcaid
            where nov.id = '''+str(id)+''' and nov.disponibilidad = 1 and
            	((nov.MARCAid is not null and mar.disponibilidad = 1) or nov.MARCAid is null) and
                ((nov.SUBCATEGORIAid is not null and sub.disponibilidad = 1) or nov.SUBCATEGORIAid is null) AND
                ((nov.SUBCATEGORIAid is not null and cat.disponibilidad = 1) or nov.SUBCATEGORIAid is null)
            GROUP by nov.id
            HAVING cant_imgs > 0;
        '''
        cursor.execute(sql)
        novedades = cursor.fetchone()
    conexion.close()
    return novedades


def buscar_listado_novedades_nombre_titulo(texto):
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
                tip.id,
                sub.disponibilidad,
                cat.disponibilidad,
                mar.disponibilidad,
                count(img.id),
                (
                    SELECT 
                        img_n.id
                    FROM 
                        img_novedad img_n
                    WHERE 
                        img_n.NOVEDADid = nov.id 
                    ORDER BY 
                        OCTET_LENGTH(img_n.imagen) DESC 
                    LIMIT 1
                )
            FROM novedad nov
            left join img_novedad img on img.NOVEDADid = nov.id
            left join tipo_novedad tip on tip.id = nov.TIPO_NOVEDADid
            left join subcategoria sub on sub.id = nov.subcategoriaid
            left join categoria cat on cat.id = sub.categoriaid
            left join marca mar on mar.id = nov.marcaid
            WHERE UPPER(nov.nombre) LIKE UPPER ('%'''+str(texto)+'''%') OR UPPER(nov.titulo) LIKE UPPER ('%'''+str(texto)+'''%')
            GROUP by nov.id
            ORDER BY nov.nombre , nov.titulo;
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
                INNER JOIN img_novedad imnov ON nov.id = imnov.NOVEDADid
                Left join tipo_img_novedad tip on tip.id = imnov.tipo_img_novedadid
                WHERE 
                    nov.disponibilidad = 1 and imnov.tipo_img_novedadid != 1 
                    and tip.disponibilidad = 1
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


def anuncioSelect(id):
    conexion = obtener_conexion()
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
            LEFT JOIN img_novedad imgnov on imgnov.NOVEDADid = nov.id
            LEFT JOIN marca mar on mar.id = nov.MARCAid
            WHERE nov.disponibilidad = 1 AND nov.TIPO_NOVEDADid = 1 and nov.id = '''+str(id)+'''
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


def insertarNovedad(nombre, titulo, fechaInicio, fechaVencimiento, terminos, marcaId, subcategoriaId, tipoNovedadId):
    novedadId = None
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO novedad (nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, MARCAid, SUBCATEGORIAid, TIPO_NOVEDADid, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, 1, %s, %s, %s, CURRENT_DATE)
        '''
        cursor.execute(sql, (nombre, titulo, fechaInicio, fechaVencimiento, terminos, marcaId, subcategoriaId, tipoNovedadId))
        novedadId = cursor.lastrowid
    
    conexion.commit()
    conexion.close()
    return novedadId


def actualizarNovedad(nombre, titulo, fechaInicio, fechaVencimiento, terminos, disponibilidad, marcaId, subcategoriaId, tipoNovedadId, imagen, novedadId):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE novedad
            SET nombre = %s, titulo = %s, fecha_inicio = %s, fecha_vencimiento = %s, terminos = %s, disponibilidad = %s, MARCAid = %s, SUBCATEGORIAid = %s, TIPO_NOVEDADid = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre, titulo, fechaInicio, fechaVencimiento, terminos, disponibilidad, marcaId, subcategoriaId, tipoNovedadId, novedadId))
        
        # if imagen:
        #     insertarImagenNovedad(novedadId, imagen)

    conexion.commit()
    conexion.close()


def eliminarNovedad(novedadId):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM novedad WHERE id = %s", (novedadId,))
    conexion.commit()
    conexion.close()


def obtenerNovedadPorId(novedadId):
    conexion = obtener_conexion()
    novedad = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, MARCAid, SUBCATEGORIAid, TIPO_NOVEDADid FROM novedad WHERE id = %s", (novedadId,))
        novedad = cursor.fetchone()
    conexion.close()
    return novedad


def actualizarImagenNovedad(nomImagen, imagen, tipo_img_novedad_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE IMG_NOVEDAD
            SET nomImagen = %s, imagen = %s, TIPO_IMG_NOVEDADid = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nomImagen, imagen, tipo_img_novedad_id, id))
    conexion.commit()
    conexion.close()


def eliminarImagenNovedad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            DELETE FROM IMG_NOVEDAD
            WHERE id = %s
        '''
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()
    

def obtener_novedad_id(id):
    conexion = obtener_conexion()
    novedad = None
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
                    nov.TIPO_NOVEDADid,
                    sub.categoriaid
                FROM novedad nov
                left join subcategoria sub on sub.id = nov.SUBCATEGORIAid 
                WHERE nov.id = '''+str(id)+'''
            '''
        cursor.execute(sql)
        novedad = cursor.fetchone()
    conexion.close()
    return novedad

