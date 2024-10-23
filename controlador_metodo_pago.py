from bd import obtener_conexion
def obtener_Metodo_pago():
    conexion=obtener_conexion()
    metodo=[]
    with conexion.cursor() as cursor:
        sql="select id,metodo from metodo_pago"
        cursor.execute(sql)
        metodo=cursor.fetchall
    conexion.commit
    return metodo