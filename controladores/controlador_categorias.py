from bd import obtener_conexion
tabla = 'categoria'
import controladores.controlador_subcategorias as controlador_subcategorias
import bd

def obtener_categorias_disponibles():
    sql = '''
        SELECT 
            id, nombre, faicon_cat, disponibilidad 
        FROM categoria 
        where disponibilidad = 1
    '''   
    return bd.sql_select_fetchall(sql)


def obtener_categoria_disponible_id(id):
    sql = '''
        SELECT 
            id, nombre, faicon_cat, disponibilidad 
        FROM categoria 
        where disponibilidad = 1 and id = %s
    '''   
    return bd.sql_select_fetchall(sql,(id))


def obtener_categorias_subcategorias():
    categorias = obtener_categorias_disponibles()

    for categoria in categorias:
        subCategorias = controlador_subcategorias.obtenerSubcategoriasXCategoria(categoria['id'])
        categoria['subcategorias'] = subCategorias

    return categorias


def obtener_categoriasXnombre():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id ,nombre,faicon_cat,disponibilidad FROM categoria order by categoria")
        categorias = cursor.fetchall()
    conexion.close()
    return categorias


def insertar_categoria(categoria,faicon_cat,disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categoria(nombre,faicon_cat,disponibilidad) VALUES (%s, %s,%s)",(categoria,faicon_cat,disponibilidad))
    conexion.commit()
    conexion.close()

def insertar_categoria_api(categoria, faicon_cat, disponibilidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categoria(nombre, faicon_cat, disponibilidad) VALUES (%s, %s, %s)", 
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
                            cat.nombre ,
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
                            cat.nombre ,
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


