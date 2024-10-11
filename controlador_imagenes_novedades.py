from bd import obtener_conexion
import base64
tabla = 'producto'


def obtener_imagenes_novedades_por_marca(marca):
    conexion = obtener_conexion()
    imagenes = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                ino.id ,
                ino.imagen
            FROM img_novedad ino
            inner join novedad nov on nov.id = ino.novedadid
            where nov.marcaid = '''+str(marca)+'''
            limit 1
            '''
        cursor.execute(sql)
        imagenes = cursor.fetchall()

    imagenes_lista = []
    for imagen in imagenes:
        id, img , prin= imagen
        if imagen:
            img_base64 = base64.b64encode(img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo
        imagenes_lista.append((id, img_url , prin))

    conexion.close()
    return imagenes_lista





