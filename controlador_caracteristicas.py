from bd import obtener_conexion
import base64


def obtener_Caracteristicas():
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                car.id,
                car.campo,
                car.disponibilidad
            FROM caracteristica car
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas


def obtener_listado_Caracteristicas():
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                car.id,
                car.campo,
                car.disponibilidad,
                sub.id,
                sub.subcategoria,
                sub.faicon_subcat,
                sub.CATEGORIAid,
                cat.categoria,
                cat.faicon_cat,
                count(pr.id)
            FROM caracteristica car
            LEFT JOIN caracteristica_subcategoria csc on csc.CARACTERISTICAid = car.id
            LEFT JOIN subcategoria sub on sub.id = csc.SUBCATEGORIAid
            LEFT JOIN categoria cat on cat.id = sub.CATEGORIAid
            LEFT JOIN caracteristica_producto cpr on cpr.CARACTERISTICAid = car.id
            LEFT JOIN producto pr on pr.id = cpr.PRODUCTOid
            group by car.id
            order by car.id asc , sub.subcategoria;
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas


def buscar_listado_Caracteristicas_nombre(nombre):
    conexion = obtener_conexion()
    caracteristicas = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                car.id,
                car.campo,
                car.disponibilidad,
                sub.id,
                sub.subcategoria,
                sub.faicon_subcat,
                sub.CATEGORIAid,
                cat.categoria,
                cat.faicon_cat,
                count(pr.id)
            FROM caracteristica car
            LEFT JOIN caracteristica_subcategoria csc on csc.CARACTERISTICAid = car.id
            LEFT JOIN subcategoria sub on sub.id = csc.SUBCATEGORIAid
            LEFT JOIN categoria cat on cat.id = sub.CATEGORIAid
            LEFT JOIN caracteristica_producto cpr on cpr.CARACTERISTICAid = car.id
            LEFT JOIN producto pr on pr.id = cpr.PRODUCTOid
            WHERE UPPER(car.campo) LIKE UPPER ('%'''+str(nombre)+'''%')
            group by car.id
            order by car.id asc , sub.subcategoria;
            '''
        cursor.execute(sql)
        caracteristicas = cursor.fetchall()
    conexion.close()
    return caracteristicas
    

def insertar_caracteristica(campo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO caracteristica (campo, disponibilidad) VALUES (%s, 1)", (campo))
    conexion.commit()
    conexion.close()


def eliminar_caracteristica(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM caracteristica WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_caracteristica_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT car.id, car.campo, car.disponibilidad FROM caracteristica car WHERE id = %s", (id))
        marca = cursor.fetchone()
    conexion.close()
    return marca


def actualizar_caracteristica(campo, disp, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE caracteristica SET campo = %s , disponibilidad = %s WHERE id =%s",
                       (campo, disp, id))
    conexion.commit()
    conexion.close()

