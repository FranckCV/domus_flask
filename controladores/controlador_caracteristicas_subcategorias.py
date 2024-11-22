from controladores.bd import obtener_conexion
import base64


def obtenerCaracteristicasxSubcategoria(subcategoria):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                sub.id,
                sub.subcategoria,
                car.id,
                car.campo
            FROM caracteristica car
            INNER JOIN caracteristica_subcategoria csc on csc.CARACTERISTICAid = car.id
            INNER JOIN subcategoria sub on sub.id = csc.SUBCATEGORIAid
            where sub.id = '''+str(subcategoria)+'''
            order by sub.subcategoria
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas


def obtenerCaracteristicas_Subcategorias():
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                car.id,
                car.campo,
                car.disponibilidad,
                sub.id,
                sub.subcategoria,
                sub.faicon_subcat,
                sub.CATEGORIAid,
                cat.categoria,
                cat.faicon_cat
            FROM caracteristica car
            LEFT JOIN caracteristica_subcategoria csc on csc.CARACTERISTICAid = car.id
            LEFT JOIN subcategoria sub on sub.id = csc.SUBCATEGORIAid
            LEFT JOIN categoria cat on cat.id = sub.CATEGORIAid 
            order by car.id asc , sub.subcategoria 
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas



