from bd import obtener_conexion
tabla = 'categoria'

def obtenerSubcategoriasXCategoria(categoria):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT su.id , su.subcategoria , su.faicon_subcat
            FROM categoria ca
            inner join subcategoria su on su.CATEGORIAid = ca.id
            where su.disponibilidad = 1 and ca.id = '''+str(categoria)+'''
            order by su.subcategoria;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias


def obtenerSubcategoriasXCategoria(categoria):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT su.id , su.subcategoria , su.faicon_subcat
            FROM categoria ca
            inner join subcategoria su on su.CATEGORIAid = ca.id
            where su.disponibilidad = 1 and ca.id = '''+str(categoria)+'''
            order by su.subcategoria;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias
