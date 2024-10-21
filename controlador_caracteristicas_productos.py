from bd import obtener_conexion
import base64


def obtenerCaracteristicasxProducto(id,valor):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                car.campo,
                cpr.valor
            FROM caracteristica_producto cpr
            inner join caracteristica car on car.id = cpr.CARACTERISTICAid
            inner join caracteristica_subcategoria csc on csc.CARACTERISTICAid = cpr.CARACTERISTICAid
            where cpr.productoid = '''+str(id)+''' and cpr.principal = '''+str(valor)+'''
            order by car.campo
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas






