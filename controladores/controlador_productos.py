from bd import obtener_conexion
import bd
from settings import img_route
ruta = img_route % 'img_producto'


def get_producto(u_id,p_id):
    sql = '''
        SELECT
            pr.id,
            pr.nombre,
            pr.precio_online as precio,
            pr.precio_oferta as oferta,
            pr.info_adicional,
            pr.stock,
            pr.fecha_registro,
            pr.disponibilidad,
            sc.nombre as subcategoria ,
            ca.nombre as categoria ,
            ma.nombre as marca,
            CASE
                WHEN ls.usuarioid IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS favorito
        FROM producto pr
        INNER JOIN subcategoria sc on sc.id = pr.subcategoriaid
        INNER JOIN categoria ca on ca.id = sc.categoriaid
        INNER JOIN marca ma on ma.id = pr.marcaid
        LEFT JOIN lista_deseos ls
            ON pr.id = ls.productoid
            AND ls.usuarioid = %s
        WHERE pr.id = %s
    '''
    return bd.sql_select_fetchone(sql,(u_id,p_id))


def get_productos_pedido(pedido_id):
    sql = '''
        SELECT
            pr.id,
            pr.nombre,
            ipr.imagen,
            det.cantidad,
            pr.stock,
            pr.precio_online as precio,
            pr.precio_oferta as oferta,
            CASE
                WHEN ls.usuarioid IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS favorito
        FROM producto pr
        INNER JOIN img_producto ipr ON pr.id = ipr.productoid
        INNER JOIN subcategoria sub ON sub.id = pr.subcategoriaid
        INNER JOIN categoria cat ON cat.id = sub.categoriaid
        INNER JOIN marca mar ON mar.id = pr.marcaid
        INNER JOIN detalles_pedido det
            ON pr.id = det.productoid
            AND det.pedidoid = %s
        INNER JOIN pedido p on p.id = det.pedidoid
        LEFT JOIN lista_deseos ls
            ON pr.id = ls.productoid
            AND ls.usuarioid = p.usuarioid
        WHERE
            cat.disponibilidad = 1
            AND sub.disponibilidad = 1
            AND mar.disponibilidad = 1
            AND ipr.imgPrincipal = 1
            AND pr.disponibilidad = 1
    '''

    return bd.sql_select_fetchall(sql, (pedido_id))


def get_productos_lista_deseos(usuario_id):
    sql = '''
        SELECT
            pr.id,
            pr.nombre,
            ipr.imagen,
            pr.precio_online as precio,
            pr.precio_oferta as oferta,
            CASE
                WHEN ls.usuarioid IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS favorito
        FROM producto pr
        INNER JOIN img_producto ipr ON pr.id = ipr.productoid
        INNER JOIN subcategoria sub ON sub.id = pr.subcategoriaid
        INNER JOIN categoria cat ON cat.id = sub.categoriaid
        INNER JOIN marca mar ON mar.id = pr.marcaid
        INNER JOIN lista_deseos ls
            ON pr.id = ls.productoid
            AND ls.usuarioid = %s
        WHERE
            cat.disponibilidad = 1
            AND sub.disponibilidad = 1
            AND mar.disponibilidad = 1
            AND ipr.imgPrincipal = 1
            AND pr.disponibilidad = 1
    '''

    return bd.sql_select_fetchall(sql, (usuario_id))


def get_productos_recientes(usuarioid,limit=10):
    sql = '''
        SELECT
            pr.id,
            pr.nombre,
            ipr.imagen,
            pr.stock,
            pr.precio_online as precio,
            pr.precio_oferta as oferta,
            CASE
                WHEN ls.usuarioid IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS favorito
        FROM producto pr
        INNER JOIN img_producto ipr ON pr.id = ipr.productoid
        INNER JOIN subcategoria sub ON sub.id = pr.subcategoriaid
        INNER JOIN categoria cat ON cat.id = sub.categoriaid
        INNER JOIN marca mar ON mar.id = pr.marcaid
        LEFT JOIN lista_deseos ls
            ON pr.id = ls.productoid
            AND ls.usuarioid = %s
        WHERE
            cat.disponibilidad = 1
            AND sub.disponibilidad = 1
            AND mar.disponibilidad = 1
            AND ipr.imgPrincipal = 1
            AND pr.disponibilidad = 1
            and pr.stock > 0
        ORDER BY pr.fecha_registro DESC , pr.id desc
        LIMIT %s
    '''
    return bd.sql_select_fetchall(sql,(usuarioid,limit))


def get_productos_populares(usuarioid,limit=10):
    sql = '''
        SELECT
            pr.id,
            pr.nombre,
            pr.stock,
            pr.precio_online as precio,
            pr.precio_oferta as oferta,
            ipr.imagen,
            SUM(dp.cantidad) AS total_compras,
            CASE
                WHEN ls.usuarioid IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS favorito
        FROM
            producto pr
        inner join img_producto ipr on pr.id = ipr.PRODUCTOid
        INNER JOIN detalles_pedido dp ON pr.id = dp.PRODUCTOid
        INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
        INNER JOIN categoria cat on cat.id = sub.categoriaid
        INNER JOIN marca mar on mar.id = pr.marcaid
        LEFT JOIN lista_deseos ls
            ON pr.id = ls.productoid
            AND ls.usuarioid = %s
        WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
        and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 and pr.stock > 0
        GROUP BY
            pr.id
        ORDER BY
            total_compras DESC , pr.fecha_registro DESC , pr.id desc
        LIMIT %s
    '''
    return bd.sql_select_fetchall(sql,(usuarioid,limit))


def get_productos_catalogo(
    usuarioid,
    busqueda=None,
    orden=None,
    categoria=None,
    subcategoria=None,
    precio_max=None,
    precio_min=None,
    limit=20
):
    """Obtiene productos del catálogo con filtros"""

    try:
        limit = int(limit) if limit else 20
        limit = min(limit, 100)
    except:
        limit = 20

    # Query base cambia según si necesitamos popularidad o no
    if str(orden) == "2":
        # Con subquery para obtener total de ventas
        sql = '''
            SELECT
                pr.id,
                pr.nombre,
                ipr.imagen,
                pr.stock,
                pr.precio_online AS precio,
                pr.precio_oferta AS oferta,
                CASE
                    WHEN ls.usuarioid IS NOT NULL THEN 1
                    ELSE 0
                END AS favorito,
                pr.fecha_registro,
                COALESCE(ventas.total_compras, 0) AS total_compras
            FROM producto pr
            INNER JOIN img_producto ipr ON pr.id = ipr.productoid
            INNER JOIN subcategoria sub ON sub.id = pr.subcategoriaid
            INNER JOIN categoria cat ON cat.id = sub.categoriaid
            INNER JOIN marca mar ON mar.id = pr.marcaid
            LEFT JOIN lista_deseos ls
                ON pr.id = ls.productoid
                AND ls.usuarioid = %s
            LEFT JOIN (
                SELECT productoid, SUM(cantidad) AS total_compras
                FROM detalles_pedido
                GROUP BY productoid
            ) ventas ON pr.id = ventas.productoid
            WHERE
                cat.disponibilidad = 1
                AND sub.disponibilidad = 1
                AND mar.disponibilidad = 1
                AND ipr.imgPrincipal = 1
                AND pr.disponibilidad = 1
        '''
    else:
        sql = '''
            SELECT
                pr.id,
                pr.nombre,
                ipr.imagen,
                pr.stock,
                pr.precio_online AS precio,
                pr.precio_oferta AS oferta,
                CASE
                    WHEN ls.usuarioid IS NOT NULL THEN 1
                    ELSE 0
                END AS favorito,
                pr.fecha_registro
            FROM producto pr
            INNER JOIN img_producto ipr ON pr.id = ipr.productoid
            INNER JOIN subcategoria sub ON sub.id = pr.subcategoriaid
            INNER JOIN categoria cat ON cat.id = sub.categoriaid
            INNER JOIN marca mar ON mar.id = pr.marcaid
            LEFT JOIN lista_deseos ls
                ON pr.id = ls.productoid
                AND ls.usuarioid = %s
            WHERE
                cat.disponibilidad = 1
                AND sub.disponibilidad = 1
                AND mar.disponibilidad = 1
                AND ipr.imgPrincipal = 1
                AND pr.disponibilidad = 1
        '''

    params = [usuarioid]

    if busqueda:
        sql += " AND pr.nombre LIKE %s "
        params.append(f"%{busqueda}%")

    if categoria:
        sql += " AND cat.id = %s "
        params.append(int(categoria))

    if subcategoria:
        sql += " AND sub.id = %s "
        params.append(int(subcategoria))

    if precio_min:
        try:
            sql += " AND pr.precio_online >= %s "
            params.append(float(precio_min))
        except:
            pass

    if precio_max:
        try:
            sql += " AND pr.precio_online <= %s "
            params.append(float(precio_max))
        except:
            pass

    # Ordenamiento
    orden_map = {
        "1": "ORDER BY pr.fecha_registro DESC, pr.id DESC",
        "2": "ORDER BY total_compras DESC, pr.fecha_registro DESC , pr.id desc",
        "3": "ORDER BY precio ASC",
        "4": "ORDER BY precio DESC",
    }

    sql += f" {orden_map.get(str(orden), 'ORDER BY pr.fecha_registro DESC , pr.id desc')}"
    # sql += " LIMIT %s"
    # params.append(limit)

    try:
        return bd.sql_select_fetchall(sql, tuple(params))
    except Exception as e:
        print(f"Error en get_productos_catalogo: {e}")
        return []











def obtener_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                pr.id,
                pr.nombre,
                pr.price_regular,
                pr.precio_online,
                pr.precio_oferta,
                pr.id,
                pr.info_adicional,
                pr.stock,
                date(pr.fecha_registro),
                pr.MARCAid,
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr
            WHERE pr.id = %s
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_info_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = f'''
            SELECT
                pr.id,
                pr.nombre,
                pr.price_regular,
                pr.precio_online,
                pr.precio_oferta,
                pr.id,
                pr.info_adicional,
                pr.stock,
                date(pr.fecha_registro),
                pr.MARCAid,
                pr.SUBCATEGORIAid,
                pr.disponibilidad,
                CONCAT({ruta},img.imagen) as imagen,
                sub.categoriaid
            FROM producto pr
            LEFT JOIN img_producto img on img.PRODUCTOid = pr.id
            LEFT JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
            WHERE pr.id = %s AND img.imgPrincipal = 1
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()

    conexion.close()
    return producto


def ver_info_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                pr.id,
                pr.nombre,
                pr.price_regular,
                pr.precio_online,
                pr.precio_oferta,
                pr.id,
                pr.info_adicional,
                pr.stock,
                date(pr.fecha_registro),
                pr.MARCAid,
                pr.SUBCATEGORIAid,
                pr.disponibilidad,
                pr.id,
                sub.categoriaid
            FROM producto pr
            LEFT JOIN img_producto img on img.PRODUCTOid = pr.id
            LEFT JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
            WHERE pr.id = %s AND img.imgPrincipal = 1
        '''
        cursor.execute(sql, (id))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_informacion_producto(id):
    return obtener_por_id(id)


def obtenerEnTarjetasTodos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen
                FROM `producto` pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                order by pr.fecha_registro desc;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtenerEnTarjetasMasRecientes():
    sql = '''
        SELECT
            pr.id,

            ipr.imagen, 
            pr.nombre,
            pr.disponibilidad,

            pr.price_regular,
            pr.precio_online,
            pr.precio_oferta,

            pr.MARCAid,
            pr.SUBCATEGORIAid,
            sub.CATEGORIAid,

            sub.nombre as subcategoria ,
            cat.nombre as categoria ,
            mar.nombre as marca ,

            pr.fecha_registro,
            pr.stock

        FROM `producto` pr
        inner join img_producto ipr on pr.id = ipr.PRODUCTOid
        LEFT JOIN subcategoria sub on sub.id = pr.subcategoriaid
        LEFT JOIN categoria cat on cat.id = sub.categoriaid
        LEFT JOIN marca mar on mar.id = pr.marcaid
        WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
        and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
        order by pr.fecha_registro desc , pr.id desc
    '''
    return bd.sql_select_fetchall(sql)


def obtenerEnTarjetasAlfabetico(orden):
    conexion = obtener_conexion()
    productos = []

    if orden == 0 :
        ordenar = 'asc'
    elif orden == 1:
        ordenar = 'desc'

    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM `producto` pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                order by pr.nombre '''+ordenar+'''
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtenerEnTarjetasxPrecio(orden):
    conexion = obtener_conexion()
    productos = []

    if orden == 0 :
        ordenar = 'asc'
    elif orden == 1:
        ordenar = 'desc'

    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM `producto` pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                order by pr.precio_oferta '''+ordenar+''' ,  pr.precio_online '''+ordenar+'''
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos




def buscarEnTarjetasMasRecientes(nombre):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM producto pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                and ( UPPER(pr.nombre) LIKE UPPER('%'''+str(nombre)+'''%') or UPPER(mar.marca) LIKE UPPER('%'''+str(nombre)+'''%'))
                order by pr.fecha_registro desc
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtenerEnTarjetasMasPopulares_catalogo():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    SUM(dp.cantidad) AS total_compras
                FROM
                    producto pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                left JOIN detalles_pedido dp ON pr.id = dp.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                GROUP BY
                    pr.id
                ORDER BY total_compras DESC , pr.fecha_registro desc
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtenerEnTarjetasMasPopulares():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    SUM(dp.cantidad) AS total_compras
                FROM
                    producto pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN detalles_pedido dp ON pr.id = dp.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                GROUP BY
                    pr.id
                ORDER BY
                    total_compras DESC
                LIMIT 15;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtenerEnTarjetasOfertas():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen
                FROM `producto` pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and ipr.imgPrincipal = 1 and pr.disponibilidad = 1
                and mar.disponibilidad = 1 and pr.precio_oferta > 0
                order by pr.fecha_registro desc
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtener_en_tarjetas_marca(id,marca, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen ,
                    sub.categoriaid
                FROM producto pr
                INNER JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' AND pr.MARCAid = '''+str(marca)+'''
                ORDER BY pr.fecha_registro desc
            '''

        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtener_en_tarjetas_subcategoria(id,subcategoria, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen
                FROM producto pr
                INNER JOIN img_producto ipr
                ON pr.id = ipr.PRODUCTOid
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' AND pr.SUBCATEGORIAid = '''+str(subcategoria)+'''
                ORDER BY pr.fecha_registro desc
            '''

        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def obtener_en_tarjetas_categoria(id,categoria, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.categoriaid
                FROM producto pr
                INNER JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+'''
                AND sub.CATEGORIAid = '''+str(categoria)+'''
                ORDER BY pr.fecha_registro desc
            '''

        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


# CRUD

def insertar_producto(nombre, price_regular, price_online, precio_oferta, info_adicional, stock, marca_id, subcategoria_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO producto(nombre, price_regular, precio_online, precio_oferta, info_adicional, stock, disponibilidad, MARCAid, SUBCATEGORIAid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, info_adicional, stock, 1, marca_id, subcategoria_id))

        cursor.execute('SELECT LAST_INSERT_ID();')
        id_producto = cursor.fetchone()[0]

    conexion.commit()
    conexion.close()

    return id_producto


def obtener_productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                id,
                nombre,
                price_regular,
                precio_online,
                precio_oferta,
                id,
                info_adicional,
                stock,
                date(fecha_registro),
                disponibilidad,
                MARCAid,
                SUBCATEGORIAid
            FROM producto
        '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_listado_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.id,
                    pr.info_adicional,
                    pr.stock,
                    date(pr.fecha_registro),
                    pr.disponibilidad,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.disponibilidad,
                    cat.disponibilidad,
                    mar.disponibilidad,
                    count(car.caracteristicaid),
                    COALESCE(img_count.total_imagenes, 0) AS total_imagenes
                FROM `producto` pr
                LEFT JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid AND ipr.imgPrincipal = 1
                LEFT JOIN subcategoria sub ON sub.id = pr.subcategoriaid
                LEFT JOIN categoria cat ON cat.id = sub.categoriaid
                LEFT JOIN marca mar ON mar.id = pr.marcaid
                left join caracteristica_producto car on car.productoid = pr.id
                LEFT JOIN (
                                SELECT
                                    PRODUCTOid,
                                    COUNT(*) AS total_imagenes
                                FROM img_producto
                                GROUP BY PRODUCTOid
                            ) AS img_count ON pr.id = img_count.PRODUCTOid
                GROUP BY pr.id;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def buscar_listado_productos_nombre(nombre):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT
                    pr.id,
                    pr.nombre,
                    pr.price_regular,
                    pr.precio_online,
                    pr.precio_oferta,
                    pr.id,
                    pr.info_adicional,
                    pr.stock,
                    date(pr.fecha_registro),
                    pr.disponibilidad,
                    pr.MARCAid,
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.disponibilidad,
                    cat.disponibilidad,
                    mar.disponibilidad,
                    count(car.caracteristicaid),
                    COALESCE(img_count.total_imagenes, 0) AS total_imagenes
                FROM `producto` pr
                LEFT JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid AND ipr.imgPrincipal = 1
                LEFT JOIN subcategoria sub ON sub.id = pr.subcategoriaid
                LEFT JOIN categoria cat ON cat.id = sub.categoriaid
                LEFT JOIN marca mar ON mar.id = pr.marcaid
                left join caracteristica_producto car on car.productoid = pr.id
                LEFT JOIN (
                                SELECT
                                    PRODUCTOid,
                                    COUNT(*) AS total_imagenes
                                FROM img_producto
                                GROUP BY PRODUCTOid
                            ) AS img_count ON pr.id = img_count.PRODUCTOid
                where ipr.imgPrincipal = 1 and UPPER(pr.nombre) LIKE UPPER ('%'''+str(nombre)+'''%')
                GROUP BY pr.id
                order by pr.nombre
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    conexion.close()
    return productos


def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM producto WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()


def actualizar_producto(nombre, price_regular, price_online, precio_oferta, info_adicional, stock, disponibilidad, marca_id, subcategoria_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE producto
            SET nombre = %s, price_regular = %s, precio_online = %s, precio_oferta = %s, info_adicional = %s, stock = %s, disponibilidad = %s, MARCAid = %s, SUBCATEGORIAid = %s
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, info_adicional, stock, disponibilidad, marca_id, subcategoria_id, id))
    conexion.commit()
    conexion.close()


def obtener_por_nombre(nombre):
    conexion = obtener_conexion()
    producto = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                pr.id,
                pr.nombre,
                pr.price_regular,
                pr.precio_online,
                pr.precio_oferta,
                pr.id,
                pr.info_adicional,
                pr.stock,
                date(pr.fecha_registro),
                pr.MARCAid,
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr
            WHERE pr.nombre LIKE '%'''+str(nombre)+'''%' and pr.disponibilidad = 1
        '''
        cursor.execute(sql)
        producto = cursor.fetchall()
    conexion.close()
    return producto




##validar las eliminaciones físicas

def buscar_en_caracteristica_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM caracteristica_producto WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_img_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM img_producto WHERE PRODUCTOid = %s and imgPrincipal = 0", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_lista_deseos(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM lista_deseos WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_detalles_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM detalles_pedido WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result



