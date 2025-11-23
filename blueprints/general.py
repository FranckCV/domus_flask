from flask import Blueprint, render_template, request, redirect
from controladores import (
    controlador_caracteristicas_productos,
    controlador_categorias,
    controlador_imagenes_novedades,
    controlador_imagenes_productos,
    controlador_marcas,
    controlador_productos,
    controlador_novedades ,
    controlador_contenido_info ,
    controlador_informacion_domus ,
    controlador_motivo_comentario,
    controlador_subcategorias,
    controlador_tipos_novedad
)

general_bp = Blueprint('general', __name__)


@general_bp.route("/")
def index():
    marcasBloque = controlador_marcas.obtener_marcas_index(10)
    productosRecientes = controlador_productos.obtenerEnTarjetasMasRecientes()
    productosPopulares = controlador_productos.obtenerEnTarjetasMasPopulares()
    novedadesBanner = controlador_novedades.obtenerBannersNovedadesRecientes()
    novedadesRecientes = controlador_novedades.obtenerNovedadesRecientes()
    # print(lista_deseos_ids)
    return render_template("index.html",
                           novedadesRecientes=novedadesRecientes,
                           marcasBloque=marcasBloque,
                           productosRecientes=productosRecientes,
                           productosPopulares=productosPopulares,
                           novedadesBanner=novedadesBanner)


@general_bp.route("/nuestras_marcas")
def nuestras_marcas():
    marcas = []
    valor = request.args.get("ctlg_products_order")  # Obtener el valor del orden

    if valor:
        if valor == "1":
            marcas = controlador_marcas.obtener_todas_marcas_recientes()
        elif valor == "2":
            marcas = controlador_marcas.obtener_todas_marcas_alfabetico(0)
        elif valor == "3":
            marcas = controlador_marcas.obtener_todas_marcas_alfabetico(1)
    else:
        marcas = controlador_marcas.obtener_todas_marcas_recientes()

    return render_template("nuestras_marcas.html", marcas = marcas)


@general_bp.route("/catalogo")
def catalogo():
    productos = []
    valor = request.args.get("ctlg_products_order")  # Obtener el valor del orden

    if valor:
        if valor == "1":  # Más Recientes
            productos = controlador_productos.obtenerEnTarjetasMasRecientes()
        elif valor == "2":  # Más Populares
            productos = controlador_productos.obtenerEnTarjetasMasPopulares_catalogo()
        elif valor == "3":  # Menor Precio
            productos = controlador_productos.obtenerEnTarjetasxPrecio(0)
        elif valor == "4":  # Mayor Precio
            productos = controlador_productos.obtenerEnTarjetasxPrecio(1)
        elif valor == "5":  # A - Z
            productos = controlador_productos.obtenerEnTarjetasAlfabetico(0)
        elif valor == "6":  # Z - A
            productos = controlador_productos.obtenerEnTarjetasAlfabetico(1)
    else:
        productos = controlador_productos.obtenerEnTarjetasMasRecientes()  # Valor predeterminado

    categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()
    return render_template("catalogo.html", productos=productos, categoriasFiltro=categoriasFiltro)


@general_bp.route("/buscar")
def buscar_elementos():
    nombreBusqueda = request.args.get("buscarElemento")
    productos = controlador_productos.buscarEnTarjetasMasRecientes(nombreBusqueda)
    categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()
    return render_template("catalogo.html", productos = productos, categoriasFiltro = categoriasFiltro , nombreBusqueda = nombreBusqueda)


@general_bp.route("/novedades")
def novedades():
    novedades_promo = controlador_novedades.mostrarNovedadesxTipo(3,5)
    novedades_anun = controlador_novedades.mostrarNovedadesxTipo(1,5)
    novedades_avis = controlador_novedades.mostrarNovedadesxTipo(2,5)
    productosOfertas = controlador_productos.obtenerEnTarjetasOfertas()
    return render_template("novedades.html" , productosOfertas = productosOfertas , novedades_promo = novedades_promo , novedades_anun = novedades_anun , novedades_avis = novedades_avis)


@general_bp.route("/promociones")
def promociones():
    promociones = controlador_novedades.mostrarNovedadesPromociones()
    if promociones:
        return render_template("promociones.html" , promociones = promociones)
    else:
        return redirect("/error")


@general_bp.route('/anuncios')
def anuncios():
    anuncios = controlador_novedades.mostrarNovedadesxTipo(1,0)
    if anuncios:
        return render_template('anuncios.html', anuncios=anuncios)
    else:
        return redirect("/error")


@general_bp.route('/avisos')
def avisos():
    avisos = controlador_novedades.mostrarNovedadesxTipo(2,0)
    if avisos:
        return render_template('avisos.html', avisos=avisos)
    else:
        return redirect("/error")


@general_bp.route("/error")
def error():
    return render_template("error.html")


@general_bp.route("/servicio_cliente") #falta
def servicio_cliente():
    tipos = controlador_contenido_info.obtener_tipos_contenido()
    return render_template("servicioCliente.html" , tipos = tipos)


@general_bp.route("/nosotros") #falta
def nosotros():
    info_domus = controlador_informacion_domus.obtener_informacion_domus()
    return render_template("nosotros.html" , info_domus = info_domus)


@general_bp.route("/contactanos")
def contactanos():
    motivos_comentario = controlador_motivo_comentario.obtener_motivos_disponibles()
    return render_template("contactanos.html", motivos=motivos_comentario)






@general_bp.route("/selectedCategoria=<int:id>")  #falta
def categoria(id):
    # try:
        categoria = controlador_categorias.obtener_categoria_por_id(id)
        if categoria and categoria[3] == 1:
            subcategorias = controlador_subcategorias.obtenerSubcategoriasXCategoria(id)
            novedadesCategoria = controlador_novedades.obtenerNovedadesCategoria(id)
            productosCategoria = controlador_productos.obtener_en_tarjetas_categoria(0,id,0)
            categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()
            return render_template("selectedCategoria.html", productosCategoria = productosCategoria , categoria = categoria, subcategorias = subcategorias , novedadesCategoria = novedadesCategoria , categoriasFiltro = categoriasFiltro)
    #     else:
    #         return redirect("/error")
    # except:
    #     return redirect("/error")


@general_bp.route("/selectedMarca=<int:id>")  #falta
def marca(id):
    # try:
        marca = controlador_marcas.obtener_marca_disponible_por_id(id)
        if marca and marca[4] == 1:
            if marca[3]:
                imagenMarcaFondo = marca[3]
            else:
                imagenMarcaFondo =  'static/img/elementos/domus_bg.jpg'

            productosMarca = controlador_productos.obtener_en_tarjetas_marca(0,id,0)
            novedadesMarca = controlador_novedades.obtenerNovedadesMarca(id)
            subcategoriasMarca = controlador_subcategorias.obtenerSubcategoriasXMarca(id)
            categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()
            return render_template("selectedMarca.html", marca = marca , novedadesMarca = novedadesMarca , imagenMarcaFondo = imagenMarcaFondo , productosMarca = productosMarca , subcategoriasMarca = subcategoriasMarca , categoriasFiltro = categoriasFiltro)

    #     else:
    #         return redirect("/error")
    # except:
    #     return redirect("/error")


@general_bp.route("/selectedProducto=<int:id>")  #falta
def producto(id):
    try:
        producto = controlador_productos.obtener_por_id(id)
        if producto and producto[11] == 1:
            categoria = controlador_subcategorias.obtenerCategoriasXSubcategoria(producto[10])
            marca = controlador_marcas.obtener_marca_disponible_por_id(producto[9])
            imgs_producto = controlador_imagenes_productos.obtener_imagenes_por_producto(id)
            caracteristicasPrincipales = controlador_caracteristicas_productos.obtenerCaracteristicasDisponiblesxProducto(id,1)
            caracteristicasSecundarias = controlador_caracteristicas_productos.obtenerCaracteristicasDisponiblesxProducto(id,0)
            productosSimilares = controlador_productos.obtener_en_tarjetas_subcategoria(id,producto[10],12)
            productosMarca = controlador_productos.obtener_en_tarjetas_marca(id,producto[9],12)
            return render_template("selectedProducto.html" , productosSimilares = productosSimilares , productosMarca = productosMarca , producto = producto , marca = marca, imgs_producto = imgs_producto, caracteristicasPrincipales = caracteristicasPrincipales, caracteristicasSecundarias = caracteristicasSecundarias, categoria = categoria)
        else:
            return redirect("/error")
    except:
        return redirect("/error")


@general_bp.route("/selectedNovedad=<int:id>")  #falta
def selectedNovedad(id):
    novedad = controlador_novedades.obtener_info_novedad_id(id)
    categoria = None
    marca = None
    if novedad[9]:
        categoria = controlador_subcategorias.obtenerCategoriasXSubcategoria(novedad[9])

    if novedad[8]:
        marca = controlador_marcas.obtener_marca_disponible_por_id(novedad[8])

    imagenes = controlador_imagenes_novedades.obtener_imagenes_disponibles_por_novedad(id)
    tipo = controlador_tipos_novedad.obtener_tipo_novedad_por_id(novedad[10])
    return render_template("selectedNovedad.html" , novedad = novedad , tipo = tipo , imagenes = imagenes , categoria = categoria , marca = marca)


@general_bp.route("/tipoNovedad=<int:id>")  #falta
def tipo_novedad(id):
    promo = controlador_novedades.promoselect(id)
    return render_template("selectedPromocion.html" , promo = promo)


@general_bp.route("/selectedPromocion=<int:id>")  #falta
def promocion(id):
    try:
        promo = controlador_novedades.promoselect(id)
        if promo:
            return render_template("selectedPromocion.html" , promo = promo)
        else:
            return redirect("/error")
    except:
        return redirect("/error")


@general_bp.route("/selectedAnuncio=<int:id>")
def anuncio(id):
    # try:
        anuncio = controlador_novedades.anuncioSelect(id)
        return render_template("selectedAnuncio.html", anuncio=anuncio)

    #     if anuncio:
    #         return render_template("selectedAnuncio.html", anuncio=anuncio)
    #     else:
    #         return redirect("/error")
    # except :
    #     return redirect("/error")


@general_bp.route("/selectedContenidoInformativo=<int:id>") #falta
def selectedContenidoInformativo(id):
    tipo = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
    datos = controlador_contenido_info.obtener_datos_contenido_por_tipo(id)
    return render_template("selectedContenidoInfo.html" , tipo = tipo , datos = datos)



@general_bp.route("/lista_productos")
def lista_productos():
    productos = controlador_productos.obtenerEnTarjetasMasRecientes() 

    return render_template(
        "lista_productos.html", 
        productos = productos,
        )
