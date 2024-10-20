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






