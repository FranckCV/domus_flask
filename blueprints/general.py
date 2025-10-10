from flask import Blueprint, render_template, request, redirect
from controladores import (
    controlador_categorias,
    controlador_marcas,
    controlador_productos,
    controlador_novedades ,
    controlador_contenido_info ,
    controlador_informacion_domus ,
    controlador_motivo_comentario
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

