from bd import obtener_conexion
tabla = 'categoria'
import controlador_subcategorias

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


