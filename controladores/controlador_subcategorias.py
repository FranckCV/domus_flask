from bd import obtener_conexion
from pymysql.cursors import DictCursor
tabla = 'categoria'


def obtenerSubcategoriasXCategoria(categoria):
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                su.id , 
                su.nombre , 
                su.faicon_subcat,
                su.CATEGORIAid
            FROM categoria ca
            inner join subcategoria su on su.CATEGORIAid = ca.id
            where su.disponibilidad = 1 and ca.id = '''+str(categoria)+'''
            order by su.nombre;
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
                ca.nombre,
                ca.faicon_cat,
                su.id, 
                su.nombre , 
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
            FROM subcategoria s 
            INNER JOIN producto p ON p.SUBCATEGORIAid = s.id 
            INNER JOIN marca m ON m.id = p.MARCAid 
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
                        sub.nombre ,
                        sub.faicon_subcat,
                        sub.disponibilidad,
                        sub.categoriaid , 
                        cat.nombre ,
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
        cursor.execute("INSERT INTO subcategoria(nombre,faicon_subcat,disponibilidad,categoriaid) VALUES (%s, %s,%s,%s)",(nombre,faicon_subcat,disponibilidad,categoriaid))
    conexion.commit()
    conexion.close()

def insertar_subcategoria_api(nombre, faicon_subcat, disponibilidad, categoriaid):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO subcategoria(nombre, faicon_subcat, disponibilidad, categoriaid) VALUES (%s, %s, %s, %s)", 
                           (nombre, faicon_subcat, disponibilidad, categoriaid))
            
            cursor.execute('SELECT LAST_INSERT_ID();')
            id_subcategoria = cursor.fetchone()[0]
        
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()
    return id_subcategoria


def obtener_subcategorias():
    conexion = obtener_conexion()
    with conexion.cursor(DictCursor) as cursor:
        cursor.execute('''
                        SELECT 
                            sub.id , 
                            sub.nombre , 
                            sub.faicon_subcat ,
                            sub.disponibilidad ,
                            sub.categoriaid , 
                            cat.nombre ,
                            cat.faicon_cat,
                            count(pr.id),
                            count(nov.id)
                        FROM subcategoria sub 
                        left JOIN categoria cat on cat.id = sub.categoriaid
                        left join producto pr on pr.SUBCATEGORIAid = sub.id
                        left join novedad nov on nov.SUBCATEGORIAid = sub.id
                        group by sub.id;
                       ''')
        subcategorias = cursor.fetchall()
    conexion.close()
    return subcategorias


def obtener_listado_subcategorias():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            sub.id , 
                            sub.nombre , 
                            sub.faicon_subcat ,
                            sub.disponibilidad ,
                            sub.categoriaid , 
                            cat.nombre ,
                            cat.faicon_cat,
                            count(pr.id),
                            count(nov.id),
                            cat.disponibilidad
                        FROM subcategoria sub 
                        left JOIN categoria cat on cat.id = sub.categoriaid
                        left join producto pr on pr.SUBCATEGORIAid = sub.id
                        left join novedad nov on nov.SUBCATEGORIAid = sub.id
                        group by sub.id;
                       ''')
        subcategorias = cursor.fetchall()
    conexion.close()
    return subcategorias


def buscar_listado_subcategorias_nombre(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            sub.id , 
                            sub.nombre , 
                            sub.faicon_subcat ,
                            sub.disponibilidad ,
                            sub.categoriaid , 
                            cat.nombre ,
                            cat.faicon_cat,
                            count(pr.id),
                            count(nov.id),
                            cat.disponibilidad
                        FROM subcategoria sub 
                        left JOIN categoria cat on cat.id = sub.categoriaid
                        left join producto pr on pr.SUBCATEGORIAid = sub.id
                        left join novedad nov on nov.SUBCATEGORIAid = sub.id
                        WHERE UPPER(sub.subcategoria) LIKE UPPER ('%'''+str(nombre)+'''%')
                        group by sub.id;
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




