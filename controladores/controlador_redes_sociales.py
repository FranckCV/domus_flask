from bd import obtener_conexion

def obtener_redes_sociales():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    red.id,
                    red.nomRed,
                    red.faicon_red,
                    red.enlace
                FROM redes_sociales red
                       ''')
        datos = cursor.fetchall()
    conexion.close()
    return datos


def insertar_redes_sociales(nomred,faicon_red,enlace):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO redes_sociales (nomred,faicon_red,enlace) VALUES (%s,%s,%s)", (nomred,faicon_red,enlace))
    conexion.commit()
    conexion.close()

def insertar_redes_sociales_api(nomred, faicon_red, enlace):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Ejecutar la inserción de la red social
        cursor.execute("INSERT INTO redes_sociales (nomred, faicon_red, enlace) VALUES (%s, %s, %s)", 
                       (nomred, faicon_red, enlace))
        
        # Obtener el último id insertado
        cursor.execute('SELECT LAST_INSERT_ID();')
        id_red_social = cursor.fetchone()[0]
    
    conexion.commit()
    conexion.close()
    
    return id_red_social



def eliminar_redes_sociales(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM redes_sociales WHERE id = %s", (id))
    conexion.commit()
    conexion.close()


def obtener_redes_sociales_por_id(id):
    conexion = obtener_conexion()
    tipo = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nomred , faicon_red , enlace FROM redes_sociales WHERE id = %s", (id))
        tipo = cursor.fetchone()
    conexion.close()
    return tipo


def actualizar_redes_sociales_por_id(nomred,faicon_red,enlace,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE redes_sociales SET nomred = %s , faicon_red = %s , enlace = %s WHERE id = %s",(nomred,faicon_red,enlace, id))
    conexion.commit()
    conexion.close()

