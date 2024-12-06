from controladores.bd import obtener_conexion
tabla = 'categoria'
import controladores.controlador_subcategorias as controlador_subcategorias


def obtener_categorias_disponibles():
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = 'SELECT id, categoria, faicon_cat, disponibilidad FROM '+tabla + ' where disponibilidad = 1'
        cursor.execute(sql)
        categorias = cursor.fetchall()    
    return categorias


# def obtener_categoria_por_id(id):
#     conexion = obtener_conexion()
#     categoria = None
#     with conexion.cursor() as cursor:
#         sql = 'SELECT id, categoria, faicon_cat, disponibilidad FROM '+tabla + ' where id = '+str(id)
#         cursor.execute(sql)
#         categoria = cursor.fetchone()    
#     return categoria


def obtener_categorias_subcategorias():
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = '''
        SELECT 
            id, 
            categoria, 
            faicon_cat, 
            disponibilidad
        FROM categoria 
        where disponibilidad = 1
        '''
        cursor.execute(sql)
        categorias = cursor.fetchall()
        
    categorias_lista = []

    for categoria in categorias:

        cat_id, cat_nom, cat_icon , cat_dis = categoria

        subCategorias = controlador_subcategorias.obtenerSubcategoriasXCategoria(cat_id)

        categorias_lista.append((cat_id, cat_nom, cat_icon , cat_dis, subCategorias))

    conexion.close()
    return categorias_lista


def obtener_categoriasXnombre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id ,categoria,faicon_cat,disponibilidad FROM categoria order by categoria")
        categorias = cursor.fetchall()
    conexion.close()
    return categorias


def insertar_categoria(categoria,faicon_cat,disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categoria(categoria,faicon_cat,disponibilidad) VALUES (%s, %s,%s)",(categoria,faicon_cat,disponibilidad))
    conexion.commit()
    conexion.close()

def insertar_categoria_api(categoria, faicon_cat, disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categoria(categoria, faicon_cat, disponibilidad) VALUES (%s, %s, %s)", 
                       (categoria, faicon_cat, disponibilidad))

        cursor.execute("SELECT LAST_INSERT_ID();")
        id_categoria = cursor.fetchone()[0]

    conexion.commit()
    conexion.close()

    return id_categoria



def obtener_categorias():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id ,categoria,faicon_cat,disponibilidad FROM categoria")
        categorias = cursor.fetchall()
    conexion.close()
    return categorias


def obtener_listado_categorias():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            cat.id ,
                            cat.categoria ,
                            cat.faicon_cat ,
                            cat.disponibilidad,
                            count(sub.id)
                        FROM categoria cat
                        LEFT JOIN subcategoria sub on sub.categoriaid = cat.id
                        Group by cat.id
                        ''')
        categorias = cursor.fetchall()
    conexion.close()
    return categorias


def eliminar_categoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM categoria WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_categoria_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, categoria,faicon_cat,disponibilidad FROM categoria WHERE id = %s", (id,))
        categoria = cursor.fetchone()
    conexion.close()
    return categoria


def actualizar_categoria(categoria,faicon_cat,disponibilidad, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE categoria SET categoria = %s ,faicon_cat = %s,disponibilidad=%s WHERE id =%s",
                       (categoria,faicon_cat,disponibilidad, id))
    conexion.commit()
    conexion.close()


def obtener_categoria_id_relacion(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            cat.id ,
                            cat.categoria ,
                            cat.faicon_cat ,
                            cat.disponibilidad,
                            count(sub.id)
                        FROM categoria cat
                        LEFT JOIN subcategoria sub on sub.categoriaid = cat.id
                        where cat.id = '''+str(id)+'''
                        group by cat.id
                        ''')
        categorias = cursor.fetchone()
    conexion.close()
    return categorias


