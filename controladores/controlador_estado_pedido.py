from controladores.bd import obtener_conexion
import base64


def obtener_estados_pedido():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    est.id,
                    est.nomestado
                FROM estado_pedido est
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def obtener_listado_estados_pedido():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    est.id,
                    est.nomestado,
                    count(ped.id)
                FROM estado_pedido est
                left join pedido ped on ped.estado_pedidoid = est.id
                group by est.id
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def insertar_estado_pedido(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO estado_pedido (nomestado) VALUES (%s)", (nombre))
    conexion.commit()
    conexion.close()


def eliminar_estado_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM estado_pedido WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_estado_pedido_por_id(id):
    conexion = obtener_conexion()
    tipo = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nomestado FROM estado_pedido WHERE id = %s", (id))
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def actualizar_estado_pedido_por_id(nombre ,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE estado_pedido SET nomestado = %s WHERE id = %s",(nombre , id))
    conexion.commit()
    conexion.close()

