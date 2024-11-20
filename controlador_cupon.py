from bd import obtener_conexion
import base64


def obtener_cupones():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                   cup.*
                FROM cupon cup
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


# def insertar_cupon(nomred,faicon_red,enlace):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("INSERT INTO cupon (nomred,faicon_red,enlace) VALUES (%s,%s,%s)", (nomred,faicon_red,enlace))
#     conexion.commit()
#     conexion.close()


# def eliminar_cupon(id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("DELETE FROM cupon WHERE id = %s", (id))
#     conexion.commit()
#     conexion.close()


# def obtener_cupon_por_id(id):
#     conexion = obtener_conexion()
#     tipo = None
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT id, nomred , faicon_red , enlace FROM cupon WHERE id = %s", (id))
#         tipo = cursor.fetchone()
#     conexion.close()
#     return tipo


# def actualizar_cupon_por_id(nomred,faicon_red,enlace,id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("UPDATE cupon SET nomred = %s , faicon_red = %s , enlace = %s WHERE id = %s",(nomred,faicon_red,enlace, id))
#     conexion.commit()
#     conexion.close()

