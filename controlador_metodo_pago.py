from bd import obtener_conexion
<<<<<<< HEAD
def obtener_Metodo_pago():
    conexion=obtener_conexion()
    metodo=[]
    with conexion.cursor() as cursor:
        sql="select id,metodo from metodo_pago"
        cursor.execute(sql)
        metodo=cursor.fetchall
    conexion.commit
    return metodo
=======
import base64


def obtener_metodo_pago():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    met.id,
                    met.metodo,
                    met.disponibilidad
                FROM metodo_pago met
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def insertar_metodo_pago(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO metodo_pago (metodo,disponibilidad) VALUES (%s,1)", (nombre))
    conexion.commit()
    conexion.close()


def eliminar_metodo_pago(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM metodo_pago WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_metodo_pago_por_id(id):
    conexion = obtener_conexion()
    tipo = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, metodo,disponibilidad FROM metodo_pago WHERE id = %s", (id))
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def actualizar_metodo_pago_por_id(nombre,disponibilidad,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE metodo_pago SET metodo = %s , disponibilidad = %s WHERE id = %s",(nombre ,disponibilidad, id))
    conexion.commit()
    conexion.close()

>>>>>>> 2fc6d23ce0dc7b276230c9909223336a1e6043ea
