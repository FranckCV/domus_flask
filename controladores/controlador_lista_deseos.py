from bd import obtener_conexion

def obtenerListaDeseos(usuario_id):
    conexion = obtener_conexion()
    lista_deseos = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT p.id, p.nombre 
                FROM lista_deseos ls 
                INNER JOIN producto p ON p.id = ls.productoid
                WHERE ls.usuarioid = %s
            ''', (usuario_id,))
            
            lista_deseos = cursor.fetchall()
    except Exception as e:
        print("Error al obtener la lista de deseos:", e)
    finally:
        conexion.close()
    
    return lista_deseos


import base64

def obtenerListaDeseosConImagen(usuario_id):
    conexion = obtener_conexion()
    lista_deseos = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT img.imagen, p.nombre 
                FROM lista_deseos ls 
                INNER JOIN producto p ON p.id = ls.productoid
                INNER JOIN img_producto img ON img.productoid = p.id
                WHERE ls.usuarioid = %s
            ''', (usuario_id,))
            
            # Procesar los resultados
            for row in cursor.fetchall():
                imagen_binaria = row[0]  # Esto debería ser el campo de imagen binaria
                nombre_producto = row[1]

                # Convertir la imagen binaria a Base64
                if imagen_binaria:
                    imagen_base64 = base64.b64encode(imagen_binaria).decode('utf-8')
                else:
                    imagen_base64 = None

                lista_deseos.append({'imagen': imagen_base64, 'nombre': nombre_producto})
    
    except Exception as e:
        print("Error al obtener la lista de deseos:", e)
    
    return lista_deseos




def agregar_a_lista_deseos(usuario_id,producto_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT 1 FROM lista_deseos
                WHERE usuarioid = %s AND productoid = %s
            ''', (usuario_id, producto_id))
            existe = cursor.fetchone()
            
            if existe:
                cursor.execute('''
                    DELETE FROM lista_deseos
                    WHERE usuarioid = %s AND productoid = %s
                ''', (usuario_id, producto_id))
            else:
                cursor.execute('''
                    INSERT INTO lista_deseos (usuarioid, productoid)
                    VALUES (%s, %s)
                ''', (usuario_id, producto_id))
            conexion.commit()
    except Exception as e:
        print(f"Error al agregar o quitar producto: {e}")
    finally:
        conexion.close()


