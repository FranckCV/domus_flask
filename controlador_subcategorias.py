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
                su.faicon_subcat,
                su.CATEGORIAid
            FROM categoria ca
            inner join subcategoria su on su.CATEGORIAid = ca.id
            where su.disponibilidad = 1 and ca.id = '''+str(categoria)+'''
            order by su.subcategoria;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias


def obtenerCategoriasXSubcategoria(subcategoria):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                ca.id,
                ca.categoria,
                ca.faicon_cat,
                su.id, 
                su.subcategoria , 
                su.faicon_subcat
            FROM categoria ca
            inner join subcategoria su on su.CATEGORIAid = ca.id
            where su.disponibilidad = 1 and ca.disponibilidad = 1 and su.id = '''+str(subcategoria)+'''
            order by su.subcategoria;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchone()
    return categorias


def obtenerSubcategoriasXMarca(marca):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT DISTINCT 
                s.id, 
                s.subcategoria , 
                s.faicon_subcat , 
                m.marca
            FROM SUBCATEGORIA s 
            INNER JOIN PRODUCTO p ON p.SUBCATEGORIAid = s.id 
            INNER JOIN MARCA m ON m.id = p.MARCAid 
            WHERE m.id = '''+str(marca)+''' AND s.disponibilidad = 1 AND m.disponibilidad = 1;
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias


def obtener_subcategoriasXnombre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                       SELECT 
                        sub.id , 
                        sub.subcategoria ,
                        sub.faicon_subcat,
                        sub.disponibilidad,
                        sub.categoriaid , 
                        cat.categoria ,
                        cat.faicon_cat 
                       FROM subcategoria sub 
                       INNER JOIN categoria cat on cat.id = sub.categoriaid 
                       order by sub.subcategoria
                       ''')
        subcategorias = cursor.fetchall()
    conexion.close()
    return subcategorias


def insertar_subcategoria(nombre,faicon_subcat,disponibilidad,categoriaid):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO subcategoria(subcategoria,faicon_subcat,disponibilidad,categoriaid) VALUES (%s, %s,%s,%s)",(nombre,faicon_subcat,disponibilidad,categoriaid))
    conexion.commit()
    conexion.close()


def obtener_subcategorias():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            sub.id , 
                            sub.subcategoria , 
                            sub.faicon_subcat ,
                            sub.disponibilidad ,
                            sub.categoriaid , 
                            cat.categoria ,
                            cat.faicon_cat 
                        FROM subcategoria sub 
                        INNER JOIN categoria cat on cat.id = sub.categoriaid
                       ''')
        subcategorias = cursor.fetchall()
    conexion.close()
    return subcategorias


def eliminar_subcategoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM subcategoria WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_subcategoria_por_id(id):
    conexion = obtener_conexion()
    subcategoria = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, subcategoria,faicon_subcat,disponibilidad,categoriaid FROM subcategoria WHERE id = %s", (id,))
        subcategoria = cursor.fetchone()
    conexion.close()
    return subcategoria


def actualizar_subcategoria(nombre,faicon_subcat,disponibilidad,categoriaid, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE subcategoria SET subcategoria = %s ,faicon_subcat = %s,disponibilidad = %s,categoriaid = %s WHERE id =%s",
                       (nombre,faicon_subcat,disponibilidad,categoriaid, id))
    conexion.commit()
    conexion.close()


def obtener_id_subcategoria(subcategoria):
    conexion = obtener_conexion()
    subcategoria_id = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM subcategoria WHERE subcategoria = %s", (subcategoria,))
        resultado = cursor.fetchone()
        if resultado:
            subcategoria_id = resultado[0]
    conexion.close()
    return subcategoria_id




