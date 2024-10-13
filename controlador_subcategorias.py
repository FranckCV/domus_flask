from bd import obtener_conexion
tabla = 'categoria'


def obtenerSubcategoriasXCategoria(categoria):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                su.id , 
                su.subcategoria , 
                su.faicon_subcat
            FROM categoria ca
            inner join subcategoria su on su.CATEGORIAid = ca.id
            where su.disponibilidad = 1 and ca.id = '''+str(categoria)+'''
            order by su.subcategoria;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias


def obtenerSubcategoriasXMarca(marca):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT DISTINCT 
                s.id, 
                s.subcategoria , 
                m.marca 
            FROM SUBCATEGORIA s 
            INNER JOIN PRODUCTO p ON p.SUBCATEGORIAid = s.id 
            INNER JOIN MARCA m ON m.id = p.MARCAid 
            WHERE m.id = '''+str(marca)+''' AND s.disponibilidad = 1 AND m.disponibilidad = 1;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias



