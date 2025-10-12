from bd import obtener_conexion

def obtener_informacion_domus():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    `id`, 
                    `correo`, 
                    `numero`, 
                    `imgLogo`, 
                    `imgIcon`, 
                    `descripcion`, 
                    `historia`,
                    `vision`, 
                    `valores`,
                    `mision`
                FROM `informacion_domus` 
                order by id desc 
                limit 1
                       ''')
        datos = cursor.fetchone()

    conexion.close()
    return datos


def obtener_informacion_domus_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    `id`, 
                    `correo`, 
                    `numero`, 
                    `imgLogo`, 
                    `imgIcon`, 
                    `descripcion`, 
                    `historia`,
                    `vision`, 
                    `valores`,
                    `mision`
                FROM `informacion_domus`
                where id = '''+str(id)+'''
                order by id desc 
                limit 1;
                       ''')
        datos = cursor.fetchone()

    conexion.close()
    return datos


def obtener_imgs_informacion_domus_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                SELECT 
                    `id`,
                    `imgLogo`, 
                    `imgIcon`
                FROM `informacion_domus`
                where id = '''+str(id)+'''
                order by id desc 
                limit 1;
                       ''')
        datos = cursor.fetchone()
    
    conexion.close()
    return datos


def actualizar_informacion_domus_por_id(correo,numero,imgLogo,imgIcon,descripcion,historia,vision,valores,mision,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('''
                    UPDATE informacion_domus SET 
                        correo = %s , 
                        numero = %s , 
                        imgLogo = %s , 
                        imgIcon = %s , 
                        descripcion = %s , 
                        historia = %s , 
                        vision = %s , 
                        valores = %s , 
                        mision = %s 
                    WHERE id = %s
                    ''',
                       (correo,numero,imgLogo,imgIcon,descripcion,historia,vision,valores,mision,id))
    conexion.commit()
    conexion.close()



