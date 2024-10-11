from bd import obtener_conexion
tabla = 'categoria'

def obtener_categorias():
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = 'SELECT id, categoria, faicon_cat, disponibilidad FROM '+tabla + ' where disponibilidad = 1'
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias

def obtener_categoria_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    with conexion.cursor() as cursor:
        sql = 'SELECT id, categoria, faicon_cat, disponibilidad FROM '+tabla + ' where id = '+str(id)
        cursor.execute(sql)
        categoria = cursor.fetchone()    
    return categoria





