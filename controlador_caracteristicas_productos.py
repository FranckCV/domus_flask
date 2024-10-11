from bd import obtener_conexion
import base64
tabla = 'caracteristica_producto'


def obtenerCaracteristicasxProducto(id,valor):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                csc.campo,
                cpr.valor
            FROM caracteristica_producto cpr
            inner join caracteristica_subcat csc on csc.id = cpr.caracteristica_subcatid
            where cpr.productoid = '''+ str(id) +''' and cpr.principal = '''+str(valor)+'''
            order by csc.campo
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas






