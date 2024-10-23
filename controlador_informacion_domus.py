from bd import obtener_conexion
import base64


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
                limit 1;
                       ''')
        datos = cursor.fetchone()

    elementos = None

    if datos:
        id, correo, numero, imgLogo , imgIcon , descripcion , historia , vision , valores , mision = datos

        if imgLogo:
            logo_base64 = base64.b64encode(imgLogo).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = "" 

        if imgIcon:
            icon_base64 = base64.b64encode(imgIcon).decode('utf-8')
            icon_url = f"data:image/png;base64,{icon_base64}"
        else:
            icon_url = "" 

        elementos = (id, correo, numero, logo_url , icon_url , descripcion , historia , vision , valores , mision)

    conexion.close()
    return elementos


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

    elementos = None

    if datos:
        id, correo, numero, imgLogo , imgIcon , descripcion , historia , vision , valores , mision = datos

        if imgLogo:
            logo_base64 = base64.b64encode(imgLogo).decode('utf-8')
            logo_url = f"data:image/png;base64,{logo_base64}"
        else:
            logo_url = "" 

        if imgIcon:
            icon_base64 = base64.b64encode(imgIcon).decode('utf-8')
            icon_url = f"data:image/png;base64,{icon_base64}"
        else:
            icon_url = "" 

        elementos = (id, correo, numero, logo_url , icon_url , descripcion , historia , vision , valores , mision)

    conexion.close()
    return elementos


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



