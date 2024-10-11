from bd import obtener_conexion
import base64
tabla = 'novedad'


# def obtenerBannersNovedadesRecientes():
#     conexion = obtener_conexion()
#     productos = []
#     with conexion.cursor() as cursor:
#         sql = '''
#                 SELECT 
#                     tn.nomTipo 
#                 FROM `tipo_novedad` tn 
#                 inner join img_producto ipr 
#                 on pr.id = ipr.PRODUCTOid 
#                 where ipr.imgPrincipal = 1 and pr.disponibilidad = 1
#                 order by pr.fecha_registro
#             '''
#         cursor.execute(sql)
#         productos = cursor.fetchall()    
    
#     conexion.close()
#     return productos



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






