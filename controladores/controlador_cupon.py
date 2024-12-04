from controladores.bd import obtener_conexion
import base64


def obtener_cupones():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                    SELECT 
                        cup.id,
                        cup.codigo,
                        cup.fecha_registro,
                        cup.fecha_inicio,
                        cup.fecha_vencimiento,
                        cup.cant_descuento,
                        cup.disponibilidad
                    FROM cupon cup
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos

def obtener_cupon_por_id(id):
    conexion = obtener_conexion()
    tipo = None
    with conexion.cursor() as cursor:
        cursor.execute('''
                    SELECT 
                        cup.id,
                        cup.codigo,
                        cup.fecha_registro,
                        cup.fecha_inicio,
                        cup.fecha_vencimiento,
                        cup.cant_descuento,
                        cup.disponibilidad
                    FROM cupon cup
                    WHERE id = '''+str(id)+'''
                       ''' )
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def eliminar_cupon(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM cupon WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def insertar_cupon(codigo,fecha_ini,fecha_ven,cant_dcto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO cupon (codigo,fecha_inicio,fecha_vencimiento,cant_descuento,disponibilidad) VALUES (%s,%s,%s,%s,1)", (codigo,fecha_ini,fecha_ven,cant_dcto))
    conexion.commit()
    conexion.close()


def actualizar_cupon_por_id(codigo,fecha_ini,fecha_ven,cant_dcto,disponibilidad,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE cupon SET codigo = %s , fecha_inicio = %s , fecha_vencimiento = %s , cant_descuento = %s , disponibilidad = %s WHERE id = %s",(codigo,fecha_ini,fecha_ven,cant_dcto,disponibilidad,id))
    conexion.commit()
    conexion.close()

