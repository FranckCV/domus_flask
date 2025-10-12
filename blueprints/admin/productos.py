from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from controladores import (
    controlador_productos,
    controlador_marcas,
    controlador_categorias,
    controlador_subcategorias,
    controlador_imagenes_productos,
    controlador_usuario_admin,
)
from clases.clsProducto import Producto as clsProducto
from clases.clsImgProducto import ImgProducto as clsImgProducto

# Crear blueprint
admin_productos_bp = Blueprint(
    'admin_productos',
    __name__,
    template_folder='../../templates',
    static_folder='../../static'
)

def login_requerido(func):
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('admin_dashboard.login_admin'))
        return func(*args, **kwargs)
    return envoltura

def verificar_permisos_admin(func):
    """Verifica si el usuario es admin (tipo 1)"""
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('admin_dashboard.login_admin'))
        
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)
        
        # Si es empleado regular (tipo 2), redirigir al dashboard
        if tipo_id == 2:
            return redirect(url_for('admin_dashboard.dashboard'))
        
        return func(*args, **kwargs)
    return envoltura

# Rutas
@admin_productos_bp.route("/agregar_producto")
@login_requerido
@verificar_permisos_admin
def formulario_agregar_producto():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("agregar_producto.html", 
                         marcas=marcas, 
                         subcategorias=subcategorias, 
                         categorias=categorias)



@admin_productos_bp.route("/eliminar_img_producto", methods=["POST"])
@login_requerido
def eliminar_img_producto():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["img_id"]
        imagen = controlador_imagenes_productos.obtener_imagen_por_id(id)
        idpro = imagen[2]
        controlador_imagenes_productos.eliminar_img_producto_x_id(id)
        return redirect("/formulario_editar_producto="+str(idpro))
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa




@admin_productos_bp.route("/guardar_producto", methods=["POST"])
@login_requerido
def guardar_producto():
    nombre = request.form["nombre"]
    price_regular= request.form["price_regular"]
    price_online= request.form["price_online"]
    precio_oferta= request.form["precio_oferta"]
    infoAdicional= request.form["infoAdicional"]
    stock= request.form["stock"]
    marca_id= request.form["marca_id"]
    subcategoria_id= request.form["subcategorySelect"]

    imagen = request.files["imagenProduct"]
    imagen_bin = imagen.read()

    objProducto = clsProducto(
        p_id=None,
        p_nombre=nombre,
        p_price_regular=price_regular,
        p_precio_online=price_online,
        p_precio_oferta=precio_oferta,
        p_info_adicional=infoAdicional,
        p_stock=stock,
        p_fecha_registro=None,
        p_disponibilidad=1,
        p_MARCAid=marca_id,
        p_SUBCATEGORIAid=subcategoria_id
    )

    id_pro = controlador_productos.insertar_producto(
        objProducto.nombre,
        objProducto.price_regular,
        objProducto.precio_online,
        objProducto.precio_oferta,
        objProducto.info_adicional,
        objProducto.stock,
        objProducto.MARCAid,
        objProducto.SUBCATEGORIAid
        )

    objImgProducto = clsImgProducto(
        p_id=None,
        p_img_nombre=nombre+"_"+imagen.filename,
        p_imagen=imagen,
        p_imgPrincipal=1,
        p_PRODUCTOid=id_pro
    )

    controlador_imagenes_productos.insertar_img_producto(objImgProducto.img_nombre,objImgProducto.imagen,objImgProducto.imgPrincipal,id_pro)

    files = request.files.getlist('imgsProd')
    for file in files:
        nom_file = nombre+'_'+file.filename
        data = file.read()
        controlador_imagenes_productos.insertar_img_producto(nom_file,data,0,id_pro)

    return redirect("/listado_productos")


@admin_productos_bp.route("/listado_productos")
@login_requerido
def productos():
    productos = controlador_productos.obtener_listado_productos()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias)


@admin_productos_bp.route("/listado_productos_buscar")
@login_requerido
def productos_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    productos = controlador_productos.buscar_listado_productos_nombre(nombreBusqueda)
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias , nombreBusqueda = nombreBusqueda)


@admin_productos_bp.route("/eliminar_producto", methods=["POST"])
@login_requerido
def eliminar_producto():
    id_producto = request.form["id"]

    # Verificamos si el producto está asociado a otras tablas
    tiene_caracteristicas = controlador_productos.buscar_en_caracteristica_producto(id_producto)
    tiene_img = controlador_productos.buscar_en_img_producto(id_producto)
    tiene_lista_deseo = controlador_productos.buscar_en_lista_deseos(id_producto)
    tiene_detalle = controlador_productos.buscar_en_detalles_pedido(id_producto)

    error_message = None

    if tiene_caracteristicas:
        error_message = "El producto tiene características asociadas y no se puede eliminar."
    elif tiene_img:
        error_message = "El producto tiene imágenes asociadas y no se puede eliminar."
    elif tiene_lista_deseo:
        error_message = "El producto está en listas de deseos de clientes y no se puede eliminar."
    elif tiene_detalle:
        error_message = "El producto está en detalles de pedidos y no se puede eliminar."

    if error_message:
        # Si el producto está asociado a alguna de las condiciones, mostramos el error
        return render_template("listado_productos.html", error=error_message + " Redirigiendo en 3 segundos...", show_modal=True)
    else:
        # Si no está asociado, procedemos a eliminar
        controlador_productos.eliminar_producto(id_producto)
        return redirect("/listado_productos")


@admin_productos_bp.route("/eliminar_producto2", methods=["POST"])
@login_requerido
def eliminar_producto2():
    id_producto = request.form["id"]

    # Verificamos si el producto está asociado a otras tablas
    tiene_caracteristicas = controlador_productos.buscar_en_caracteristica_producto(id_producto)
    tiene_img = controlador_productos.buscar_en_img_producto(id_producto)
    tiene_lista_deseo = controlador_productos.buscar_en_lista_deseos(id_producto)
    tiene_detalle = controlador_productos.buscar_en_detalles_pedido(id_producto)

    tiene_img_princ = controlador_imagenes_productos.validar_img_principal_por_producto(id_producto) != 1

    error_message = None

    if tiene_img :
        error_message = "El producto tiene imagenes secundarias asociadas y no se puede eliminar."
    elif tiene_caracteristicas:
        error_message = "El producto tiene características asociadas y no se puede eliminar."
    elif tiene_img_princ:
        error_message = "El producto tiene imágenes asociadas y no se puede eliminar."
    elif tiene_lista_deseo:
        error_message = "El producto está en listas de deseos de clientes y no se puede eliminar."
    elif tiene_detalle:
        error_message = "El producto está en detalles de pedidos y no se puede eliminar."

    if error_message:
        # Si el producto está asociado a alguna de las condiciones, mostramos el error
        return render_template("listado_productos.html", error=error_message + " Redirigiendo en 3 segundos...", show_modal=True)
    else:
        # Si no está asociado, procedemos a eliminar
        controlador_imagenes_productos.eliminar_img_producto(id_producto)
        controlador_productos.eliminar_producto(id_producto)
        return redirect("/listado_productos")


@admin_productos_bp.route("/ver_producto=<int:id>")
@login_requerido
def ver_producto(id):
    producto = controlador_productos.ver_info_por_id(id)
    imagenes = controlador_imagenes_productos.obtener_imagenes_por_producto(id)
    caracteristicasPrincipales = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,1)
    caracteristicasSecundarias = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,0)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("ver_producto.html", producto=producto,marcas=marcas, subcategorias=subcategorias,categorias = categorias , id = id , imagenes = imagenes , caracteristicasPrincipales = caracteristicasPrincipales , caracteristicasSecundarias = caracteristicasSecundarias)


@admin_productos_bp.route("/formulario_editar_producto=<int:id>")
@login_requerido
def editar_producto(id):
    imagenes = controlador_imagenes_productos.obtener_listado_imagenes_sec_por_producto(id)
    caracteristicasPrincipales = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,1)
    caracteristicasSecundarias = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,0)
    producto = controlador_productos.obtener_info_por_id(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("editar_producto.html", producto=producto,marcas=marcas, subcategorias=subcategorias,categorias = categorias , imagenes = imagenes , caracteristicasPrincipales = caracteristicasPrincipales , caracteristicasSecundarias = caracteristicasSecundarias)


@admin_productos_bp.route("/actualizar_producto", methods=["POST"])
@login_requerido
def actualizar_producto():
    id = request.form["id"]

    producto = controlador_imagenes_productos.obtener_img_principal_por_producto(id)

    nombre = request.form["nombre"]
    price_online= request.form["price_online"]
    price_regular= request.form["price_regular"]
    precio_oferta= request.form["precio_oferta"]
    infoAdicional= request.form["infoAdicional"]
    stock= request.form["stock"]
    disponibilidad= request.form["disponibilidad"]
    marca_id= request.form["marca_id"]
    subcategoria_id= request.form["subcategorySelect"]

    imagen = request.files["imagenProduct"]

    if imagen.filename == '':
        imagen_bin = producto[1]
    else:
        imagen_bin = imagen.read()

    objProducto = clsProducto(
        p_id=id,
        p_nombre=nombre,
        p_price_regular=price_regular,
        p_precio_online=price_online,
        p_precio_oferta=precio_oferta,
        p_info_adicional=infoAdicional,
        p_stock=stock,
        p_fecha_registro=None,
        p_disponibilidad=disponibilidad,
        p_MARCAid=marca_id,
        p_SUBCATEGORIAid=subcategoria_id
    )

    objImgProducto = clsImgProducto(
        p_id=None,
        p_img_nombre=None,
        p_imagen=imagen_bin,
        p_imgPrincipal=None,
        p_PRODUCTOid=id
    )


    controlador_productos.actualizar_producto(objProducto.nombre, objProducto.price_regular, objProducto.precio_online, objProducto.precio_oferta, objProducto.info_adicional, objProducto.stock, objProducto.disponibilidad, objProducto.MARCAid, objProducto.SUBCATEGORIAid, objProducto.id)
    controlador_imagenes_productos.actualizar_img_producto(objImgProducto.imagen,objImgProducto.PRODUCTOid)

    return redirect("/listado_productos")



