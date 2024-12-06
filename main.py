from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from flask_jwt import JWT, jwt_required, current_identity
# import uuid
from functools import wraps
from clase_user_v1.usuario import Usuario
import hashlib
import base64

import controladores.controlador_caracteristicas_productos as controlador_caracteristicas_productos
import controladores.controlador_caracteristicas_subcategorias as controlador_caracteristicas_subcategorias
import controladores.controlador_caracteristicas as controlador_caracteristicas
import controladores.controlador_carrito as controlador_carrito
import controladores.controlador_comentario as controlador_comentario
import controladores.controlador_contenido_info as controlador_contenido_info
import controladores.controlador_tipos_usuario as controlador_tipos_usuario
import controladores.controlador_pedido as controlador_pedido
import controladores.controlador_metodo_pago as controlador_metodo_pago
import controladores.controlador_motivo_comentario as controlador_motivo_comentario
import controladores.controlador_estado_pedido as controlador_estado_pedido
import controladores.controlador_metodo_pago as controlador_metodo_pago
import controladores.controlador_redes_sociales as controlador_redes_sociales
import controladores.controlador_informacion_domus as controlador_informacion_domus
import controladores.controlador_cupon as controlador_cupon
import controladores.controlador_marcas as controlador_marcas
import controladores.controlador_categorias as controlador_categorias
import controladores.controlador_productos as controlador_productos
import controladores.controlador_imagenes_productos as controlador_imagenes_productos
import controladores.controlador_tipos_novedad as controlador_tipos_novedad
import controladores.controlador_imagenes_novedades as controlador_imagenes_novedades
import controladores.controlador_subcategorias as controlador_subcategorias
import controladores.controlador_usuario_cliente as controlador_usuario_cliente
import controladores.controlador_novedades as controlador_novedades
import controladores.controlador_tipos_img_novedad as controlador_tipos_img_novedad
import controladores.controlador_detalle as controlador_detalle
import controladores.controlador_empleados as controlador_empleados
import controladores.controlador_lista_deseos as controlador_lista_deseos
import controladores.controlador_usuario_admin as controlador_usuario_admin

from datetime import datetime, date

from clases.clsMarca import Marca as clsMarca
from clases.clsProducto import Producto as clsProducto
from clases.clsSubcategoria import Subcategoria as clsSubcategoria
from clases.clsCategoria import Categoria as clsCategoria
from clases.clsPedido import Pedido as clsPedido
from clases.clsUsuario import Usuario as clsUsuario
from clases.clsImgProducto import ImgProducto as clsImgProducto
from clases.clsDetallesPedido import DetallesPedido as clsDetallesPedido
from clases.clsListaDeseos import ListaDeseos as clsListaDeseos
from clases.clsComentario import Comentario as clsComentario
from clases.clsMotivo_comentario import MotivoComentario as clsMotivoComentario
from clases.clsTipo_novedad import TipoNovedad as clsTipoNovedad
from clases.clsNovedad import Novedad as clsNovedad
from clases.clsCaracteristicas_producto import CaracteristicasProducto as clsCaracteristicaProducto
from clases.clsMetodoPago import MetodoPago as clsMetodoPago
from clases.clsTipoImgNovedad import TipoImgNovedad as clsTipoImgNovedad
from clases.clsImgNovedad import ImgNovedad as clsImgNovedad
from clases.clsEstadoPedido import EstadoPedido as clsEstadoPedido
from clases.clsTipoUsuario import TipoUsuario as clsTipoUsuario
from clases.clsCaracteristica import Caracteristica as clsCaracteristica
# from clases.clsCaracteristicas_subcategoria import CaracteristicasSubcategoria as clsCaracteristicaSubcategoria
from clases.clsRedesSociales import RedesSociales as clsRedesSociales
from clases.clsInformacionDomus import InformacionDomus as clsInformacionDomus
# from clases.clsTipoContenidoInfo import TipoContenidoInfo as clsTipoContenidoInfo
# from clases.clsContenidoInfo import ContenidoInfo as clsContenidoInfo
from clases.clsCupon import Cupon as clsCupon
from clases.clsCuponUsuario import CuponUsuario as clsCuponUsuario


# class User(object):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def __str__(self):
#         return "User(id='%s')" % self.id



# users = [
#     User(1, 'user1', 'abcxyz'),
#     User(2, 'user2', 'abcxyz'),
# ]


def authenticate(username, password):
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_email(username)
    if not data:
        return None
    user = Usuario(id=data[0], correo=data[1], contrasenia=data[2], tipo_usuario_id=data[3])
    
    if user and user.contrasenia == hashlib.sha256(password.encode('utf-8')).hexdigest():
        if user.tipo_usuario_id in [1, 2, 3]:
            return user
    
    return None

def identity(payload):
    user_id = payload['identity']
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    user = Usuario(id=data[0], correo=data[1], contrasenia=data[2])
    return user


def encstringsha256(cadena_legible):
    h = hashlib.new('sha256')
    h.update(bytes(cadena_legible, encoding='utf-8'))
    epassword = h.hexdigest()
    return epassword

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

logo_domus = 'img/elementos/logoDomus.png'

# General

@app.context_processor
def inject_globals():
    categoriasMenu = controlador_categorias.obtener_categorias_disponibles()
    marcasMenu = controlador_marcas.obtener_marcas_menu(10) 
    logo_foto = logo_domus
    redes_footer = controlador_redes_sociales.obtener_redes_sociales()
    conts_info_footer = controlador_contenido_info.obtener_tipos_contenido()
    datos_domus_main = controlador_informacion_domus.obtener_informacion_domus()
    logueado_dato = session.get('id') is not None
    user_id = session.get('id') if logueado_dato else None 
    lista_deseos = controlador_lista_deseos.obtenerListaDeseos(session.get('id'))
    lista_deseos_ids = [producto[0] for producto in lista_deseos] 
    return dict(
        marcasMenu=marcasMenu,
        logo_foto=logo_foto,
        categoriasMenu=categoriasMenu,
        redes_footer=redes_footer,
        conts_info_footer=conts_info_footer,
        datos_domus_main=datos_domus_main,
        logueado=logueado_dato,
        user_id=user_id , 
        lista_deseos_ids=lista_deseos_ids
    )


# PAGINAS GENERALES

cupon= 'DOMUSESMICASA50'

@app.route("/") #falta
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

@app.route("/nuestras_marcas")
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


@app.route("/catalogo")
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


@app.route("/buscar")
def buscar_elementos():
    nombreBusqueda = request.args.get("buscarElemento")
    productos = controlador_productos.buscarEnTarjetasMasRecientes(nombreBusqueda)
    categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()   
    return render_template("catalogo.html", productos = productos, categoriasFiltro = categoriasFiltro , nombreBusqueda = nombreBusqueda)


@app.route("/novedades") 
def novedades():
    novedades_promo = controlador_novedades.mostrarNovedadesxTipo(3,5)
    novedades_anun = controlador_novedades.mostrarNovedadesxTipo(1,5)
    novedades_avis = controlador_novedades.mostrarNovedadesxTipo(2,5)
    productosOfertas = controlador_productos.obtenerEnTarjetasOfertas()
    return render_template("novedades.html" , productosOfertas = productosOfertas , novedades_promo = novedades_promo , novedades_anun = novedades_anun , novedades_avis = novedades_avis)


@app.route("/promociones") 
def promociones():
    promociones = controlador_novedades.mostrarNovedadesPromociones()
    if promociones:
        return render_template("promociones.html" , promociones = promociones)
    else:
        return redirect("/error")


@app.route('/anuncios')
def anuncios():
    anuncios = controlador_novedades.mostrarNovedadesxTipo(1,0)
    if anuncios:
        return render_template('anuncios.html', anuncios=anuncios)
    else:
        return redirect("/error")
    

@app.route('/avisos')
def avisos():
    avisos = controlador_novedades.mostrarNovedadesxTipo(2,0)
    if avisos:
        return render_template('avisos.html', avisos=avisos)
    else:
        return redirect("/error")


@app.route("/error") 
def error():
    return render_template("error.html")


# PAGINAS ESPECIFICAS

@app.route("/selectedCategoria=<int:id>")  #falta
def categoria(id):
    try:
        categoria = controlador_categorias.obtener_categoria_por_id(id)
        if categoria and categoria[3] == 1:        
            subcategorias = controlador_subcategorias.obtenerSubcategoriasXCategoria(id)
            novedadesCategoria = controlador_novedades.obtenerNovedadesCategoria(id)
            productosCategoria = controlador_productos.obtener_en_tarjetas_categoria(0,id,0)
            categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()   
            return render_template("selectedCategoria.html", productosCategoria = productosCategoria , categoria = categoria, subcategorias = subcategorias , novedadesCategoria = novedadesCategoria , categoriasFiltro = categoriasFiltro)
        else:
            return redirect("/error")
    except:
        return redirect("/error")


@app.route("/selectedMarca=<int:id>")  #falta
def marca(id):
    try:
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
            
        else:
            return redirect("/error")
    except:
        return redirect("/error")


@app.route("/selectedProducto=<int:id>")  #falta
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


@app.route("/selectedNovedad=<int:id>")  #falta
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


@app.route("/tipoNovedad=<int:id>")  #falta
def tipo_novedad(id):
    promo = controlador_novedades.promoselect(id)
    return render_template("selectedPromocion.html" , promo = promo)


@app.route("/selectedPromocion=<int:id>")  #falta
def promocion(id):
    try:
        promo = controlador_novedades.promoselect(id)
        if promo:            
            return render_template("selectedPromocion.html" , promo = promo)
        else:
            return redirect("/error")
    except:
        return redirect("/error")


@app.route("/selectedAnuncio=<int:id>")
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


# PAGINAS INFORMATIVAS

@app.route("/servicio_cliente") #falta
def servicio_cliente():
    tipos = controlador_contenido_info.obtener_tipos_contenido()
    return render_template("servicioCliente.html" , tipos = tipos)


@app.route("/selectedContenidoInformativo=<int:id>") #falta
def selectedContenidoInformativo(id):
    tipo = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
    datos = controlador_contenido_info.obtener_datos_contenido_por_tipo(id)
    return render_template("selectedContenidoInfo.html" , tipo = tipo , datos = datos)

@app.route("/nosotros") #falta
def nosotros():
    info_domus = controlador_informacion_domus.obtener_informacion_domus()
    return render_template("nosotros.html" , info_domus = info_domus)


@app.route("/contactanos")
def contactanos():
    motivos_comentario = controlador_motivo_comentario.obtener_motivos_disponibles()
    return render_template("contactanos.html", motivos=motivos_comentario)


@app.route("/iniciar_sesion") #falta
def iniciar_sesion():
    return render_template("iniciar_sesion.html")


@app.route("/registrate") #falta
def registrate():

    return render_template("registrate.html")


######################CARRO######################
@app.route("/carrito") 
def carrito():
    productosPopulares = controlador_productos.obtenerEnTarjetasMasRecientes()
    print(session.get('id'))
    productos = controlador_detalle.obtener_Detalle(session.get('id'))  
    error_message = request.args.get("error_message")  
    
    return render_template("carrito.html", productosPopulares=productosPopulares, productos=productos, error_message=error_message or "")


@app.route('/obtener_cantidad_carrito', methods=['GET'])
def obtener_cantidad_carrito():
    usuario_id = session.get('id')
    
    if not usuario_id:
        return jsonify({"cantidad": 0}), 200
    
    cantidad_carrito = controlador_detalle.obtenerCantidadDetallePorUsuario(usuario_id)
    
    return jsonify({"cantidad": cantidad_carrito}), 200



@app.route("/obtener_resumen_carrito", methods=["GET"])
def obtener_resumen_carrito():
    usuario_id = session.get('id')
    
    if usuario_id is None:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    carrito = controlador_detalle.obtener_DetalleConDic(usuario_id)
    
    subtotal = 0
    for producto in carrito:
        subtotal += producto['precio'] * producto['cantidad']
    
    descuento = 0
    descuento_aplicado = False
    if cupon in request.args: 
        descuento = subtotal * 0.20  
        descuento_aplicado = True
    
    total = subtotal - descuento
    
    return jsonify({
        'carrito': carrito, 
        'subtotal': subtotal,
        'descuento': descuento,
        'total': total,
        'descuento_aplicado': descuento_aplicado
    })


@app.route("/agregar_carrito", methods=["POST"]) 
def agregar_carrito():
    producto_id = request.form["producto_id"]
    estado = 1
    usuario_id = session.get('id')
    
    if usuario_id is not None:
        pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
        
        if pedido_id is None:
            pedido_id = controlador_carrito.insertar_pedido(usuario_id, estado)
        
        result = controlador_carrito.insertar_detalle(producto_id, pedido_id)
        referrer = request.referrer
        
        if result is not None:
            if referrer and "carrito" in referrer:
                return redirect(url_for('carrito'))
            else:
                return '', 204
        else:
            return redirect(url_for('carrito', error_message="No se pudo agregar el producto al carrito."))
    
    else:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Regístrese para agregar al carrito")


@app.route("/aumentar_carro", methods=["POST"])
def aumentar_carro():
    producto_id = request.form.get("producto_id")
    print(f"Producto ID recibido: {producto_id}") 
    usuario_id = session.get('id')
    estado = 1 

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

    if pedido_id:
        result=controlador_carrito.aumentar_producto(pedido_id,producto_id)
        if result is None:
            return redirect('/carrito')
        else:
           return redirect(url_for('carrito', error_message=str(result)))
    else:
        print("No se encontró un pedido activo.")


@app.route("/disminuir_carro", methods=["POST"])
def disminuir_carro():
    producto_id = request.form["producto_id"]
    usuario_id =session.get('id')
    estado = 1

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

    if pedido_id:
        controlador_carrito.eliminar_producto(pedido_id,producto_id)
    
    return redirect('/carrito')


@app.route("/confirmar_carrito", methods=["POST"])
def confirmar_carrito():
    estado = 1
    usuario_id = session.get('id')
    
    valor_descuento=request.form.get('total_descuento')
    
    pedido_id=controlador_carrito.verificarIdPedido(usuario_id,estado)        

    subtotal=0
    productos_carrito = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)
    
    for producto in productos_carrito:
        cantidad = producto[3]  
        precio_unitario = producto[2]  
        total_producto = cantidad * precio_unitario
        subtotal += total_producto
    
    # print(f"Total del pedido: {subtotal}")
    # print(f"Descuento aplicado: {valor_descuento}")
    #Obtengo el pedido_id del usuario
    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    #Obtengo el detalle de ese pedido_id
    existencias = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)

    metodos_pago = controlador_metodo_pago.obtener_metodo_pago()
    
    if existencias and len(existencias) > 0:        
        return render_template("resumen_de_pedido.html", 
                               existencias=existencias, 
                               total_pagar=subtotal, 
                               valor_descuento=valor_descuento,
                               metodos_pago=metodos_pago)
    else:
        return redirect(url_for('carrito', error_message="El carrito no puede estar vacío"))


@app.route("/resumen_de_pedido")
def resumen_de_pedido():
    usuario=1
    pedido_id=controlador_carrito.ultimoPedido(usuario)    
    metodos_pago =controlador_metodo_pago.obtener_metodo_pago()
    print("los metodos son:",metodos_pago)
    existencias = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)
    # metodoID = request.form["metodo_pago"]
    # controlador_pedido.actualizar_MetPago_Pedido(pedido_id,metodoID)    
    return render_template("resumen_de_pedido.html", metodos_pago=metodos_pago, existencias=existencias)


@app.route('/cancelar_compra')
def cancelar_compra():
    usuario_id = session.get('id')
    estado_cancelado = 1    
    pedido_id=controlador_carrito.ultimoPedido(usuario_id)    
    controlador_carrito.cancelar_pedido(usuario_id, estado_cancelado,pedido_id)
    return redirect('/carrito')



###################################### CRUDS ##################################

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


def login_requerido(func):
    @wraps(func)  # Conserva el nombre y docstring de la función decorada
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:  # Si no hay sesión activa
            return redirect(url_for('login_admin'))  # Redirigir al login
        return func(*args, **kwargs)  # Ejecutar la función original si está autenticado
    return envoltura


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    # Si el usuario ya tiene sesión, redirigir al dashboard
    if 'usuario' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form.get('username')
        password = request.form.get('password')
        epassword = password

        if password != controlador_empleados.clave_default_empleado():
            epassword = encstringsha256(password)

        # Llamar al controlador para validar las credenciales
        if controlador_usuario_admin.confirmarDatosAdm(username, epassword):
            # Crear sesión
            session['usuario'] = username
            session['tipo_usuarioid'] = controlador_usuario_admin.obtenerTipoU(username)
            session['nombre_c'] = controlador_usuario_admin.obtenerNombresC(username)
            contrase = controlador_usuario_admin.obtenerContrasenia(username)
            user_id = controlador_usuario_admin.obtenerID(username)

            if contrase == controlador_empleados.clave_default_empleado():
                return redirect('/cambiar_contrasenia='+str(user_id))
            else:
                return redirect(url_for('dashboard'))  # Redirigir al dashboard

        # Mostrar un mensaje de alerta si las credenciales son inválidas
        flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")

    return render_template('login-admin.html')  # Renderizar formulario de login


@app.route('/api/session-data', methods=['GET'])
def get_session_data():
    if 'usuario' in session:
        return jsonify({
            'usuario': session.get('usuario', ''),
            'tipoid': session.get('tipo_usuarioid', ''),
            'nombres': session.get('nombre_c', '')
        })
    return jsonify({'error': 'No session data'}), 401


@app.route('/logout_admin')
def logout_admin():
    session.pop('usuario', None)  # Eliminar la sesión
    return redirect(url_for('login_admin'))  # Redirigir al login


@app.route("/error_adm")
def error_adm():
    return render_template("error_admin.html")


@app.route('/cuenta_administrativa')
@login_requerido #Decorador
def cuenta_administrativa():
    return render_template('cuenta_administrativa.html')


@app.route("/dashboard")
@login_requerido #Decorador
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login_admin'))
    return render_template("dashboard.html")


@app.route("/agregar_marca")
@login_requerido 
def formulario_agregar_marca():
    return render_template("agregar_marca.html")


@app.route("/guardar_marca", methods=["POST"])
@login_requerido 
def guardar_marca():
    marca = request.form["marca"]

    logo= request.files["logo"]
    logo_binario = logo.read()

    banner = request.files["banner"]

    if banner.filename == '':
        banner_binario = ''
    else:
        banner_binario = banner.read()
    

    controlador_marcas.insertar_marca(marca,logo_binario,banner_binario)
    return redirect("/listado_marcas")


@app.route("/listado_marcas")
@login_requerido 
def marcas():
    marcas = controlador_marcas.obtener_listado_marcas()
    return render_template("listado_marcas.html", marcas=marcas, active='marcas')


@app.route("/listado_marcas_buscar")
@login_requerido 
def marcas_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    marcas = controlador_marcas.buscar_listado_marcas_nombre(nombreBusqueda)

    return render_template("listado_marcas.html", marcas=marcas, active='marcas' , nombreBusqueda = nombreBusqueda)


@app.route("/eliminar_marca", methods=["POST"])
@login_requerido 
def eliminar_marca():
    controlador_marcas.eliminar_marca(request.form["id"])
    return redirect("/listado_marcas")


@app.route("/formulario_editar_marca=<int:id>")
@login_requerido 
def editar_marca(id):
    marca = controlador_marcas.obtener_listado_marca_por_id(id)
    return render_template("editar_marca.html", marca=marca)


@app.route("/actualizar_marca", methods=["POST"])
@login_requerido 
def actualizar_marca():
    id = request.form["id"]

    marca_element = controlador_marcas.obtener_imgs_marca_disponible_por_id(id)
    
    marca = request.form["marca"]
    disponibilidad = request.form["disponibilidad"]
    logo= request.files["logo"]
    banner = request.files["banner"]

    if logo.filename == '':
        logo_binario = marca_element[1]
    else:
        logo_binario = logo.read()

    if banner.filename == '':
        banner_binario = marca_element[2]
    else:
        banner_binario = banner.read()

    controlador_marcas.actualizar_marca(marca,logo_binario,banner_binario,disponibilidad,id)
    return redirect("/listado_marcas")



    # CARACTERISTICAS


@app.route("/listado_caracteristicas_buscar")
@login_requerido  
def caracteristicas_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
        categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
        caracteristicas = controlador_caracteristicas.buscar_listado_Caracteristicas_nombre(nombreBusqueda)    
        categorias = controlador_categorias.obtener_categorias()
        subcategorias =controlador_subcategorias.obtener_subcategorias()
        return render_template("listado_caracteristicas.html", caracteristicas = caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro , subcategorias=subcategorias , categorias = categorias , nombreBusqueda = nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_caracteristicas")
@login_requerido  
def caracteristicas():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
        categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
        caracteristicas = controlador_caracteristicas.obtener_listado_Caracteristicas()
        categorias = controlador_categorias.obtener_categorias()
        subcategorias = controlador_subcategorias.obtener_subcategorias()
        return render_template("listado_caracteristicas.html", caracteristicas=caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro, subcategorias=subcategorias, categorias=categorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_caracteristica")
@login_requerido  
def formulario_agregar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        categorias = controlador_categorias.obtener_categoriasXnombre()
        subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
        return render_template("agregar_caracteristica.html", subcategorias=subcategorias, categorias=categorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_caracteristica", methods=["POST"])
@login_requerido  
def guardar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        campo = request.form["campo"]
        subcategoria_id = request.form["subcategorySelect"]
        id_carac = controlador_caracteristicas.insertar_caracteristica(campo)
        controlador_caracteristicas.insertar_caracteristica_subcategoria(id_carac, subcategoria_id)
        return redirect("/listado_caracteristicas")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_caracteristica", methods=["POST"])
@login_requerido  
def eliminar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_caracteristicas.eliminar_caracteristica(request.form["id"])
        return redirect("/listado_caracteristicas")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_caracteristica=<int:id>")
@login_requerido  
def editar_caracteristica(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        carac = controlador_caracteristicas.obtener_caracteristica_por_id(id)
        sub_id = controlador_caracteristicas.obtener_carac_subcat_por_carac_id(id)
        categorias = controlador_categorias.obtener_categoriasXnombre()
        subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
        return render_template("editar_caracteristica.html", caracteristica=carac, categorias=categorias, subcategorias=subcategorias, sub_id=sub_id)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_caracteristica", methods=["POST"])
@login_requerido  
def actualizar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        sub_id = request.form["sub_id"]
        campo = request.form["campo"]
        disp = request.form["disponibilidad"]
        subcategoria_id = request.form["subcategorySelect"]
        controlador_caracteristicas.actualizar_caracteristica(campo, disp, subcategoria_id, sub_id, id)
        return redirect("/listado_caracteristicas")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_subcategorias")
@login_requerido
def subcategorias():
    if 'usuario' in session:
        username = session['usuario']  # Recuperar el usuario desde la sesión
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener el tipo de usuario

        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        # Si el tipo de usuario no es 2, continuar con el resto del flujo
        categorias = controlador_categorias.obtener_listado_categorias()
        subcategorias = controlador_subcategorias.obtener_listado_subcategorias()

        # Renderizar la plantilla con los datos
        return render_template(
            "listado_subcategorias.html",
            categorias=categorias,
            subcategorias=subcategorias
        )
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_subcategorias_buscar")
@login_requerido  
def subcategorias_buscar():
    if 'usuario' in session:
        username = session['usuario']  # Recuperar el usuario desde la sesión
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener el tipo de usuario

        # Verificar si el tipo de usuario es 2 y redirigir al dashboard si es así
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        # Si el tipo de usuario no es 2, continuar con la búsqueda
        nombreBusqueda = request.args.get("buscarElemento")
        categorias = controlador_categorias.obtener_listado_categorias()
        subcategorias = controlador_subcategorias.buscar_listado_subcategorias_nombre(nombreBusqueda)

        return render_template(
            "listado_subcategorias.html",
            categorias=categorias,
            subcategorias=subcategorias,
            nombreBusqueda=nombreBusqueda
        )
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_subcategoria")
@login_requerido  
def formulario_agregar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        categorias = controlador_categorias.obtener_categorias()
        return render_template("agregar_subcategoria.html", categorias=categorias, active='categorias')
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_subcategoria", methods=["POST"])
@login_requerido  
def guardar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        faicon_subcat = request.form["faicon_subcat"]
        categoria_id = request.form["categoria_id"]
        controlador_subcategorias.insertar_subcategoria(nombre, faicon_subcat, 1, categoria_id)
        return redirect("/listado_subcategorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_subcategoria", methods=["POST"])
@login_requerido  
def eliminar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        controlador_subcategorias.eliminar_subcategoria(request.form["id"])
        return redirect("/listado_subcategorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_subcategoria=<int:id>")
@login_requerido  
def editar_subcategoria(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        subcategoria = controlador_subcategorias.obtener_subcategoria_por_id(id)
        categorias = controlador_categorias.obtener_categorias()
        return render_template("editar_subcategoria.html", subcategoria=subcategoria, categorias=categorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_subcategoria", methods=["POST"])
@login_requerido  
def actualizar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        id = request.form["id"]
        nombre = request.form["nombre"]
        faicon_subcat = request.form["faicon_subcat"]
        disponibilidad = request.form["disponibilidad"]
        categoria_id = request.form["categoria_id"]
        controlador_subcategorias.actualizar_subcategoria(nombre, faicon_subcat, disponibilidad, categoria_id, id)
        return redirect("/listado_subcategorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_categoria")
@login_requerido  
def formulario_agregar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        return render_template("agregar_categoria.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_categoria", methods=["POST"])
@login_requerido  
def guardar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        categoria = request.form["categoria"]
        faicon_cat = request.form["faicon_cat"]
        controlador_categorias.insertar_categoria(categoria, faicon_cat, 1)
        return redirect("/listado_categorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_categorias")
@login_requerido  
def categorias():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        categorias = controlador_categorias.obtener_listado_categorias()
        subcategorias = controlador_subcategorias.obtener_subcategorias()
        return render_template("listado_categorias.html", categorias=categorias, subcategorias=subcategorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_categoria", methods=["POST"])
@login_requerido  
def eliminar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        id = request.form["id"]
        categoria = controlador_categorias.obtener_categoria_id_relacion(id)
        result = categoria[4]

        if result != 0:
            return render_template("listado_categorias.html", error="La categoría tiene elementos asociados y no se puede eliminar. Redirigiendo en 3 segundos...", show_modal=True)
        else:
            controlador_categorias.eliminar_categoria(id)
            return redirect("/listado_categorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_categoria=<int:id>")
@login_requerido  
def editar_categoria(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        categoria = controlador_categorias.obtener_categoria_por_id(id)
        return render_template("editar_categoria.html", categoria=categoria)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_categoria", methods=["POST"])
@login_requerido  
def actualizar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2
        
        id = request.form["id"]
        categoria = request.form["categoria"]
        faicon_cat = request.form["faicon_cat"]
        disponibilidad = request.form["disponibilidad"]
        controlador_categorias.actualizar_categoria(categoria, faicon_cat, disponibilidad, id)
        return redirect("/listado_categorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/comentarios_listado")
@login_requerido  
def comentarios_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        comentarios = controlador_comentario.obtener_listado_comentarios()
        motivos = controlador_motivo_comentario.obtener_motivos_disponibles()

        return render_template("listado_comentarios.html", comentarios=comentarios, motivos=motivos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/ver_comentario=<int:id>")
@login_requerido  
def ver_comentario(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        comentario = controlador_comentario.ver_comentario_por_id(id)
        motivos = controlador_motivo_comentario.obtener_listado_motivos()

        return render_template("ver_comentario.html", comentario=comentario, motivos=motivos, id=id)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/comentarios_listado_buscar")
@login_requerido  
def comentarios_listado_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        comentarios = controlador_comentario.buscar_listado_comentarios_palabra(nombreBusqueda)
        motivos = controlador_motivo_comentario.obtener_motivos_disponibles()

        return render_template("listado_comentarios.html", comentarios=comentarios, motivos=motivos, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_comentario", methods=["POST"])
@login_requerido  
def guardar_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        motivo_comentario_id = request.form["motivo_comentario_id"]
        mensaje = request.form["mensaje"]

        # Estado por defecto: pendiente (1)
        estado = 0

        # Usuario id como null (si no está disponible)
        usuario_id = None

        controlador_comentario.insertar_comentario(nombres, apellidos, email, telefono, mensaje, estado, motivo_comentario_id, usuario_id)

        return redirect("/")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_comentario", methods=["POST"])
@login_requerido  
def eliminar_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_comentario.eliminar_comentario(request.form["id"])
        return redirect("/comentarios_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/estado_comentario", methods=["POST"])
@login_requerido  
def estado_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_comentario.estado_comentario(request.form["id"])
        return redirect(request.referrer)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/estado_comentario_respondido", methods=["POST"])
@login_requerido  
def estado_comentario_respondido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_comentario.estado_comentario_respondido(request.form["id"])
        return redirect(request.referrer)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/motivos_comentario_listado")
@login_requerido  
def motivos_comentario_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        motivos = controlador_motivo_comentario.obtener_listado_motivos()
        return render_template("listado_motivos_comentarios.html", motivos=motivos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/motivos_comentario_buscar")
@login_requerido  
def motivos_comentario_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        motivos = controlador_motivo_comentario.buscar_listado_motivos_nombre(nombreBusqueda)
        return render_template("listado_motivos_comentarios.html", motivos=motivos, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_motivo_comentario")
@login_requerido  
def formulario_agregar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_motivo_comentario.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_motivo_comentario", methods=["POST"])
@login_requerido  
def guardar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        motivo = request.form["motivo"]
        controlador_motivo_comentario.insertar_motivo(motivo, 1)
        return redirect("/motivos_comentario_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_motivo_comentario", methods=["POST"])
@login_requerido  
def eliminar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_motivo_comentario.eliminar_motivo(request.form["id"])
        return redirect("/motivos_comentario_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_motivo_comentario=<int:id>")
@login_requerido  
def editar_motivo_comentario(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        motivo_comentario = controlador_motivo_comentario.obtener_motivo_por_id(id)
        return render_template("editar_motivo_comentario.html", motivo_comentario=motivo_comentario)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_motivo_comentario", methods=["POST"])
@login_requerido  
def actualizar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        motivo = request.form["motivo"]
        disponibilidad = request.form["disponibilidad"]
        controlador_motivo_comentario.actualizar_motivo(motivo, disponibilidad, id)
        return redirect("/motivos_comentario_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/cambiar_contrasenia=<int:id>")
@login_requerido  
def cambiar_contrasenia(id):
    usuario = controlador_empleados.obtener_usuario_por_id(id)
    clave_default = controlador_empleados.clave_default_empleado()
    clave_actual = None
    if usuario[9] == controlador_empleados.clave_default_empleado():
        clave_actual = clave_default
    return render_template("nueva_contrasenia_admin.html", usuario=usuario , clave_actual = clave_actual)
    

@app.route("/guardar_contrasenia_empleado", methods=["POST"])
@login_requerido  
def guardar_contrasenia_empleado():
    id = request.form["id"]
    contrasenia = request.form["contrasenia"]
    confcontrasenia = request.form["confcontrasenia"]
    password = encstringsha256(contrasenia)
    if contrasenia == confcontrasenia:
        controlador_empleados.cambiar_contrasenia_usuario(password,id)
        return redirect("/dashboard")
    else:
        return redirect("/cambiar_contrasenia="+id)

    
@app.route("/empleados_listado")
@login_requerido  
def empleados_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuarios = controlador_empleados.obtener_listado_usuarios_empleados()
        tipos_usuarios = controlador_tipos_usuario.obtener_tipos_usuario()
        imagenes = controlador_empleados.obtener_listado_imagenes_usuario_empleado()
        return render_template("listado_empleados.html", usuarios=usuarios, tipos_usuarios=tipos_usuarios, imagenes=imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/empleados_listado_buscar")
@login_requerido  
def empleados_listado_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        usuarios = controlador_empleados.buscar_listado_usuarios_empleados_nombre(nombreBusqueda)
        tipos_usuarios = controlador_tipos_usuario.obtener_tipos_usuario()
        imagenes = controlador_empleados.obtener_listado_imagenes_usuario_empleado()
        return render_template("listado_empleados.html", usuarios=usuarios, tipos_usuarios=tipos_usuarios, nombreBusqueda=nombreBusqueda, imagenes=imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/ver_empleado=<int:id>")
@login_requerido  
def ver_empleado(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_empleados.ver_info_usuario_empleado(id)
        imagen = controlador_empleados.obtener_imagen_usuario_empleado_id(id)
        return render_template("ver_usuario_empleado.html", usuario=usuario, imagen=imagen)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_empleado")
@login_requerido  
def formulario_agregar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_empleado.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_empleado", methods=["POST"])
@login_requerido  
def guardar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        doc_identidad = request.form["doc_identidad"]
        
        # Verificar si se subió una imagen
        img_usuario = request.files["img_usuario"].read() if "img_usuario" in request.files and request.files["img_usuario"].filename != '' else None
        
        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        contraseña = controlador_empleados.clave_default_empleado()  
        # contraseña = request.form["contraseña"]  # Aquí se mantiene la contraseña sin cifrado
        
        disponibilidad = 1

    # Verificar si el correo ya existe
        if controlador_empleados.verificar_correo_existente(correo):
            error = "El correo se encuentra registrado. Intente con otro correo."
            return render_template("agregar_empleado.html", error=error, nombres=nombres, apellidos=apellidos, doc_identidad=doc_identidad, genero=genero, fecha_nacimiento=fecha_nacimiento, telefono=telefono, correo=correo)

        controlador_empleados.insertar_usuario(
            nombres, apellidos, doc_identidad, img_usuario, genero, 
            fecha_nacimiento, telefono, correo, contraseña, disponibilidad
        )
        return redirect("/empleados_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_empleado", methods=["POST"])
@login_requerido  
def actualizar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        doc_identidad = request.form["doc_identidad"]
        
        img_usuario = request.files["img_usuario"].read() if "img_usuario" in request.files and request.files["img_usuario"].filename != '' else None
        
        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        # contraseña = request.form["contraseña"]  # Aquí también se mantiene la contraseña sin cifrado
        disponibilidad = request.form["disponibilidad"]

        # epassword = encstringsha256(contraseña)
        controlador_empleados.actualizar_usuario_empleado(
            nombres, apellidos, doc_identidad, img_usuario, genero, 
            fecha_nacimiento, telefono, correo, disponibilidad, id
        )
        return redirect("/empleados_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_empleado=<int:id>")
@login_requerido  
def editar_empleado(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_empleados.obtener_usuario_por_id(id)
        imagen = controlador_empleados.obtener_imagen_usuario_empleado_id(id)
        return render_template("editar_empleado.html", usuario=usuario, imagen=imagen)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_empleado", methods=["POST"])
@login_requerido  
def eliminar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_empleados.eliminar_usuario(request.form["id"])
        return redirect("/empleados_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_img_producto", methods=["POST"])
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


@app.route("/agregar_producto")
@login_requerido #Decorador
def formulario_agregar_producto():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("agregar_producto.html", marcas = marcas, subcategorias = subcategorias , categorias = categorias)


@app.route("/guardar_producto", methods=["POST"])
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

    id_pro = controlador_productos.insertar_producto(nombre,price_regular,price_online,precio_oferta,infoAdicional,stock,marca_id,subcategoria_id)
    controlador_imagenes_productos.insertar_img_producto(nombre,imagen_bin,1,id_pro)
    
    files = request.files.getlist('imgsProd')
    for file in files:
        nom_file = nombre+'_'+file.filename
        data = file.read()
        controlador_imagenes_productos.insertar_img_producto(nom_file,data,0,id_pro)

    return redirect("/listado_productos")


@app.route("/listado_productos")
@login_requerido
def productos():
    productos = controlador_productos.obtener_listado_productos()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias)


@app.route("/listado_productos_buscar")
@login_requerido
def productos_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    productos = controlador_productos.buscar_listado_productos_nombre(nombreBusqueda)
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias , nombreBusqueda = nombreBusqueda)


@app.route("/eliminar_producto", methods=["POST"])
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


@app.route("/eliminar_producto2", methods=["POST"])
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


@app.route("/ver_producto=<int:id>")
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


@app.route("/formulario_editar_producto=<int:id>")
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


@app.route("/actualizar_producto", methods=["POST"])
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

    controlador_productos.actualizar_producto(nombre, price_regular, price_online, precio_oferta, infoAdicional, stock, disponibilidad, marca_id, subcategoria_id, id)
    controlador_imagenes_productos.actualizar_img_producto(imagen_bin,id)
    
    return redirect("/listado_productos")


@app.route("/listado_tipos_novedad")
@login_requerido  
def listado_tipos_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_novedad = controlador_tipos_novedad.obtener_listado_tipos_novedad()
        return render_template("listado_tipos_novedad.html", tipos_novedad=tipos_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_novedad")
@login_requerido  
def formulario_agregar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_novedad.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_novedad", methods=["POST"])
@login_requerido  
def guardar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre_tipo = request.form["nombre_tipo"]
        controlador_tipos_novedad.insertar_tipo_novedad(nombre_tipo)
        return redirect("/listado_tipos_novedad")  # Aquí se muestra el listado de tipos de novedades
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_novedad", methods=["POST"])
@login_requerido  
def eliminar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_tipos_novedad.eliminar_tipo_novedad(request.form["id"])
        return redirect("/listado_tipos_novedad")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_novedad=<int:id>")
@login_requerido  
def editar_tipo_novedad(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo_novedad = controlador_tipos_novedad.obtener_tipo_novedad_por_id(id)
        id_tipo = id
        return render_template("editar_tipo_novedad.html", tipo_novedad=tipo_novedad, id_tipo=id_tipo)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_novedad", methods=["POST"])
@login_requerido  
def actualizar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre_tipo = request.form["nombre_tipo"]
        disponibilidad = request.form["disponibilidad"]
        controlador_tipos_novedad.actualizar_tipo_novedad(nombre_tipo, disponibilidad, id)
        return redirect("/listado_tipos_novedad")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_novedad")
@login_requerido 
def formulario_agregar_novedad():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("agregar_novedad.html", marcas=marcas, subcategorias=subcategorias, categorias = categorias, tipos_novedad=tipos_novedad, tipos_img_novedad = tipos_img_novedad)


@app.route("/guardar_novedad", methods=["POST"])
@login_requerido 
def guardar_novedad():
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    
    nombre = request.form["nombre"]
    titulo = request.form["titulo"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    terminos = request.form["terminos"]
    marca_id = request.form["marca"]
    subcategoria_id = request.form["subcategorySelect"]
    tipo_novedad_id = request.form["tipo_novedad"]

    idNovedad = controlador_novedades.insertarNovedad(
        nombre, 
        titulo, 
        fecha_inicio, 
        fecha_vencimiento, 
        terminos, 
        marca_id, 
        subcategoria_id, 
        tipo_novedad_id
    )
    
    files = request.files.getlist('imgNovedad')
    for file in files:
        nom_file = nombre+'_'+file.filename
        data = file.read()
        controlador_imagenes_novedades.insertar_imagen_novedad(nom_file, data, 2, idNovedad)

    # return render_template('agregar_img_novedad.html', novedad_id=idNovedad, tipos_img_novedad = tipos_img_novedad)
    return redirect("/listado_novedades")


@app.route("/listado_novedades")
@login_requerido 
def novedades_listado():
    novedades = controlador_novedades.obtener_listado_novedades()
    imgs_nov = controlador_imagenes_novedades.obtener_todas_imagenes_novedad()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias , categorias=categorias , imgs_nov = imgs_nov)


@app.route("/listado_novedades_buscar")
@login_requerido 
def novedades_listado_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    novedades = controlador_novedades.buscar_listado_novedades_nombre_titulo(nombreBusqueda)
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias , nombreBusqueda = nombreBusqueda)


@app.route("/ver_novedad=<int:id>")
@login_requerido 
def ver_novedad(id):
    novedad = controlador_novedades.obtener_novedad_id(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    imagenes = controlador_imagenes_novedades.obtener_imagenes_novedad_id(id)
    return render_template("ver_novedad.html", novedad=novedad, marcas=marcas , subcategorias = subcategorias, id = id ,tiposNovedad = tiposNovedad , imagenes = imagenes , categorias = categorias)


@app.route("/eliminar_novedad", methods=["POST"])
@login_requerido 
def eliminar_novedad():
    controlador_novedades.eliminarNovedad(request.form["id"])
    return redirect("/listado_novedades")


@app.route("/formulario_editar_novedad=<int:id>")
@login_requerido 
def editar_novedad(id):
    novedad = controlador_novedades.obtenerNovedadPorId(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    return render_template("editar_novedad.html", novedad=novedad, marcas=marcas, subcategorias=subcategorias, tipos_novedad=tiposNovedad, novedad_id = id , categorias = categorias)


@app.route("/actualizar_novedad", methods=["POST"])
@login_requerido 
def actualizar_novedad():
    id = request.form["id"]
    nombre = request.form["nombre"]
    titulo = request.form["titulo"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    terminos = request.form["terminos"]
    disponibilidad = request.form["disponibilidad"]
    marca_id = request.form["marca_id"]
    subcategoria_id = request.form["subcategorySelect"]
    if (subcategoria_id == "null" or subcategoria_id == None or subcategoria_id == 0):
        subcategoria_id = None
    tipo_novedad_id = request.form["tipo_novedad_id"]

    imagen = request.files["imagen"].read() if "imagen" in request.files else None

    controlador_novedades.actualizarNovedad(nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id, imagen, id)
    return redirect("/listado_novedades")


@app.route("/guardar_img_novedad", methods=["POST"])
@login_requerido  
def guardar_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        novedad_id = request.form["novedad_id"]
        nomImagen = request.form["nomImagen"]
        tipo_img_novedad_id = request.form["tipo_img_novedad"]
        img = request.files["imagen"]

        if img:
            imagen = img.read()
            controlador_imagenes_novedades.insertar_imagen_novedad(nomImagen, imagen, tipo_img_novedad_id, novedad_id)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_img_novedad=<int:novedad_id>")
@login_requerido  
def formulario_agregar_img_novedad(novedad_id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
        return render_template("agregar_img_novedad.html", novedad_id=novedad_id, tipos_img_novedad=tipos_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/img_novedades_listado=<int:novedad_id>")
@login_requerido  
def img_novedades_listado(novedad_id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        novedad = controlador_novedades.obtenerNovedadPorId(novedad_id)
        img_novedades = controlador_imagenes_novedades.obtener_imagenes_novedad_por_id(novedad_id=novedad_id)
        tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
        return render_template("listado_img_novedades.html", img_novedades=img_novedades, novedad_id=novedad_id, novedad = novedad , tipos_img_novedad = tipos_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_img_novedad", methods=["POST"])
@login_requerido  
def eliminar_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_imagenes_novedades.eliminar_imagen_novedad(request.form["id"])
        novedad_id = request.form["novedad_id"]
        return redirect(f"/img_novedades_listado={novedad_id}")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_img_novedad=<int:id>")
@login_requerido  
def editar_img_novedad(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        img_nov = controlador_imagenes_novedades.obtener_imagen_novedad_por_img_id(id)
        img_novedad = controlador_imagenes_novedades.obtener_imagenes_novedad_por_id(id)
        novedad_id = controlador_imagenes_novedades.obtener_novedad_id_por_imagen_id(id)
        tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
        return render_template("editar_img_novedad.html", img_novedad=img_novedad, tipos_img_novedad=tipos_img_novedad, novedad_id = novedad_id,id = id , img_nov = img_nov)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_img_novedad", methods=["POST"])
@login_requerido  
def actualizar_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        
        id = request.form["id"]
        nom_imagen = request.form["nomImagen"]
        tipo_img_novedad_id = request.form["tipo_img_novedad"]
        novedad_id = request.form["novedad_id"]
        controlador_imagenes_novedades.actualizar_imagen_novedad(id, nom_imagen, tipo_img_novedad_id, novedad_id)
        return redirect(f"/img_novedades_listado={novedad_id}")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/tipos_img_novedad_listado")
@login_requerido  
def tipos_img_novedad_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_img_novedad = controlador_tipos_img_novedad.obtener_listado_tipos_img_novedad()
        return render_template("listado_tipos_img_novedad.html", tipos_img_novedad=tipos_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_img_novedad")
@login_requerido  
def formulario_agregar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_img_novedad.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_img_novedad", methods=["POST"])
@login_requerido  
def guardar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo = request.form["tipo"]
        controlador_tipos_img_novedad.insertar_tipo_img_novedad(tipo, 1)
        return redirect("/tipos_img_novedad_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_img_novedad=<int:id>")
@login_requerido  
def editar_tipo_img_novedad(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo_img_novedad = controlador_tipos_img_novedad.obtener_tipo_img_novedad_por_id(id)
        return render_template("editar_tipo_img_novedad.html", tipo_img_novedad=tipo_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_img_novedad", methods=["POST"])
@login_requerido  
def actualizar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        tipo = request.form["tipo"]
        disponibilidad = request.form["disponibilidad"]
        controlador_tipos_img_novedad.actualizar_tipo_img_novedad(id, tipo, disponibilidad)
        return redirect("/tipos_img_novedad_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_img_novedad", methods=["POST"])
@login_requerido  
def eliminar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        controlador_tipos_img_novedad.eliminar_tipo_img_novedad(id)
        return redirect("/tipos_img_novedad_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/ver_tipo_contenido_info=<int:id>")
@login_requerido  
def ver_tipo_contenido_info(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        contenido = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
        articulos = controlador_contenido_info.obtener_datos_contenido_por_tipo(id)
        return render_template("ver_contenido_info.html", articulos=articulos, contenido=contenido)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_tipo_contenido_info")
@login_requerido  
def listado_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos = controlador_contenido_info.obtener_listado_tipos_contenido()
        return render_template("listado_tipo_contenido_info.html", tipos=tipos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_tipo_contenido_info_buscar")
@login_requerido  
def listado_tipo_contenido_info_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        tipos = controlador_contenido_info.buscar_listado_tipos_contenido_nombre(nombreBusqueda)
        return render_template("listado_tipo_contenido_info.html", tipos=tipos, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_contenido_info")
@login_requerido  
def formulario_agregar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_contenido_info.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_contenido_info", methods=["POST"])
@login_requerido  
def guardar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        faicon_cont = request.form["icono"]
        controlador_contenido_info.insertar_tipo_contenido_info(nombre, descripcion, faicon_cont)
        return redirect("/listado_tipo_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_contenido_info", methods=["POST"])
@login_requerido  
def actualizar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        faicon_cont = request.form["icono"]
        descripcion = request.form["descripcion"]
        disponibilidad = request.form["disponibilidad"]
        controlador_contenido_info.actualizar_tipo_contenido_info_por_id(nombre, descripcion, faicon_cont, disponibilidad, id)
        return redirect("/listado_tipo_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_contenido_info=<int:id>")
@login_requerido  
def editar_tipo_contenido_info(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
        return render_template("editar_tipo_contenido_info.html", tipo=tipo)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_contenido_info", methods=["POST"])
@login_requerido  
def eliminar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_contenido_info.eliminar_tipo_contenido_info(request.form["id"])
        return redirect("/listado_tipo_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_contenido_info")
@login_requerido  
def listado_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        datos = controlador_contenido_info.obtener_datos_contenido()
        secciones = controlador_contenido_info.obtener_listado_tipos_contenido()
        return render_template("listado_contenido_info.html", datos=datos, secciones=secciones)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_contenido_info_buscar")
@login_requerido  
def listado_contenido_info_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        datos = controlador_contenido_info.buscar_datos_contenido_info_titulo(nombreBusqueda)
        secciones = controlador_contenido_info.obtener_listado_tipos_contenido()
        return render_template("listado_contenido_info.html", datos=datos, secciones=secciones, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_contenido_info")
@login_requerido  
def formulario_agregar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        secciones = controlador_contenido_info.obtener_tipos_contenido()
        return render_template("agregar_contenido_info.html", secciones=secciones)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_contenido_info", methods=["POST"])
@login_requerido  
def guardar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        titulo = request.form["titulo"]
        cuerpo = request.form["cuerpo"]
        tipo = request.form["tipo"]
        controlador_contenido_info.insertar_contenido_info(titulo, cuerpo, tipo)
        return redirect("/listado_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_contenido_info", methods=["POST"])
@login_requerido  
def actualizar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        cuerpo = request.form["cuerpo"]
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        controlador_contenido_info.actualizar_contenido_info_por_id(titulo, cuerpo, tipo, id)
        return redirect("/listado_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_contenido_info=<int:id>")
@login_requerido  
def editar_contenido_info(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        secciones = controlador_contenido_info.obtener_tipos_contenido()
        tipo = controlador_contenido_info.obtener_contenido_info_por_id(id)
        return render_template("editar_contenido_info.html", tipo=tipo, secciones=secciones)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_contenido_info", methods=["POST"])
@login_requerido  
def eliminar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_contenido_info.eliminar_contenido_info(request.form["id"])
        return redirect("/listado_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_estado_pedido")
@login_requerido  
def listado_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        estados = controlador_estado_pedido.obtener_listado_estados_pedido()
        return render_template("listado_estados_pedidos.html", estados=estados)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_agregar_estado_pedido")
@login_requerido  
def formulario_agregar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_estado_pedido.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_estado_pedido", methods=["POST"])
@login_requerido  
def guardar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        controlador_estado_pedido.insertar_estado_pedido(nombre)
        return redirect("/listado_estado_pedido")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_estado_pedido", methods=["POST"])
@login_requerido  
def actualizar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        controlador_estado_pedido.actualizar_estado_pedido_por_id(nombre, id)
        return redirect("/listado_estado_pedido")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_estado_pedido=<int:id>")
@login_requerido  
def editar_estado_pedido(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        estado = controlador_estado_pedido.obtener_estado_pedido_por_id(id)
        return render_template("editar_estado_pedido.html", estado=estado)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_estado_pedido", methods=["POST"])
@login_requerido  
def eliminar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_estado_pedido.eliminar_estado_pedido(request.form["id"])
        return redirect("/listado_estado_pedido")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_metodo_pago")
@login_requerido  
def listado_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
        return render_template("listado_metodo_pago.html", metodos=metodos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_agregar_metodo_pago")
@login_requerido  
def formulario_agregar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_metodo_pago.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_metodo_pago", methods=["POST"])
@login_requerido  
def guardar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        controlador_metodo_pago.insertar_metodo_pago(nombre)
        return redirect("/listado_metodo_pago")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_metodo_pago", methods=["POST"])
@login_requerido  
def actualizar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        disponibilidad = request.form["disponibilidad"]
        controlador_metodo_pago.actualizar_metodo_pago_por_id(nombre, disponibilidad, id)
        return redirect("/listado_metodo_pago")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_metodo_pago=<int:id>")
@login_requerido  
def editar_metodo_pago(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        metodo = controlador_metodo_pago.obtener_metodo_pago_por_id(id)
        return render_template("editar_metodo_pago.html", metodo=metodo)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_metodo_pago", methods=["POST"])
@login_requerido  
def eliminar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_metodo_pago.eliminar_metodo_pago(request.form["id"])
        return redirect("/listado_metodo_pago")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_redes_sociales")
@login_requerido  
def listado_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        redes = controlador_redes_sociales.obtener_redes_sociales()
        return render_template("listado_redes_sociales.html", redes=redes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_agregar_redes_sociales")
@login_requerido  # Decorador
def formulario_agregar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_redes_sociales.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_redes_sociales", methods=["POST"])
@login_requerido  # Decorador
def guardar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        enlace = request.form["enlace"]
        icono = request.form["icono"]
        controlador_redes_sociales.insertar_redes_sociales(nombre, icono, enlace)
        return redirect("/listado_redes_sociales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_redes_sociales", methods=["POST"])
@login_requerido  # Decorador
def actualizar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        enlace = request.form["enlace"]
        icono = request.form["icono"]
        controlador_redes_sociales.actualizar_redes_sociales_por_id(nombre, icono, enlace, id)
        return redirect("/listado_redes_sociales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_redes_sociales=<int:id>")
@login_requerido  # Decorador
def editar_redes_sociales(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        red = controlador_redes_sociales.obtener_redes_sociales_por_id(id)
        return render_template("editar_redes_sociales.html", red=red)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_redes_sociales", methods=["POST"])
@login_requerido  # Decorador
def eliminar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_redes_sociales.eliminar_redes_sociales(request.form["id"])
        return redirect("/listado_redes_sociales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_cupones")
@login_requerido  
def listado_cupones():
    cupones = controlador_cupon.obtener_cupones()
    return render_template("listado_cupones.html", cupones = cupones)


@app.route("/formulario_agregar_cupones")
@login_requerido  
def formulario_agregar_cupones():
    return render_template("agregar_cupon.html")


@app.route("/eliminar_cupones", methods=["POST"])
@login_requerido  
def eliminar_cupones():
    controlador_cupon.eliminar_cupon(request.form["id"])
    return redirect("/listado_cupones")


@app.route("/guardar_cupones", methods=["POST"])
@login_requerido  
def guardar_cupones():
    codigo = request.form["codigo"]
    fecha_ini = request.form["fecha_inicio"]
    fecha_ven = request.form["fecha_vencimiento"]
    cant_dcto = request.form["cant_dcto"]
    controlador_cupon.insertar_cupon(codigo,fecha_ini,fecha_ven,cant_dcto)
    return redirect("/listado_cupones")


@app.route("/formulario_editar_cupones=<int:id>")
@login_requerido  
def editar_cupones(id):
    cupon = controlador_cupon.obtener_cupon_por_id(id)
    return render_template("editar_cupones.html", cupon=cupon)


@app.route("/actualizar_cupones", methods=["POST"])
@login_requerido  
def actualizar_cupones():
    id = request.form["id"]
    codigo = request.form["codigo"]
    fecha_ini = request.form["fecha_inicio"]
    fecha_ven = request.form["fecha_vencimiento"]
    cant_dcto = request.form["cant_dcto"]
    disponibilidad = request.form["disponibilidad"]
    controlador_cupon.actualizar_cupon_por_id(codigo,fecha_ini,fecha_ven,cant_dcto,disponibilidad,id)
    return redirect("/listado_cupones")


@app.route("/listado_datos_principales")
@login_requerido  # Decorador
def listado_datos_principales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        info = controlador_informacion_domus.obtener_informacion_domus()
        return render_template("ver_datos_principales.html", info=info)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_datos_principales=<int:id>")
@login_requerido  # Decorador
def editar_datos_principales(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        info = controlador_informacion_domus.obtener_informacion_domus_por_id(id)
        return render_template("editar_datos_principales.html", info=info)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_datos_principales", methods=["POST"])
@login_requerido  # Decorador
def actualizar_datos_principales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        info = controlador_informacion_domus.obtener_imgs_informacion_domus_por_id(id)

        correo = request.form["correo"]
        numero = request.form["numero"]
        descripcion = request.form["descripcion"]
        historia = request.form["historia"]
        vision = request.form["vision"]
        valores = request.form["valores"]
        mision = request.form["mision"]

        imgLogo = request.files["imglogo"]
        imgIcon = request.files["imgicon"]

        if imgLogo.filename == '':
            logo = info[1]
        else:
            logo = imgLogo.read()

        if imgIcon.filename == '':
            icon = info[2]
        else:
            icon = imgIcon.read()

        controlador_informacion_domus.actualizar_informacion_domus_por_id(correo, numero, logo, icon, descripcion, historia, vision, valores, mision, id)
        return redirect("/listado_datos_principales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_tipos_usuario")
@login_requerido  
def listado_tipos_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_usuario = controlador_tipos_usuario.obtener_listado_tipos_usuario()
        return render_template("listado_tipos_usuario.html", tipos_usuario=tipos_usuario)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_usuario")
@login_requerido  
def formulario_agregar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_usuario.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_usuario", methods=["POST"])
@login_requerido  
def guardar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo = request.form["tipo"]
        descripcion = request.form["descripcion"]
        imagen = request.files["img_user"]
        img_binario = imagen.read()

        controlador_tipos_usuario.insertar_tipo_usuario(tipo, descripcion, img_binario)
        return redirect("/listado_tipos_usuario")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_usuario=<int:id>")
@login_requerido 
def editar_tipo_usuario(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo_usuario = controlador_tipos_usuario.obtener_tipo_usuario_por_id(id)
        return render_template("editar_tipo_usuario.html", tipo_usuario=tipo_usuario)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_usuario", methods=["POST"])
@login_requerido  
def actualizar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        imagen_user = controlador_tipos_usuario.obtener_img_tipo_usuario_por_id(id)
        tipo = request.form["tipo"]
        descripcion = request.form["descripcion"]
        imagen = request.files["img_user"]

        if imagen.filename == '':
            img_binario = imagen_user[0]
        else:
            img_binario = imagen.read()

        disp = request.form.get("disponibilidad")

        controlador_tipos_usuario.actualizar_tipo_usuario(id, tipo, descripcion, img_binario, disp)
        return redirect("/listado_tipos_usuario")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_usuario", methods=["POST"])
@login_requerido  
def eliminar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        controlador_tipos_usuario.eliminar_tipo_usuario(id)
        return redirect("/listado_tipos_usuario")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_clientes")
@login_requerido  
def listado_clientes():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuarios_clientes = controlador_usuario_cliente.obtener_listado_usuarios_clientes()
        imagenes = controlador_usuario_cliente.obtener_listado_imagenes_usuario_cliente()
        return render_template("listado_clientes.html", usuarios_clientes=usuarios_clientes , imagenes = imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_clientes_buscar")
@login_requerido  
def listado_clientes_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        usuarios_clientes = controlador_usuario_cliente.buscar_listado_usuarios_clientes_nombre(nombreBusqueda)
        imagenes = controlador_usuario_cliente.obtener_listado_imagenes_usuario_cliente()
        return render_template("listado_clientes.html", usuarios_clientes=usuarios_clientes , nombreBusqueda = nombreBusqueda , imagenes = imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/ver_cliente=<int:id>")
@login_requerido  
def ver_cliente(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_usuario_cliente.ver_info_usuario_cliente(id)
        imagen = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
        pedidos = controlador_pedido.obtener_listado_pedidos_usuario_id(id)
        estados = controlador_estado_pedido.obtener_listado_estados_pedido()
        metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
        return render_template("ver_usuario_cliente.html", usuario = usuario , pedidos = pedidos , estados = estados , metodos = metodos , imagen = imagen)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_cliente=<int:id>")
@login_requerido  
def editar_cliente(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(id)
        imagen = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
        return render_template("editar_cliente.html", usuario=usuario , imagen = imagen)

    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_cliente", methods=["POST"])
@login_requerido  
def actualizar_cliente():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        img_usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(id)

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        doc_identidad = request.form["doc_identidad"]
        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        disponibilidad = request.form["disponibilidad"]

        imagen = request.files["img_usuario"]
        if imagen.filename == '':
            img_bin = img_usuario[4]
        else:
            img_bin = imagen.read()

        controlador_usuario_cliente.actualizar_usuario_cliente(id, nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, disponibilidad,img_bin)
        return redirect("/listado_clientes")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_cliente", methods=["POST"])
@login_requerido  
def eliminar_cliente():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        controlador_usuario_cliente.eliminar_usuario_cliente(id)
        return redirect("/listado_clientes")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa






# def registrar_usuario():
#     email = request.form['username']
#     password = request.form['password']
#     confpassword = request.form['confpassword']

#     if password == confpassword:
#         h = hashlib.new('sha256')
#         h.update(bytes(password, encoding='utf-8'))
#         epassword = h.hexdigest()
#         controlador_users.registrar_usuario(email, epassword)
#         return redirect("/login")
#     else:
#         return redirect("/signup")

@app.route("/registrar_cliente", methods=["POST"])
def registrar_cliente():
    try:
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        dni = request.form["dni"]
        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        password = request.form["password"]
        disponibilidad = 1
        tipo_usuario = 3

        epassword = encstringsha256(password)

        result = controlador_usuario_cliente.insertar_usuario(
            nombres, apellidos, dni, genero, fecha_nacimiento, telefono, correo, epassword, disponibilidad, tipo_usuario
        )

        if result == 1:
            
            usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_email(correo)
            user_id = usuario[0] 
            
            session['username'] = correo
            session['id'] = user_id
            resp = make_response(redirect(f"/perfil={user_id}"))
            resp.set_cookie('username', correo)
            return resp
        elif result == 0:
            return render_template(
                "iniciar_sesion.html",
                mostrar_modal=True,
                mensaje_modal="El correo usado ya fue registrado. Por favor, intente con otro."
            )
        else:
            return "Error al procesar la solicitud", 400
    except Exception as e:
        print(f"Error en registrar_cliente: {e}")
        return render_template(
            "iniciar_sesion.html",
            mostrar_modal=True,
            mensaje_modal="Error en el servidor. Por favor, intente más tarde."
        )


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email-login')
    password = request.form.get('password-login')
    user = controlador_usuario_cliente.obtener_usuario_cliente_por_email(email)
    
    # if user and user[2]==epassword:
    #     session['username']=email
    #     resp=make_response(redirect("/"))
    #     resp.set_cookie('username',email)
    #     return resp
    if user:
        epassword = encstringsha256(password)
        if user[2] == epassword:
            session['id'] = user[0]
            session['username'] = email

            resp = make_response(redirect("/"))
            resp.set_cookie('username', email)
            return resp
        else:
            return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Contraseña incorrecta.")
    else:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Usuario no registrado.")


@app.route("/logout")
def logout():
    session.clear() 
    
    resp = make_response(redirect('/'))
    
    resp.delete_cookie('username') 

    return resp

from flask import redirect, make_response

@app.route('/cambiar_contrasenia_cliente', methods=['GET', 'POST'])
def cambiar_contrasenia_cliente():
    user_id = session.get('id')
    usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    img = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)
    
    if request.method == 'POST':
        current_password = request.form['current-password']
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']
        
        if new_password != confirm_password:
            error_message = "Las contraseñas no coinciden."
            return render_template('cambiarContraseñaCliente.html', error_message=error_message, user_id=user_id, usuario=usuario, img=img)

        if usuario and usuario[9] == encstringsha256(current_password): 
            controlador_usuario_cliente.cambiar_contrasenia(user_id, encstringsha256(new_password))
            
            session.clear()
            
            resp = make_response(redirect('/iniciar_sesion'))  
            resp.delete_cookie('username') 
            return resp  

        else:
            error_message = "La contraseña actual es incorrecta."
            return render_template('cambiarContraseñaCliente.html', error_message=error_message, user_id=user_id, usuario=usuario, img=img)

    return render_template('cambiarContraseñaCliente.html', user_id=user_id, usuario=usuario, img=img)





# @app.route("/iniciar_sesion" , methods=["POST"])
# def iniciar_sesion():
#     email = request.form['username']
#     password = request.form['password']
#     user = controlador_users.obtener_user_por_email(email)
#     epassword=encstringsha256(password)


#     if user and user[2] == epassword:
#         session['username'] = email
#         resp = make_response(redirect("/discos"))
#         resp.set_cookie('username',email)
#         #return redirect("/discos")
#         return resp
#     else:
#         return redirect("/login")

##################################### PARA PERFIL #################################################

@app.route("/perfil=<int:user_id>")
def perfil(user_id):
    if 'id' in session and session['id'] == user_id:
        usuario=controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
        img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)
        return render_template('perfil.html', user_id=user_id,usuario=usuario,img=img )
    else:
        return redirect('/iniciar_sesion')


@app.route("/detalle_pedido_perfil=<int:user_id>")
def detalle_pedido_perfil(user_id):
    usuario=controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    pedidos = controlador_pedido.obtener_pedidos_usuario(user_id)
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()  
    img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)

    return render_template("miDetallePedido_perfil.html", 
                           pedidos=pedidos,  # Ahora pasamos todos los pedidos
                           metodos=metodos, user_id=user_id,usuario=usuario,img=img )


@app.route("/lista_deseos=<int:user_id>")
def lista_deseos(user_id):
    usuario=controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)
    lista=controlador_lista_deseos.obtenerListaDeseosConImagen(user_id)
    return render_template("listaDeseos.html",user_id=user_id,usuario=usuario,img=img, lista=lista )   
    

@app.route('/agregar_a_lista_deseos', methods=['POST'])
def agregar_a_lista_deseos():
    usuario_id = session.get('id')
    
    if not usuario_id:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Regístrese para agregar a la lista de deseos")

    producto_id = request.form['producto_id']
    
    controlador_lista_deseos.agregar_a_lista_deseos(usuario_id, producto_id)
    
    return '', 204
   
    
@app.route("/insertar_imagen_usuario", methods=['POST'])
def imagen_usuario():
    if 'imagen' not in request.files:
        flash('No se seleccionó ninguna imagen.', 'error')
        return redirect(url_for('perfil', user_id=session.get('id')))
    
    imagen = request.files["imagen"]
    if imagen.filename == '':
        flash('No se seleccionó ninguna imagen.', 'error')
        return redirect(url_for('perfil', user_id=session.get('id')))

    try:
        imagen_bin = imagen.read()
        id = session.get('id')
        controlador_usuario_cliente.insertar_imagen(id,imagen_bin)
        img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
        flash('Imagen actualizada correctamente.', 'success')
    except Exception as e:
        flash(f'Error al guardar la imagen: {e}', 'error')

    return redirect(url_for('perfil', user_id=session.get('id') ))


###################################CONFIRMAR PEDIDO###############################

@app.route("/confirmar_compra", methods=['POST'])
def confirmar_compra():
    usuario_id = session.get('id')
    fecha_compra = date.today()
    metodo_pago = request.form.get('metodo_pago')
    estado = 2

    pedido_id = controlador_carrito.ultimoPedido(usuario_id)

    subtotal = 0
    productos_carrito = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)
    
    for producto in productos_carrito:
        cantidad = producto[3]  
        precio_unitario = producto[2]  
        total_producto = cantidad * precio_unitario
        subtotal += total_producto

    controlador_pedido.actualizarPedido(pedido_id, fecha_compra, subtotal,metodo_pago,estado,usuario_id)

    return redirect("/")



############################CANCELAR PEDIDO#########################

#####################################LISTADO PEDIDOS#######################################

@app.route("/listado_pedidos")
def pedido():
    pedidos=controlador_pedido.obtener_listado_pedidos()
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_pedidos.html", pedidos = pedidos , estados = estados , metodos = metodos)


@app.route("/listado_pedidos_buscar")
def pedido_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    pedidos = controlador_pedido.buscar_listado_pedidos_usuario(nombreBusqueda)
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_pedidos.html", pedidos = pedidos , estados = estados , metodos = metodos , nombreBusqueda = nombreBusqueda)


@app.route("/eliminar_pedido", methods=["POST"])
def eliminar_pedido():
    id = request.form["id"]
    result=controlador_pedido.buscar_pedido_por_id(id)

    if result:
        return render_template("listado_pedidos.html", error="El pedido tiene detalles asociados y no se puede eliminar. Redirigiendo...", show_modal=True)
    else:
        controlador_pedido.eliminar_pedido(id)
        return redirect("/listado_pedidos")


@app.route("/detalle_pedido=<int:id>")
def detalle_pedido(id):
    detalles = controlador_detalle.obtener_listado_detalle_por_id_pedido(id)
    pedido = controlador_pedido.obtener_pedido_id(id)
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_detalle_pedido.html", detalles=detalles , pedido_id=id , pedido = pedido , estados = estados , metodos = metodos)


@app.route("/eliminar_detalle_pedido", methods=["POST"])
def eliminar_detalle_pedido():
    producto_id = request.form["producto_id"]
    pedido_id = request.form["pedido_id"]  
    controlador_detalle.eliminar_detalle(producto_id, pedido_id)
    
    existencia=controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)
    
    if existencia and len(existencia) > 0:
        return render_template('listado_detalle_pedido.html',id=pedido_id)
    else:
        controlador_pedido.eliminar_pedido(pedido_id)
        return redirect('listado_pedidos')


@app.route("/editar_detalle=<int:producto_id>&editar_detalle=<int:pedido_id>", methods=["GET", "POST"])
def editar_detalle(producto_id, pedido_id):
    detalle = controlador_detalle.obtener_detalle_por_ids(producto_id, pedido_id)
    
    productos =controlador_detalle.obtenerProductos()

    return render_template("editar_detalle.html", detalle=detalle, productos=productos, producto_id=producto_id, pedido_id=pedido_id)


@app.route("/actualizar_detalle_pedido", methods=["POST"])
def actualizar_detalle_pedido():
    producto_id = request.form["producto_id"]
    pedido_id = request.form["pedido_id"]
    cantidad = request.form["cantidad"]
        
    controlador_detalle.editar_detalle(producto_id, pedido_id, cantidad)
        
    return redirect(url_for('detalle_pedido', id=pedido_id))



# TEST DE API
@app.route("/api_obtenerdiscos")
@jwt_required()
def api_obtenerdiscos():
    discos = controlador_categorias.obtener_listado_categorias()
    return jsonify(discos)














############################################  APIs  ###############################################
# @app.route("/api_error_adm")  # /error_adm
# @app.route("/api_cuenta_administrativa")  # /cuenta_administrativa
# @app.route("/api_dashboard")  # /dashboard

## MARCAS ##
@app.route("/api_guardar_marca", methods=["POST"])
@jwt_required()
def api_guardar_marca():
    # Obtener los datos desde la solicitud
    marca_nombre = request.json["marca"]
    img_logo = request.json["img_logo"]
    img_banner = request.json.get("img_banner")  # Es opcional

    dictRespuesta = {}

    try:
        # Crear una instancia de la clase Marca
        marca = clsMarca(None, marca_nombre, img_logo, img_banner)

        # Llamar al método del controlador para insertar la marca
        controlador_marcas.insertar_marca(marca)
        
        dictRespuesta["status"] = 1
        dictRespuesta["message"] = "Marca registrada con éxito"
        dictRespuesta["data"] = {"id": marca.id, "marca": marca.marca}  # Devuelvo el id y el nombre de la marca

        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["message"] = f"Error al registrar la marca: {str(e)}"
        dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)



@app.route("/api_listado_marcas")
@jwt_required()
def api_listado_marcas():
    dictRespuesta = {}
    try:
        marcas = controlador_marcas.obtener_listado_marcas()
        dictRespuesta["status"] = 1
        dictRespuesta["message"] = "Listado de marcas obtenido correctamente"
        dictRespuesta["data"] = {
            "marcas": []
        }

        for marca in marcas:
            marca_data = {
                "id_marca": marca[0],
                "nombre_marca": marca[1],
                "logo": marca[2],
                "banner": marca[3],
                "fecha_registro": marca[4].strftime('%Y-%m-%d %H:%M:%S'),
                "disponibilidad": marca[5],
                "productos": marca[6],
                "novedades": marca[7]
            }
            dictRespuesta["data"]["marcas"].append(marca_data)
        
        dictRespuesta["data"]["total_marcas"] = len(marcas)
        
        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["message"] = f"Error al obtener el listado de marcas: {str(e)}"
        return jsonify(dictRespuesta)

import base64

@app.route("/api_listar_marca", methods=["POST"])
# @jwt_required()
def api_marca_por_id():
    dictRespuesta = {}
    try:
        # Obtener el ID del cuerpo de la solicitud JSON
        request_data = request.get_json()
        id = request_data.get('id')

        # Verificamos si el ID fue enviado
        if not id:
            dictRespuesta["status"] = 0
            dictRespuesta["message"] = "ID no proporcionado"
            dictRespuesta["data"] = {}
            return jsonify(dictRespuesta)
        
        # Llamamos a la función para obtener la marca por ID
        marca = controlador_marcas.obtener_marca_por_id(id)
        
        if marca:
            # Convertir los campos binarios (si existen) en base64
            logo_base64 = base64.b64encode(marca[2]).decode('utf-8') if marca[2] else None
            banner_base64 = base64.b64encode(marca[3]).decode('utf-8') if marca[3] else None
            
            dictRespuesta["status"] = 1
            dictRespuesta["message"] = "Marca obtenida correctamente"
            dictRespuesta["data"] = {
                "id_marca": marca[0],
                "nombre_marca": marca[1],
                "logo": logo_base64,
                "banner": banner_base64,
                "disponibilidad": marca[4],
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["message"] = "Marca no encontrada"
            dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["message"] = f"Error al obtener la marca: {str(e)}"
        dictRespuesta["data"] = {}
        return jsonify(dictRespuesta)



@app.route("/api_eliminar_marca", methods=["POST"])
@jwt_required()
def api_eliminar_marca():
    id_marca = request.json["id"]
    dictRespuesta = {}
    try:
        controlador_marcas.eliminar_marca(id_marca)
        dictRespuesta["status"] = 1
        dictRespuesta["message"] = "Marca eliminada con éxito"
        dictRespuesta["data"] = {}
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["message"] = f"Error al eliminar la marca: {str(e)}"
        dictRespuesta["data"] = {}
        return jsonify(dictRespuesta)


@app.route("/api_actualizar_marca", methods=["POST"])
@jwt_required()
def api_actualizar_marca():
    id_marca = request.json["id"]
    marca = request.json["marca"]
    img_logo = request.json.get("img_logo")
    img_banner = request.json.get("img_banner")
    disponibilidad = request.json["disponibilidad"]
    dictRespuesta = {}
    try:
        controlador_marcas.actualizar_marca(marca, img_logo, img_banner, disponibilidad, id_marca)
        dictRespuesta["status"] = 1
        dictRespuesta["message"] = "Marca actualizada con éxito"
        dictRespuesta["data"] = {}
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["message"] = f"Error al actualizar la marca: {str(e)}"
        dictRespuesta["data"] = {}
        return jsonify(dictRespuesta)

################# APIs PRODUCTOS ###################
@app.route("/api_listado_productos")
@jwt_required()
def api_listado_productos():
    dictRespuesta = {}
    try:
        productos = controlador_productos.obtener_listado_productos()
        productos_formateados = []

        for producto in productos:
            id_producto = producto[0]
            nombre_producto = producto[1]
            price_regular = producto[2]
            precio_online = producto[3]
            precio_oferta = producto[4]
            info_adicional = producto[5]
            stock = producto[6]
            fecha_registro = producto[7]
            disponibilidad = producto[8]
            cantidad_novedades = producto[9]
            cantidad_caracteristicas = producto[10]
            marca = producto[11]
            subcategoria = producto[12]
            
            if isinstance(fecha_registro, int):
                fecha_registro = datetime.fromtimestamp(fecha_registro)
            
            productos_formateados.append({
                "idproducto": id_producto,
                "nombre": nombre_producto,
                "price_regular": price_regular,
                "precio_online": precio_online,
                "precio_oferta": precio_oferta,
                "info_adicional": info_adicional,
                "stock": stock,
                "fecha_registro": fecha_registro.strftime("%Y-%m-%d %H:%M:%S"),
                "disponibilidad": disponibilidad,
                "cantidad_novedades": cantidad_novedades,
                "cantidad_caracteristicas": cantidad_caracteristicas,
                "marca": marca,
                "subcategoria": subcategoria
            })

        dictRespuesta["status"] = 1
        dictRespuesta["data"] = productos_formateados
        dictRespuesta["message"] = "Productos obtenidos correctamente"
        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el listado de productos: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_guardar_producto", methods=["POST"])
# @jwt_required()  # Si necesitas autenticación, puedes descomentar esta línea
def api_guardar_producto():
    dictRespuesta = {}
    try:
        # Recibir datos del producto
        nombre = request.json["nombre"]
        price_regular = request.json.get("price_regular", None)
        precio_online = request.json["precio_online"]
        precio_oferta = request.json.get("precio_oferta", None)
        info_adicional = request.json.get("info_adicional", "")
        stock = request.json["stock"]
        marcaid = request.json["marcaid"]
        subcategoriaid = request.json["subcategoriaid"]

        # Llamar a la función para insertar el producto y obtener su id
        id_producto = controlador_productos.insertar_producto(
            nombre, price_regular, precio_online, precio_oferta, 
            info_adicional, stock, marcaid, subcategoriaid
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Producto guardado con éxito"
        dictRespuesta["id"] = id_producto
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al guardar el producto: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_eliminar_producto", methods=["POST"])
# @jwt_required()
def api_eliminar_producto():
    dictRespuesta = {}
    try:
        id_producto = request.json["id"]
        controlador_productos.eliminar_producto(id_producto)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Producto eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el producto: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_producto", methods=["POST"])
# @jwt_required()
def api_actualizar_producto():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON
        id_producto = request.json["id"]
        nombre = request.json.get("nombre", "")
        price_regular = request.json.get("price_regular", None)
        precio_online = request.json["precio_online"]
        precio_oferta = request.json.get("precio_oferta", None)
        info_adicional = request.json.get("info_adicional", "")
        stock = request.json["stock"]
        marcaid = request.json["marcaid"]
        subcategoriaid = request.json["subcategoriaid"]
        disponibilidad = request.json["disponibilidad"]

        # Crear el objeto Pedido (aunque no es el mismo contexto, usaremos los parámetros de manera similar)
        producto = clsPedido(
            p_id=id_producto,
            p_fecha_compra=None,  # No es necesario para este contexto
            p_subtotal=None,      # No es necesario para este contexto
            p_METODO_PAGOid=None, # No es necesario para este contexto
            p_USUARIOid=None,     # No es necesario para este contexto
            p_ESTADO_PEDIDOid=None  # No es necesario para este contexto
        )
        
        # Pasar los datos del objeto a la función de actualización
        controlador_productos.actualizar_producto(
            nombre, price_regular, precio_online, precio_oferta, 
            info_adicional, stock, disponibilidad, marcaid, 
            subcategoriaid, producto.id  # Usar el id del objeto
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Producto actualizado con éxito"
        dictRespuesta["id"] = id_producto
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el producto: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_producto", methods=["POST"])
# @jwt_required()
def api_listar_producto():
    dictRespuesta = {}
    try:
        # Obtener el ID del producto desde el JSON
        id_producto = request.json["id"]
        
        # Llamar al controlador para obtener los detalles del producto por ID
        producto = controlador_productos.obtener_por_id(id_producto)
        
        if producto:
            # Si el producto existe, devolver los datos en formato JSON
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Producto encontrado"
            dictRespuesta["data"] = {
                "id": producto[0],
                "nombre": producto[1],
                "price_regular": producto[2],
                "precio_online": producto[3],
                "precio_oferta": producto[4],
                "info_adicional": producto[5],
                "stock": producto[6],
                "disponibilidad": producto[7],
                "marcaid": producto[8],
                "subcategoriaid": producto[9]
            }
        else:
            # Si no se encuentra el producto
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Producto no encontrado"
        
        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el producto: {str(e)}"
        return jsonify(dictRespuesta)



#############SUBCATEGORIA#############

@app.route("/api_listado_subcategorias")
# @jwt_required()
def api_listado_subcategorias():
    dictRespuesta = {}
    try:
        subcategorias = controlador_subcategorias.obtener_subcategorias()
        subcategorias_formateadas = []
        for subcategoria in subcategorias:
            subcategoria_id = subcategoria[0]
            subcategoria_nombre = subcategoria[1]
            faicon_subcat = subcategoria[2]
            disponibilidad_subcat = subcategoria[3]
            categoria_id = subcategoria[4]
            categoria_nombre = subcategoria[5]
            faicon_categoria = subcategoria[6]
            cantidad_productos = subcategoria[7]
            cantidad_novedades = subcategoria[8]

            subcategoria_formateada = {
                "subcategoria_id": subcategoria_id,
                "subcategoria": subcategoria_nombre,
                "faicon_subcat": faicon_subcat,
                "disponibilidad_subcat": disponibilidad_subcat,
                "categoria": {
                    "categoria_id": categoria_id,
                    "categoria_nombre": categoria_nombre,
                    "faicon_categoria": faicon_categoria
                },
                "cantidad_productos": cantidad_productos,
                "cantidad_novedades": cantidad_novedades
            }
            subcategorias_formateadas.append(subcategoria_formateada)

        dictRespuesta["status"] = 1
        dictRespuesta["data"] = subcategorias_formateadas
        dictRespuesta["mensaje"] = "Listado de subcategorías obtenido correctamente"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el listado de subcategorías: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_guardar_subcategoria", methods=["POST"])
# @jwt_required()  # Si necesitas autenticación, puedes descomentar esta línea
def api_guardar_subcategoria():
    dictRespuesta = {}
    try:
        # Obtener los datos desde el JSON
        subcategoria_nombre = request.json["subcategoria"]
        faicon_subcat = request.json["faicon_subcat"]
        disponibilidad = request.json["disponibilidad"]
        categoriaid = request.json["categoriaid"]

        # Crear una instancia del objeto Subcategoria
        subcategoria = clsSubcategoria(
            p_id=None,  # El ID será generado automáticamente por la base de datos
            p_subcategoria=subcategoria_nombre,
            p_faicon_subcat=faicon_subcat,
            p_disponibilidad=disponibilidad,
            p_CATEGORIAid=categoriaid
        )

        id_sub = controlador_subcategorias.insertar_subcategoria_api(
            subcategoria.subcategoria, 
            subcategoria.faicon_subcat, 
            subcategoria.disponibilidad, 
            subcategoria.CATEGORIAid
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Subcategoría registrada con éxito"
        dictRespuesta["data"] = {
            "id": id_sub,
            "subcategoria": subcategoria.subcategoria,
            "faicon_subcat": subcategoria.faicon_subcat,
            "disponibilidad": subcategoria.disponibilidad,
            "categoriaid": subcategoria.CATEGORIAid
        }
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al registrar la subcategoría: {str(e)}"
        return jsonify(dictRespuesta)



@app.route("/api_eliminar_subcategoria", methods=["POST"])
# @jwt_required()
def api_eliminar_subcategoria():
    dictRespuesta = {}
    try:
        id_subcategoria = request.json["id"]
        controlador_subcategorias.eliminar_subcategoria(id_subcategoria)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Subcategoría eliminada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la subcategoría: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_subcategoria", methods=["POST"])
# @jwt_required()
def api_actualizar_subcategoria():
    dictRespuesta = {}
    try:
        id_subcategoria = request.json["id"]
        subcategoria_nombre = request.json.get("subcategoria", "")
        faicon_subcat = request.json.get("faicon_subcat", "")
        disponibilidad = request.json["disponibilidad"]
        categoriaid = request.json["categoriaid"]

        subcategoria = clsSubcategoria(
            p_id=id_subcategoria,
            p_subcategoria=subcategoria_nombre,
            p_faicon_subcat=faicon_subcat,
            p_disponibilidad=disponibilidad,
            p_CATEGORIAid=categoriaid
        )

        controlador_subcategorias.actualizar_subcategoria(
            subcategoria.subcategoria,
            subcategoria.faicon_subcat,
            subcategoria.disponibilidad,
            subcategoria.CATEGORIAid,
            subcategoria.id
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Subcategoría actualizada con éxito"
        dictRespuesta["id"] = id_subcategoria
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la subcategoría: {str(e)}"
        return jsonify(dictRespuesta)
    
@app.route("/api_listar_subcategoria", methods=["POST"])
# @jwt_required()  # Si necesitas autenticación, puedes descomentar esta línea
def api_listar_subcategoria():
    dictRespuesta = {}
    try:
        id_subcategoria = request.json["id"]

        subcategoria_data = controlador_subcategorias.obtener_subcategoria_por_id(id_subcategoria)

        if subcategoria_data:
            subcategoria = clsSubcategoria(
                p_id=subcategoria_data[0],
                p_subcategoria=subcategoria_data[1],
                p_faicon_subcat=subcategoria_data[2],
                p_disponibilidad=subcategoria_data[3],
                p_CATEGORIAid=subcategoria_data[4]
            )

            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Subcategoría obtenida con éxito"
            dictRespuesta["data"] = {
                "id": subcategoria.id,
                "subcategoria": subcategoria.subcategoria,
                "faicon_subcat": subcategoria.faicon_subcat,
                "disponibilidad": subcategoria.disponibilidad,
                "categoriaid": subcategoria.CATEGORIAid
            }
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Subcategoría no encontrada"
            dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la subcategoría: {str(e)}"
        dictRespuesta["data"] = {}
        return jsonify(dictRespuesta)


###################APIs CATEGORIA###############
@app.route("/api_guardar_categoria", methods=["POST"])
# @jwt_required()  # Descomentar si necesitas autenticación
def api_guardar_categoria():
    dictRespuesta = {}
    try:
        categoria = request.json["categoria"]
        faicon_cat = request.json["faicon_cat"]
        disponibilidad = request.json["disponibilidad"]
        
        categoria_obj = clsCategoria(None, categoria, faicon_cat, disponibilidad)

        id_categoria = controlador_categorias.insertar_categoria_api(
            categoria_obj.categoria, categoria_obj.faicon_cat, categoria_obj.disponibilidad
        )

        categoria_obj.id = id_categoria

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Categoría guardada con éxito"
        dictRespuesta["data"] = {"id": categoria_obj.id, "categoria": categoria_obj.categoria}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al guardar la categoría: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_listado_categorias")
# @jwt_required()
def api_listado_categorias():
    dictRespuesta = {}
    try:
        categorias = controlador_categorias.obtener_listado_categorias()

        categorias_procesadas = []
    
        for categoria in categorias:
            id_categoria = categoria[0]
            nombre_categoria = categoria[1]
            faicon_categoria = categoria[2]
            disponibilidad = categoria[3]
            subcategorias_count = categoria[4]

            categorias_procesadas.append({
                "id": id_categoria,
                "categoria": nombre_categoria,
                "faicon_cat": faicon_categoria,
                "disponibilidad": disponibilidad,
                "subcategorias_count": subcategorias_count
            })

        dictRespuesta["status"] = 1
        dictRespuesta["data"] = categorias_procesadas
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el listado de categorías: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_categoria", methods=["POST"])
# @jwt_required()
def api_eliminar_categoria():
    id_categoria = request.json["id"]
    dictRespuesta = {}
    try:
        controlador_categorias.eliminar_categoria(id_categoria)
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Categoría eliminada con éxito"
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la categoría: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_categoria", methods=["POST"])
# @jwt_required()
def api_actualizar_categoria():
    dictRespuesta = {}
    try:
        id_categoria = request.json["id"]
        categoria_nombre = request.json["categoria"]
        faicon_cat = request.json["faicon_cat"]
        disponibilidad = request.json["disponibilidad"]

        categoria = clsCategoria(
            p_id=id_categoria,
            p_categoria=categoria_nombre,
            p_faicon_cat=faicon_cat,
            p_disponibilidad=disponibilidad
        )

        controlador_categorias.actualizar_categoria(
            categoria.categoria,
            categoria.faicon_cat,
            categoria.disponibilidad,
            categoria.id
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Categoría actualizada con éxito"
        dictRespuesta["id"] = categoria.id
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la categoría: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_categoria", methods=["POST"])
# @jwt_required()  # Si es necesario autenticación, puedes dejarlo habilitado
def api_listar_categoria():
    dictRespuesta = {}
    try:
        # Obtener el id de la categoría desde el cuerpo del JSON
        id_categoria = request.json["id"]
        
        # Llamar a la función para obtener la categoría desde la base de datos
        categoria_data = controlador_categorias.obtener_categoria_por_id(id_categoria)
        
        if categoria_data:
            # Crear una instancia de la clase Categoria usando los datos obtenidos
            categoria = clsCategoria(
                p_id=categoria_data[0],
                p_categoria=categoria_data[1],
                p_faicon_cat=categoria_data[2],
                p_disponibilidad=categoria_data[3]
            )
            
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Categoría encontrada"
            dictRespuesta["data"] = {
                "id": categoria.id,
                "categoria": categoria.categoria,
                "faicon_cat": categoria.faicon_cat,
                "disponibilidad": categoria.disponibilidad
            }
        
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Categoría no encontrada"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la categoría: {str(e)}"
        return jsonify(dictRespuesta)

    
################APIs USUARIOS###########
@app.route("/api_guardar_usuario_cliente", methods=["POST"])
# @jwt_required()  # Descomentar si necesitas autenticación
def api_guardar_usuario():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON recibido
        usuario = request.json["usuario"]
        doc_identidad = request.json["doc_identidad"]
        img_usuario = request.json.get("img_usuario")
        genero = request.json["genero"]
        fecha_nacimiento = request.json["fecha_nacimiento"]
        telefono = request.json["telefono"]
        correo = request.json["correo"]
        contrasenia = request.json["contrasenia"]
        disponibilidad = request.json["disponibilidad"]
        tipo_usuarioid = request.json["tipo_usuarioid"]

        # Crear el objeto Usuario
        usuario_obj = clsUsuario(None, usuario, None, doc_identidad, img_usuario, genero,
                              fecha_nacimiento, telefono, correo, contrasenia, disponibilidad,
                              None, tipo_usuarioid)

        # Llamar al controlador para insertar el usuario
        id_usuario = controlador_usuario_cliente.insertar_usuario_api(
            usuario_obj.nombres, usuario_obj.doc_identidad, usuario_obj.img_usuario,
            usuario_obj.genero, usuario_obj.fecha_nacimiento, usuario_obj.telefono,
            usuario_obj.correo, usuario_obj.contrasenia, usuario_obj.disponibilidad,
            usuario_obj.TIPO_USUARIOid
        )

        # Asignar el id generado al objeto
        usuario_obj.id = id_usuario

        # Devolver respuesta con el ID del usuario insertado
        if usuario_obj.id == 0:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Correo ya registrado, mejor recupera contraseña"
            dictRespuesta["data"] = {}
        else:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Usuario registrado con éxito"
            dictRespuesta["data"] = {"id": usuario_obj.id, "usuario": usuario_obj.nombres}
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al registrar el usuario: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_listado_usuarios_clientes")
# @jwt_required()
def api_listado_usuarios_clientes():
    dictRespuesta = {}
    try:
        usuarios = controlador_usuario_cliente.obtener_listado_usuarios_clientes()

        usuarios_procesados = []
        
        for usuario in usuarios:
            id_usuario = usuario[0]
            nombres = usuario[1]
            apellidos = usuario[2]
            doc_identidad = usuario[3]
            img_usuario_binario = usuario[4]
            genero = usuario[5]
            fecha_nacimiento = usuario[6]
            telefono = usuario[7]
            correo = usuario[8]
            disponibilidad = usuario[9]
            cantidad_pedidos = usuario[10]
            fecha_registro = usuario[11]
            cantidad_comentarios = usuario[12]

            if img_usuario_binario:
                img_usuario_base64 = base64.b64encode(img_usuario_binario).decode('utf-8')
                img_usuario_formato = f"data:image/png;base64,{img_usuario_base64}"
            else:
                img_usuario_formato = None

            fecha_nacimiento_formateada = None
            if isinstance(fecha_nacimiento, datetime):
                try:
                    fecha_nacimiento_formateada = fecha_nacimiento.strftime('%Y-%m-%d')
                except Exception:
                    fecha_nacimiento_formateada = None

            fecha_registro_formateada = None
            if isinstance(fecha_registro, datetime):
                try:
                    fecha_registro_formateada = fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    fecha_registro_formateada = None

            usuarios_procesados.append({
                "id": id_usuario,
                "nombres": nombres,
                "apellidos": apellidos,
                "doc_identidad": doc_identidad,
                "img_usuario": img_usuario_formato,
                "genero": genero,
                "fecha_nacimiento": fecha_nacimiento_formateada,
                "telefono": telefono,
                "correo": correo,
                "disponibilidad": disponibilidad,
                "cantidad_pedidos": cantidad_pedidos,
                "fecha_registro": fecha_registro_formateada,
                "cantidad_comentarios": cantidad_comentarios
            })

        dictRespuesta["status"] = 1
        dictRespuesta["data"] = usuarios_procesados
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el listado de usuarios: {str(e)}"
        return jsonify(dictRespuesta)



@app.route("/api_eliminar_usuario", methods=["POST"])
# @jwt_required()
def api_eliminar_usuario():
    id_usuario = request.json["id"]
    dictRespuesta = {}
    try:
        controlador_usuario_cliente.eliminar_usuario_cliente(id_usuario)
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Usuario eliminado con éxito"
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el usuario: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_usuario", methods=["POST"])
# @jwt_required()
def api_actualizar_usuario():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON recibido
        id_usuario = request.json["id"]
        nombres = request.json["usuario"]  # El campo "usuario" corresponde a los nombres
        apellidos = request.json.get("apellidos", "")  # Apellidos es opcional
        doc_identidad = request.json["doc_identidad"]
        img_usuario = request.json.get("img_usuario")  # Es opcional
        genero = request.json["genero"]
        fecha_nacimiento = request.json["fecha_nacimiento"]
        telefono = request.json["telefono"]
        correo = request.json["correo"]
        disponibilidad = request.json["disponibilidad"]

        # Crear el objeto Usuario
        usuario_obj = clsUsuario(id_usuario, nombres, apellidos, doc_identidad, img_usuario, genero,
                              fecha_nacimiento, telefono, correo, None, disponibilidad,
                              None, 3)  # TIPO_USUARIOid está fijo en 3 para clientes

        # Llamar al controlador para actualizar el usuario cliente
        if controlador_usuario_cliente.actualizar_usuario_cliente(
            usuario_obj.id, usuario_obj.nombres, usuario_obj.apellidos, usuario_obj.doc_identidad,
            usuario_obj.genero, usuario_obj.fecha_nacimiento, usuario_obj.telefono, usuario_obj.correo,
            usuario_obj.disponibilidad, usuario_obj.img_usuario
        ):
            # Devolver respuesta con mensaje de éxito
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Usuario actualizado con éxito"
            dictRespuesta["data"] = {"id": usuario_obj.id, "usuario": usuario_obj.nombres}
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Error al actualizar el usuario"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el usuario: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_obtener_usuario_cliente", methods=["POST"])
# @jwt_required()
def api_obtener_usuario_cliente():
    dictRespuesta = {}
    try:
        # Obtener el ID del usuario desde el cuerpo de la solicitud
        id_usuario = request.json.get("id")

        # Verificar que se haya proporcionado el ID
        if not id_usuario:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        # Llamar al controlador para obtener los datos del usuario
        usuario_data = controlador_usuario_cliente.obtener_usuario_cliente_por_id(id_usuario)

        if usuario_data:
            # Crear un objeto de usuario sin la imagen
            usuario_obj = {
                "id": usuario_data[0],
                "nombres": usuario_data[1],
                "apellidos": usuario_data[2],
                "doc_identidad": usuario_data[3],
                "genero": usuario_data[5],
                "fecha_nacimiento": usuario_data[6],
                "telefono": usuario_data[7],
                "correo": usuario_data[8],
                "disponibilidad": usuario_data[10],
                "tipo_usuarioid": usuario_data[11]

            }

            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Usuario obtenido con éxito"
            dictRespuesta["data"] = usuario_obj

        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Usuario no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el usuario: {str(e)}"
        return jsonify(dictRespuesta)

###########################COMENTARIOS###############################
@app.route("/api_guardar_comentario", methods=["POST"])
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_guardar_comentario():
    nombres = request.json["nombres"]
    apellidos = request.json["apellidos"]
    email = request.json["email"]
    celular = request.json["celular"]
    mensaje = request.json["mensaje"]
    estado = request.json["estado"]
    motivo_comentarioid = request.json["motivo_comentarioid"]
    usuarioid = request.json.get("usuarioid")  # Opcional
    
    dictRespuesta = {}
    
    # Crear objeto Comentario
    comentario = clsComentario(
        p_id=None,  # El ID es auto-incremental, no lo pasamos
        p_nombres=nombres,
        p_apellidos=apellidos,
        p_email=email,
        p_celular=celular,
        p_mensaje=mensaje,
        p_fecha_registro=None,  # Lo establecerá la base de datos (timestamp)
        p_estado=estado,
        p_MOTIVO_COMENTARIOid=motivo_comentarioid,
        p_USUARIOid=usuarioid
    )
    
    try:
        # Extraer los atributos directamente del objeto Comentario y pasarlos a la función de inserción
        controlador_comentario.insertar_comentario(
            comentario.nombres,
            comentario.apellidos,
            comentario.email,
            comentario.celular,
            comentario.mensaje,
            comentario.estado,
            comentario.MOTIVO_COMENTARIOid,
            comentario.USUARIOid
        )
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Comentario registrado con éxito"
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al registrar el comentario: {str(e)}"
        return jsonify(dictRespuesta)

    

@app.route("/api_listado_comentarios")
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_listado_comentarios():
    dictRespuesta = {}
    
    try:
        comentarios = controlador_comentario.obtener_listado_comentarios()  
        comentarios_procesados = []
        
        for comentario in comentarios:
            id_comentario = comentario[0]
            nombres = comentario[1]
            apellidos = comentario[2]
            email = comentario[3]
            celular = comentario[4]
            mensaje = comentario[5]
            fecha_registro = comentario[6]
            estado = comentario[7]
            motivo = comentario[8]
            motivo_id = comentario[9]
            disponibilidad = comentario[10]
            usuarioid = comentario[11]

            # Formatear la fecha si es un objeto datetime
            if isinstance(fecha_registro, datetime):
                fecha_registro_formateada = fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
            else:
                fecha_registro_formateada = None  # O manejar el caso si no es datetime

            comentarios_procesados.append({
                "id": id_comentario,
                "nombres": nombres,
                "apellidos": apellidos,
                "email": email,
                "celular": celular,
                "mensaje": mensaje,
                "fecha_registro": fecha_registro,  # Usamos la fecha formateada
                "estado": estado,
                "motivo": motivo,
                "motivo_id": motivo_id,
                "disponibilidad": disponibilidad,
                "usuarioid": usuarioid
            })
        
        dictRespuesta["status"] = 1
        dictRespuesta["data"] = comentarios_procesados
        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el listado de comentarios: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_eliminar_comentario", methods=["POST"])
# @jwt_required()
def api_eliminar_comentario():
    id_comentario = request.json["id"]
    dictRespuesta = {}
    try:
        controlador_comentario.eliminar_comentario(id_comentario)
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Comentario eliminado con éxito"
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el comentario: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_comentario", methods=["POST"])
# @jwt_required()
def api_actualizar_comentario():
    id_comentario = request.json["id"]
    nombres = request.json["nombres"]
    apellidos = request.json["apellidos"]
    email = request.json["email"]
    celular = request.json["celular"]
    mensaje = request.json["mensaje"]
    estado = request.json["estado"]
    motivo_comentarioid = request.json["motivo_comentarioid"]
    usuarioid = request.json.get("usuarioid")  # Opcional
    
    dictRespuesta = {}
    
    # Crear objeto Comentario con los nuevos datos
    comentario = clsComentario(
        p_id=id_comentario,
        p_nombres=nombres,
        p_apellidos=apellidos,
        p_email=email,
        p_celular=celular,
        p_mensaje=mensaje,
        p_fecha_registro=None,  # No necesitamos pasar la fecha aquí, la base de datos lo hace automáticamente
        p_estado=estado,
        p_MOTIVO_COMENTARIOid=motivo_comentarioid,
        p_USUARIOid=usuarioid
    )
    
    try:
        # Extraer los atributos directamente del objeto Comentario y pasarlos a la función de actualización
        controlador_comentario.actualizar_comentario(
            comentario.id,            # Usamos el id del comentario para actualizar
            comentario.nombres,
            comentario.apellidos,
            comentario.email,
            comentario.celular,
            comentario.mensaje,
            comentario.estado,
            comentario.MOTIVO_COMENTARIOid,
            comentario.USUARIOid
        )
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Comentario actualizado con éxito"
        return jsonify(dictRespuesta)
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el comentario: {str(e)}"
        return jsonify(dictRespuesta)




############################FIN COMENTARIOS####################################UUUUUUUUUUU

############################APIS PEDIDO#############################
@app.route("/api_guardar_pedido", methods=["POST"])
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_guardar_pedido():
    # Obtener los datos desde la solicitud
    fecha_compra = request.json["fecha_compra"]
    subtotal = request.json["subtotal"]
    metodo_pagoid = request.json["metodo_pagoid"]
    usuarioid = request.json["usuarioid"]
    estado_pedidoid = request.json["estado_pedidoid"]
    
    dictRespuesta = {}

    try:
        # Crear objeto Pedido
        pedido = clsPedido(
            p_id=None,  # El ID es auto-incremental, no lo pasamos
            p_fecha_compra=fecha_compra,
            p_subtotal=subtotal,
            p_METODO_PAGOid=metodo_pagoid,
            p_USUARIOid=usuarioid,
            p_ESTADO_PEDIDOid=estado_pedidoid
        )
        
        # Llamar al método del controlador para insertar el pedido
        pedido_id = controlador_carrito.insertar_pedido(
            pedido.USUARIOid,
            pedido.ESTADO_PEDIDOid
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Pedido registrado con éxito"
        dictRespuesta["data"] = {"id": pedido_id, "fecha_compra": pedido.fecha_compra}

        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al registrar el pedido: {str(e)}"
        dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)

@app.route("/api_actualizar_pedido", methods=["POST"])
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_actualizar_pedido():
    # Obtener los datos desde la solicitud
    id_pedido = request.json["id"]
    fecha_compra = request.json["fecha_compra"]
    subtotal = request.json["subtotal"]
    metodo_pagoid = request.json["metodo_pagoid"]
    usuarioid = request.json["usuarioid"]
    estado_pedidoid = request.json["estado_pedidoid"]
    
    dictRespuesta = {}

    try:
        # Crear objeto Pedido con los nuevos valores
        pedido = clsPedido(
            p_id=id_pedido,
            p_fecha_compra=fecha_compra,
            p_subtotal=subtotal,
            p_METODO_PAGOid=metodo_pagoid,
            p_USUARIOid=usuarioid,
            p_ESTADO_PEDIDOid=estado_pedidoid
        )
        
        # Llamar al método del controlador para actualizar el pedido
        controlador_pedido.actualizarPedido(
            pedido.id,
            pedido.fecha_compra,
            pedido.subtotal,
            pedido.METODO_PAGOid,
            pedido.USUARIOid,
            pedido.ESTADO_PEDIDOid
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Pedido actualizado con éxito"
        dictRespuesta["data"] = {"id": pedido.id, "fecha_compra": pedido.fecha_compra}

        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el pedido: {str(e)}"
        dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)


@app.route("/api_eliminar_pedido", methods=["POST"])
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_eliminar_pedido():
    # Obtener el id del pedido desde la solicitud
    id_pedido = request.json["id"]
    
    dictRespuesta = {}

    try:
        # Llamar al método del controlador para eliminar el pedido
        controlador_pedido.eliminar_pedido(id_pedido)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Pedido eliminado con éxito"
        dictRespuesta["data"] = {"id": id_pedido}

        return jsonify(dictRespuesta)
    
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el pedido: {str(e)}"
        dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)

@app.route("/api_listar_pedidos", methods=["GET"])
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_listar_pedidos():
    dictRespuesta = {}

    try:
        # Obtener los pedidos desde el controlador
        pedidos = controlador_pedido.obtener_listado_pedidos()

        # Convertir los pedidos a una lista de diccionarios (si es necesario)
        pedidos_data = [
            {
                "id": pedido[0],
                "fecha_compra": pedido[1],
                "subtotal": pedido[2],
                "METODO_PAGOid": pedido[3],
                "nombre_usuario": pedido[4],
                "ESTADO_PEDIDOid": pedido[5],
                "cantidad_productos": pedido[6],
                "metodo_pago_disponibilidad": pedido[7],
                "usuarioid": pedido[8]
            }
            for pedido in pedidos
        ]

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Pedidos obtenidos con éxito"
        dictRespuesta["data"] = pedidos_data

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los pedidos: {str(e)}"
        dictRespuesta["data"] = []

        return jsonify(dictRespuesta)

@app.route("/api_listar_pedido", methods=["POST"])
# @jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
def api_listar_pedido():
    dictRespuesta = {}

    try:
        # Obtener el ID del pedido desde el JSON
        pedido_id = request.json.get("id")

        if not pedido_id:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "ID de pedido no proporcionado"
            dictRespuesta["data"] = {}
            return jsonify(dictRespuesta)

        # Obtener el pedido desde el controlador por ID
        pedido = controlador_pedido.obtener_pedido_id(pedido_id)

        # Si no se encuentra el pedido, devolver mensaje de error
        if not pedido:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Pedido no encontrado"
            dictRespuesta["data"] = {}
            return jsonify(dictRespuesta)

        # Convertir el pedido a un diccionario
        pedido_data = {
            "id": pedido[0],
            "fecha_compra": pedido[1],
            "subtotal": pedido[2],
            "METODO_PAGOid": pedido[3],
            "nombre_usuario": pedido[4],
            "ESTADO_PEDIDOid": pedido[5],
            "cantidad_productos": pedido[6],
            "metodo_pago_disponibilidad": pedido[7],
            "usuarioid": pedido[8]
        }

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Pedido obtenido con éxito"
        dictRespuesta["data"] = pedido_data

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el pedido: {str(e)}"
        dictRespuesta["data"] = {}

        return jsonify(dictRespuesta)

############################FIN PEDIDOS########################

##################3APIS DETALLE#############3
@app.route("/api_obtener_detalles_por_usuario", methods=["POST"])
# @jwt_required()
def api_obtener_detalles_por_usuario():
    dictRespuesta = {}
    try:
        # Obtener el ID del usuario desde el cuerpo de la solicitud
        id_usuario = request.json.get("id")

        if not id_usuario:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        # Obtener los detalles del pedido para el usuario
        detalles = controlador_detalle.obtener_Detalle(id_usuario)

        if detalles:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Detalles obtenidos con éxito"
            dictRespuesta["data"] = detalles
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "No se encontraron detalles"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los detalles: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_obtener_detalles_por_pedido", methods=["POST"])
# @jwt_required()
def api_obtener_detalles_por_pedido():
    dictRespuesta = {}
    try:
        # Obtener el ID del pedido desde el cuerpo de la solicitud
        id_pedido = request.json.get("id")

        if not id_pedido:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        # Obtener los detalles del pedido
        detalles = controlador_detalle.obtener_Detalle_por_Id_pedido(id_pedido)

        if detalles:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Detalles obtenidos con éxito"
            dictRespuesta["data"] = detalles
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "No se encontraron detalles"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los detalles: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_detalle", methods=["POST"])
# @jwt_required()
def api_eliminar_detalle():
    dictRespuesta = {}
    try:
        # Obtener los parámetros desde el cuerpo de la solicitud
        producto_id = request.json.get("producto_id")
        pedido_id = request.json.get("pedido_id")

        if not producto_id or not pedido_id:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Los campos 'producto_id' y 'pedido_id' son obligatorios"
            return jsonify(dictRespuesta)

        # Eliminar el detalle del pedido
        controlador_detalle.eliminar_detalle(producto_id, pedido_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Detalle eliminado correctamente"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar detalle: {str(e)}"
        return jsonify(dictRespuesta)
    
@app.route("/api_editar_detalle", methods=["POST"])
@jwt_required()
def api_editar_detalle():
    dictRespuesta = {}
    try:
        # Obtener los parámetros desde el cuerpo de la solicitud
        producto_id = request.json.get("producto_id")
        pedido_id = request.json.get("pedido_id")
        nueva_cantidad = request.json.get("nueva_cantidad")

        if not producto_id or not pedido_id or not nueva_cantidad:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Los campos 'producto_id', 'pedido_id' y 'nueva_cantidad' son obligatorios"
            return jsonify(dictRespuesta)

        # Editar la cantidad del detalle
        controlador_detalle.editar_detalle(producto_id, pedido_id, nueva_cantidad)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Detalle actualizado correctamente"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al editar detalle: {str(e)}"
        return jsonify(dictRespuesta)


@app.route('/api_guardar_detalle', methods=['POST'])
def api_guardar_detalle():
    try:
        # Recibimos los datos desde el JSON de la petición
        data = request.get_json()
        producto_id = data['producto_id']
        pedido_id = data['pedido_id']
        cantidad = data['cantidad']

        # Llamamos a la función para guardar el detalle
        controlador_detalle.guardar_detalle(producto_id, pedido_id, cantidad)

        # Retornamos una respuesta de éxito
        return jsonify({"message": "Detalle guardado correctamente"}), 200
    except Exception as e:
        # Retornamos una respuesta de error
        return jsonify({"message": f"Error al guardar detalle: {e}"}), 400

##################APIS MOTIVO_COMENTARIO###############33
@app.route("/api_guardar_motivo", methods=["POST"])
# @jwt_required()
def api_guardar_motivo():
    dictRespuesta = {}
    try:
        motivo = request.json["motivo"]
        disponibilidad = request.json["disponibilidad"]

        motivo_obj = clsMotivoComentario(None, motivo, disponibilidad)

        controlador_motivo_comentario.insertar_motivo(motivo_obj.motivo, motivo_obj.disponibilidad)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Motivo guardado con éxito"
        dictRespuesta["data"] = {"motivo": motivo_obj.motivo, "disponibilidad": motivo_obj.disponibilidad}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al guardar el motivo: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_motivo", methods=["POST"])
# @jwt_required()
def api_eliminar_motivo():
    dictRespuesta = {}
    try:
        id_motivo = request.json["id"]

        if not id_motivo:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        controlador_motivo_comentario.eliminar_motivo(id_motivo)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Motivo eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el motivo: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_motivos", methods=["GET"])
# @jwt_required()
def api_listar_motivos():
    dictRespuesta = {}
    try:
        motivos = controlador_motivo_comentario.obtener_listado_motivos()
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Motivos obtenidos con éxito"
        dictRespuesta["data"] = []

        for motivo in motivos:
            motivo_data = {
                "id": motivo[0],
                "motivo": motivo[1],
                "disponibilidad": motivo[2],
                "comentarios_count": motivo[3]
            }
            dictRespuesta["data"].append(motivo_data)

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los motivos: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_motivo_por_id", methods=["POST"])
# @jwt_required()
def api_listar_motivo_por_id():
    dictRespuesta = {}
    try:
        id_motivo = request.json["id"]

        if not id_motivo:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        motivo_data = controlador_motivo_comentario.obtener_motivo_por_id(id_motivo)

        if motivo_data:
            motivo_obj = clsMotivoComentario(motivo_data[0], motivo_data[1], motivo_data[2])
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Motivo obtenido con éxito"
            dictRespuesta["data"] = {
                "id": motivo_obj.id,
                "motivo": motivo_obj.motivo,
                "disponibilidad": motivo_obj.disponibilidad
            }
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Motivo no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el motivo: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_motivo", methods=["POST"])
# @jwt_required()
def api_actualizar_motivo():
    dictRespuesta = {}
    try:
        id_motivo = request.json["id"]
        motivo = request.json["motivo"]
        disponibilidad = request.json["disponibilidad"]

        motivo_obj = clsMotivoComentario(id_motivo, motivo, disponibilidad)

        controlador_motivo_comentario.actualizar_motivo(motivo_obj.motivo, motivo_obj.disponibilidad, motivo_obj.id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Motivo actualizado con éxito"
        dictRespuesta["data"] = {"id": motivo_obj.id, "motivo": motivo_obj.motivo, "disponibilidad": motivo_obj.disponibilidad}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el motivo: {str(e)}"
        return jsonify(dictRespuesta)
##############3FIN APIS TIPO MOTIVO COMENTARIO#############

###############APIS TIPO NOVEDAD############
@app.route("/api_guardar_tipo_novedad", methods=["POST"])
# @jwt_required()
def api_guardar_tipo_novedad():
    dictRespuesta = {}
    try:
        # Recibir datos del tipo de novedad desde el JSON de la petición
        nombre_tipo = request.json["nomTipo"]

        # Crear una instancia de TipoNovedad
        tipo_novedad_obj = clsTipoNovedad(None, nombre_tipo, 1)

        controlador_tipos_novedad.insertar_tipo_novedad(tipo_novedad_obj.nomTipo)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de novedad guardado con éxito"
        dictRespuesta["data"] = {"nomTipo": tipo_novedad_obj.nomTipo}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al guardar el tipo de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_tipo_novedad", methods=["POST"])
# @jwt_required()
def api_eliminar_tipo_novedad():
    dictRespuesta = {}
    try:
        # Recibir el ID del tipo de novedad desde el JSON de la petición
        id_tipo_novedad = request.json["id"]

        if not id_tipo_novedad:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        # Eliminar el tipo de novedad
        controlador_tipos_novedad.eliminar_tipo_novedad(id_tipo_novedad)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de novedad eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el tipo de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_tipos_novedad", methods=["GET"])
# @jwt_required()
def api_listar_tipos_novedad():
    dictRespuesta = {}
    try:
        # Obtener todos los tipos de novedad
        tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipos de novedad obtenidos con éxito"
        dictRespuesta["data"] = []

        for tipo in tipos_novedad:
            tipo_data = {
                "id": tipo[0],
                "nomTipo": tipo[1],
                "disponibilidad": tipo[2]
            }
            dictRespuesta["data"].append(tipo_data)

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los tipos de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_tipo_novedad_por_id", methods=["POST"])
# @jwt_required()
def api_listar_tipo_novedad_por_id():
    dictRespuesta = {}
    try:
        # Recibir el ID del tipo de novedad desde el JSON de la petición
        id_tipo_novedad = request.json["id"]

        if not id_tipo_novedad:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        # Obtener el tipo de novedad por ID
        tipo_novedad_data = controlador_tipos_novedad.obtener_tipo_novedad_por_id(id_tipo_novedad)

        if tipo_novedad_data:
            tipo_novedad_obj = clsTipoNovedad(tipo_novedad_data[0], tipo_novedad_data[1], tipo_novedad_data[2])
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Tipo de novedad obtenido con éxito"
            dictRespuesta["data"] = {
                "id": tipo_novedad_obj.id,
                "nomTipo": tipo_novedad_obj.nomTipo,
                "disponibilidad": tipo_novedad_obj.disponibilidad
            }
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Tipo de novedad no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el tipo de novedad: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_actualizar_tipo_novedad", methods=["POST"])
# @jwt_required()
def api_actualizar_tipo_novedad():
    dictRespuesta = {}
    try:
        # Recibir datos del tipo de novedad desde el JSON de la petición
        id_tipo_novedad = request.json["id"]
        nombre_tipo = request.json["nomTipo"]
        disponibilidad = request.json["disponibilidad"]

        # Crear una instancia de TipoNovedad
        tipo_novedad_obj = clsTipoNovedad(id_tipo_novedad, nombre_tipo, disponibilidad)

        # Actualizar el tipo de novedad en la base de datos
        controlador_tipos_novedad.actualizar_tipo_novedad(tipo_novedad_obj.nomTipo, tipo_novedad_obj.disponibilidad, tipo_novedad_obj.id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de novedad actualizado con éxito"
        dictRespuesta["data"] = {"id": tipo_novedad_obj.id, "nomTipo": tipo_novedad_obj.nomTipo, "disponibilidad": tipo_novedad_obj.disponibilidad}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el tipo de novedad: {str(e)}"
        return jsonify(dictRespuesta)

##############################################################################

#######################APIS NOVEDAD################
@app.route("/api_guardar_novedad", methods=["POST"])
# @jwt_required()
def api_guardar_novedad():
    dictRespuesta = {}
    try:
        # Recibir datos de la novedad desde el JSON de la petición
        nombre = request.json["nombre"]
        titulo = request.json["titulo"]
        fecha_inicio = request.json["fecha_inicio"]
        fecha_vencimiento = request.json["fecha_vencimiento"]
        terminos = request.json["terminos"]
        marca_id = request.json["marcaId"]
        subcategoria_id = request.json["subcategoriaId"]
        tipo_novedad_id = request.json["tipoNovedadId"]

        # Crear una instancia de Novedad
        novedad_obj = clsNovedad(None, nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, None, 1, marca_id, subcategoria_id, tipo_novedad_id)

        # Insertar la novedad en la base de datos
        novedad_id = controlador_novedades.insertarNovedad(novedad_obj.nombre, novedad_obj.titulo, novedad_obj.fecha_inicio,
                                                        novedad_obj.fecha_vencimiento, novedad_obj.terminos, novedad_obj.MARCAid,
                                                        novedad_obj.SUBCATEGORIAid, novedad_obj.TIPO_NOVEDADid)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Novedad guardada con éxito"
        dictRespuesta["data"] = {"id": novedad_id, "nombre": novedad_obj.nombre, "titulo": novedad_obj.titulo}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al guardar la novedad: {str(e)}"
        return jsonify(dictRespuesta)
    
@app.route("/api_eliminar_novedad", methods=["POST"])
# @jwt_required()
def api_eliminar_novedad():
    dictRespuesta = {}
    try:
        # Recibir el ID de la novedad desde el JSON de la petición
        novedad_id = request.json["id"]

        if not novedad_id:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        # Eliminar la novedad
        controlador_novedades.eliminarNovedad(novedad_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Novedad eliminada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_novedades", methods=["GET"])
# @jwt_required()
def api_listar_novedades():
    dictRespuesta = {}
    try:
        # Obtener todas las novedades
        novedades = controlador_novedades.obtener_listado_novedades()

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Novedades obtenidas con éxito"
        dictRespuesta["data"] = []

        for novedad in novedades:
            novedad_data = {
                "id": novedad[0],
                "nombre": novedad[1],
                "titulo": novedad[2],
                "fecha_inicio": novedad[3],
                "fecha_vencimiento": novedad[4],
                "terminos": novedad[5],
                "fecha_registro": novedad[6],
                "disponibilidad": novedad[7],
                "marcaId": novedad[8],
                "subcategoriaId": novedad[9],
                "tipoNovedadId": novedad[10]
            }
            dictRespuesta["data"].append(novedad_data)

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener las novedades: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_listar_novedad_por_id", methods=["POST"])
# @jwt_required()
def api_listar_novedad_por_id():
    dictRespuesta = {}
    try:
        # Recibir el ID de la novedad desde el JSON de la petición
        novedad_id = request.json["id"]

        if not novedad_id:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "El campo 'id' es obligatorio"
            return jsonify(dictRespuesta)

        novedad_data = controlador_novedades.obtenerNovedadPorId(novedad_id)

        if novedad_data:
            novedad_obj = clsNovedad(novedad_data[0], novedad_data[1], novedad_data[2], novedad_data[3],
                                  novedad_data[4], novedad_data[5], None, novedad_data[6], novedad_data[7], novedad_data[8],
                                  novedad_data[9])
            
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Novedad obtenida con éxito"
            dictRespuesta["data"] = {
                "id": novedad_obj.id,
                "nombre": novedad_obj.nombre,
                "titulo": novedad_obj.titulo,
                "fecha_inicio": novedad_obj.fecha_inicio,
                "fecha_vencimiento": novedad_obj.fecha_vencimiento,
                "terminos": novedad_obj.terminos,
                "fecha_registro": novedad_obj.fecha_registro,
                "disponibilidad": novedad_obj.disponibilidad,
                "marcaId": novedad_obj.MARCAid,
                "subcategoriaId": novedad_obj.SUBCATEGORIAid,
                "tipoNovedadId": novedad_obj.TIPO_NOVEDADid
            }
        else:
            dictRespuesta["status"] = -1
            dictRespuesta["mensaje"] = "Novedad no encontrada"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_novedad", methods=["POST"])
# @jwt_required()
def api_actualizar_novedad():
    dictRespuesta = {}
    try:
        # Recibir datos de la novedad desde el JSON de la petición
        novedad_id = request.json["id"]
        nombre = request.json["nombre"]
        titulo = request.json["titulo"]
        fecha_inicio = request.json["fecha_inicio"]
        fecha_vencimiento = request.json["fecha_vencimiento"]
        terminos = request.json["terminos"]
        disponibilidad = request.json["disponibilidad"]
        marca_id = request.json["marcaId"]
        subcategoria_id = request.json["subcategoriaId"]
        tipo_novedad_id = request.json["tipoNovedadId"]

        # Crear una instancia de Novedad
        novedad_obj = clsNovedad(novedad_id, nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, None, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id)

        # Actualizar la novedad en la base de datos
        controlador_novedades.actualizarNovedad(novedad_obj.nombre, novedad_obj.titulo, novedad_obj.fecha_inicio,
                                              novedad_obj.fecha_vencimiento, novedad_obj.terminos, novedad_obj.disponibilidad,
                                              novedad_obj.MARCAid, novedad_obj.SUBCATEGORIAid, novedad_obj.TIPO_NOVEDADid, None, novedad_obj.id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Novedad actualizada con éxito"
        dictRespuesta["data"] = {"id": novedad_obj.id, "nombre": novedad_obj.nombre, "titulo": novedad_obj.titulo}

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la novedad: {str(e)}"
        return jsonify(dictRespuesta)

###################FIN APIS NOVEDAD#####################

########################APIS CARACTERISTICA PRODUCTOS#############
@app.route("/api_insertar_caracteristica_producto", methods=["POST"])
# @jwt_required()
def api_insertar_caracteristica_producto():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON de la petición
        caracteristica_id = request.json["caracteristicaId"]
        producto_id = request.json["productoId"]
        valor = request.json["valor"]
        principal = request.json["principal"]

        # Crear objeto CaracteristicasProducto
        caracteristica_producto = clsCaracteristicaProducto(caracteristica_id, producto_id, valor, principal)

        # Llamar a la función para insertar la característica en la base de datos
        controlador_caracteristicas_productos.insertar_caracteristica_producto(caracteristica_producto)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica de producto insertada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar la característica: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_obtener_caracteristicas_producto", methods=["POST"])
# @jwt_required()
def api_obtener_caracteristicas_producto():
    dictRespuesta = {}
    try:
        # Obtener el ID del producto desde la petición
        producto_id = request.json["id"]

        # Obtener las características del producto desde la base de datos
        caracteristicas = controlador_caracteristicas_productos.obtener_caracteristicas_producto(producto_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Características obtenidas con éxito"
        dictRespuesta["data"] = caracteristicas
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener las características: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_actualizar_caracteristica_producto", methods=["POST"])
# @jwt_required()
def api_actualizar_caracteristica_producto():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON de la petición
        caracteristica_id = request.json["caracteristicaId"]
        producto_id = request.json["productoId"]
        valor = request.json["valor"]
        principal = request.json["principal"]

        # Crear objeto CaracteristicasProducto
        caracteristica_producto = clsCaracteristicaProducto(caracteristica_id, producto_id, valor, principal)

        # Llamar a la función para actualizar la característica en la base de datos
        controlador_caracteristicas_productos.actualizar_caracteristica_producto(caracteristica_producto)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica de producto actualizada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la característica: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_caracteristica_producto", methods=["POST"])
# @jwt_required()
def api_eliminar_caracteristica_producto():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON de la petición
        caracteristica_id = request.json["caracteristicaId"]
        producto_id = request.json["productoId"]

        # Llamar a la función para eliminar la característica en la base de datos
        controlador_caracteristicas_productos.eliminar_caracteristica_producto(caracteristica_id, producto_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica de producto eliminada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la característica: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_obtener_caracteristica_producto", methods=["POST"])
# @jwt_required()
def api_obtener_caracteristica_producto():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON de la petición
        caracteristica_id = request.json["caracteristicaId"]
        producto_id = request.json["productoId"]

        # Obtener la característica del producto por ID
        caracteristica = controlador_caracteristicas_productos.obtener_caracteristica_producto(caracteristica_id, producto_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica obtenida con éxito"
        dictRespuesta["data"] = caracteristica
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la característica: {str(e)}"
        return jsonify(dictRespuesta)

#######################APIS METODO PAGO###################
@app.route("/api_insertar_metodo_pago", methods=["POST"])
# @jwt_required()
def api_insertar_metodo_pago():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON de la petición
        nombre = request.json["nombre"]

        # Crear objeto MetodoPago
        metodo_pago = clsMetodoPago(None, nombre, 1)

        # Llamar a la función para insertar el método de pago en la base de datos
        controlador_metodo_pago.insertar_metodo_pago(metodo_pago.metodo)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Método de pago insertado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar el método de pago: {str(e)}"
        return jsonify(dictRespuesta)
    
@app.route("/api_obtener_metodos_pago", methods=["GET"])
# @jwt_required()
def api_obtener_metodos_pago():
    dictRespuesta = {}
    try:
        # Obtener los métodos de pago desde la base de datos
        metodos_pago = controlador_metodo_pago.obtener_metodo_pago()

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Métodos de pago obtenidos con éxito"
        dictRespuesta["data"] = metodos_pago
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los métodos de pago: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_obtener_listado_metodos_pago", methods=["GET"])
# @jwt_required()
def api_obtener_listado_metodos_pago():
    dictRespuesta = {}
    try:
        # Obtener el listado de métodos de pago con pedidos asociados
        listado_metodos_pago = controlador_metodo_pago.obtener_listado_metodo_pago()

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Listado de métodos de pago obtenido con éxito"
        dictRespuesta["data"] = listado_metodos_pago
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el listado de métodos de pago: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_actualizar_metodo_pago", methods=["POST"])
# @jwt_required()
def api_actualizar_metodo_pago():
    dictRespuesta = {}
    try:
        # Obtener los datos del JSON de la petición
        metodo_id = request.json["id"]
        nombre = request.json["nombre"]
        disponibilidad = request.json["disponibilidad"]

        # Llamar a la función para actualizar el método de pago en la base de datos
        controlador_metodo_pago.actualizar_metodo_pago_por_id(nombre, disponibilidad, metodo_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Método de pago actualizado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el método de pago: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_eliminar_metodo_pago", methods=["POST"])
# @jwt_required()
def api_eliminar_metodo_pago():
    dictRespuesta = {}
    try:
        # Obtener el ID del método de pago desde la petición
        metodo_id = request.json["id"]

        # Llamar a la función para eliminar el método de pago de la base de datos
        controlador_metodo_pago.eliminar_metodo_pago(metodo_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Método de pago eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el método de pago: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_obtener_metodo_pago", methods=["POST"])
# @jwt_required()
def api_obtener_metodo_pago():
    dictRespuesta = {}
    try:
        # Obtener el ID del cuerpo de la solicitud
        data = request.get_json()
        id = data.get("id")

        if not id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del método de pago"
            return jsonify(dictRespuesta)
        
        # Llamar a la función para obtener el método de pago por ID
        metodo_pago = controlador_metodo_pago.obtener_metodo_pago_por_id(id)

        if metodo_pago:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Método de pago obtenido con éxito"
            dictRespuesta["data"] = metodo_pago
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Método de pago no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el método de pago: {str(e)}"
        return jsonify(dictRespuesta)

###############FIN APIS METODO PAGO##################

####################APIS TIPO IMG  NOVEDAD#######################3
@app.route("/api_obtener_tipos_img_novedad", methods=["GET"])
# @jwt_required()
def api_obtener_tipos_img_novedad():
    dictRespuesta = {}
    try:
        tipos_img = controlador_tipos_img_novedad.obtener_tipos_img_novedad()
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipos de imagen obtenidos con éxito"
        dictRespuesta["data"] = tipos_img
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los tipos de imagen de novedad: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_tipo_img_novedad", methods=["POST"])
# @jwt_required()
def api_obtener_tipo_img_novedad():
    dictRespuesta = {}
    try:
        # Obtener el ID del cuerpo de la solicitud
        data = request.get_json()
        id = data.get("id")

        if not id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del tipo de imagen"
            return jsonify(dictRespuesta)

        # Llamar a la función para obtener el tipo de imagen de novedad por ID
        tipo_img = controlador_tipos_img_novedad.obtener_tipo_img_novedad_por_id(id)

        if tipo_img:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Tipo de imagen de novedad obtenido con éxito"
            dictRespuesta["data"] = tipo_img
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Tipo de imagen de novedad no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el tipo de imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_insertar_tipo_img_novedad", methods=["POST"])
# @jwt_required()
def api_insertar_tipo_img_novedad():
    dictRespuesta = {}
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        tipo = data.get("tipo")
        disponibilidad = data.get("disponibilidad")

        if not tipo or disponibilidad is None:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere tipo y disponibilidad"
            return jsonify(dictRespuesta)

        # Llamar a la función para insertar el tipo de imagen de novedad
        controlador_tipos_img_novedad.insertar_tipo_img_novedad(tipo, disponibilidad)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de imagen de novedad insertado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar el tipo de imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)
    

@app.route("/api_actualizar_tipo_img_novedad", methods=["POST"])
# @jwt_required()
def api_actualizar_tipo_img_novedad():
    dictRespuesta = {}
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        id = data.get("id")
        tipo = data.get("tipo")
        disponibilidad = data.get("disponibilidad")

        if not id or not tipo or disponibilidad is None:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere id, tipo y disponibilidad"
            return jsonify(dictRespuesta)

        # Llamar a la función para actualizar el tipo de imagen de novedad
        controlador_tipos_img_novedad.actualizar_tipo_img_novedad(id, tipo, disponibilidad)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de imagen de novedad actualizado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el tipo de imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_tipo_img_novedad", methods=["POST"])
# @jwt_required()
def api_eliminar_tipo_img_novedad():
    dictRespuesta = {}
    try:
        # Obtener el ID del cuerpo de la solicitud
        data = request.get_json()
        id = data.get("id")

        if not id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del tipo de imagen"
            return jsonify(dictRespuesta)

        # Llamar a la función para eliminar el tipo de imagen de novedad
        controlador_tipos_img_novedad.eliminar_tipo_img_novedad(id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de imagen de novedad eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el tipo de imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

#################FIN APIS TIPO IMG NOVEDAD################3

#####################APIS IMG NOVEDAD#################33
@app.route("/api_obtener_todas_imagenes_novedad", methods=["GET"])
# @jwt_required()
def api_obtener_todas_imagenes_novedad():
    dictRespuesta = {}
    try:
        imagenes = controlador_imagenes_novedades.obtener_todas_imagenes_novedad()
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imágenes de novedades obtenidas con éxito"
        dictRespuesta["data"] = imagenes
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener las imágenes de novedades: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_obtener_imagen_novedad", methods=["POST"])
# @jwt_required()
def api_obtener_imagen_novedad():
    dictRespuesta = {}
    try:
        data = request.get_json()
        img_id = data.get("id")

        if not img_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la imagen"
            return jsonify(dictRespuesta)

        imagen = controlador_imagenes_novedades.obtener_imagen_novedad_por_img_id(img_id)

        if imagen:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Imagen de novedad obtenida con éxito"
            dictRespuesta["data"] = {
                "id": imagen[0],
                "nomImagen": imagen[1],
                "imagen": imagen[2],
                "tipo": imagen[3],
                "novedad_id": imagen[4],
                "tipo_id": imagen[5]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Imagen de novedad no encontrada"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_insertar_imagen_novedad", methods=["POST"])
# @jwt_required()
def api_insertar_imagen_novedad():
    dictRespuesta = {}
    try:
        data = request.get_json()
        nomImagen = data.get("nomImagen")
        imagen = data.get("imagen")  # Imagen en base64
        tipo_img_id = data.get("tipo_img_id")
        novedad_id = data.get("novedad_id")

        if not nomImagen or not imagen or not tipo_img_id or not novedad_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere nomImagen, imagen, tipo_img_id y novedad_id"
            return jsonify(dictRespuesta)

        # Decodificar la imagen desde base64
        imagen_binaria = base64.b64decode(imagen)

        controlador_imagenes_novedades.insertar_imagen_novedad(nomImagen, imagen_binaria, tipo_img_id, novedad_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imagen de novedad insertada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar la imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_imagen_novedad", methods=["POST"])
# @jwt_required()
def api_actualizar_imagen_novedad():
    dictRespuesta = {}
    try:
        data = request.get_json()
        img_id = data.get("id")
        nomImagen = data.get("nomImagen")
        tipo_img_id = data.get("tipo_img_id")
        novedad_id = data.get("novedad_id")

        if not img_id or not nomImagen or not tipo_img_id or not novedad_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere id, nomImagen, tipo_img_id y novedad_id"
            return jsonify(dictRespuesta)

        controlador_imagenes_novedades.actualizar_imagen_novedad(img_id, nomImagen, tipo_img_id, novedad_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imagen de novedad actualizada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_imagen_novedad", methods=["POST"])
# @jwt_required()
def api_eliminar_imagen_novedad():
    dictRespuesta = {}
    try:
        data = request.get_json()
        img_id = data.get("id")

        if not img_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la imagen"
            return jsonify(dictRespuesta)

        controlador_imagenes_novedades.eliminar_imagen_novedad(img_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imagen de novedad eliminada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la imagen de novedad: {str(e)}"
        return jsonify(dictRespuesta)

##################FIN APIS IMG NOVEDAD###############

##########################APIS ESTADO PEDIDO#########
@app.route("/api_obtener_estados_pedido", methods=["GET"])
# @jwt_required()
def api_obtener_estados_pedido():
    dictRespuesta = {}
    try:
        estados = controlador_estado_pedido.obtener_estados_pedido()
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Estados de pedidos obtenidos con éxito"
        dictRespuesta["data"] = estados
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los estados de pedidos: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_obtener_estado_pedido", methods=["POST"])
# @jwt_required()
def api_obtener_estado_pedido():
    dictRespuesta = {}
    try:
        data = request.get_json()
        estado_id = data.get("id")

        if not estado_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del estado del pedido"
            return jsonify(dictRespuesta)

        estado = controlador_estado_pedido.obtener_estado_pedido_por_id(estado_id)

        if estado:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Estado del pedido obtenido con éxito"
            dictRespuesta["data"] = {
                "id": estado[0],
                "nomEstado": estado[1]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Estado del pedido no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el estado del pedido: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_insertar_estado_pedido", methods=["POST"])
# @jwt_required()
def api_insertar_estado_pedido():
    dictRespuesta = {}
    try:
        data = request.get_json()
        nomEstado = data.get("nomEstado")

        if not nomEstado:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere nomEstado"
            return jsonify(dictRespuesta)

        controlador_estado_pedido.insertar_estado_pedido(nomEstado)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Estado del pedido insertado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar el estado del pedido: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_actualizar_estado_pedido", methods=["POST"])
# @jwt_required()
def api_actualizar_estado_pedido():
    dictRespuesta = {}
    try:
        data = request.get_json()
        estado_id = data.get("id")
        nomEstado = data.get("nomEstado")

        if not estado_id or not nomEstado:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere id y nomEstado"
            return jsonify(dictRespuesta)

        controlador_estado_pedido.actualizar_estado_pedido_por_id(nomEstado, estado_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Estado del pedido actualizado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el estado del pedido: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_estado_pedido", methods=["POST"])
# @jwt_required()
def api_eliminar_estado_pedido():
    dictRespuesta = {}
    try:
        data = request.get_json()
        estado_id = data.get("id")

        if not estado_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del estado del pedido"
            return jsonify(dictRespuesta)

        controlador_estado_pedido.eliminar_estado_pedido(estado_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Estado del pedido eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el estado del pedido: {str(e)}"
        return jsonify(dictRespuesta)

########################FIN APIS ESTADO PEDIDO#########

##################APIS TIPO_USUARIO#############
@app.route("/api_obtener_tipos_usuario", methods=["GET"])
# @jwt_required()
def api_obtener_tipos_usuario():
    dictRespuesta = {}
    try:
        tipos_usuario = controlador_tipos_usuario.obtener_tipos_usuario()
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipos de usuario obtenidos con éxito"
        dictRespuesta["data"] = tipos_usuario
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los tipos de usuario: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_tipo_usuario", methods=["POST"])
# @jwt_required()
def api_obtener_tipo_usuario():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo_usuario_id = data.get("id")

        if not tipo_usuario_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del tipo de usuario"
            return jsonify(dictRespuesta)

        tipo_usuario = controlador_tipos_usuario.obtener_tipo_usuario_por_id(tipo_usuario_id)

        if tipo_usuario:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Tipo de usuario obtenido con éxito"
            dictRespuesta["data"] = {
                "id": tipo_usuario[0],
                "tipo": tipo_usuario[1],
                "descripcion": tipo_usuario[2],
                "imagen": tipo_usuario[3],
                "disponibilidad": tipo_usuario[4]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Tipo de usuario no encontrado"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener el tipo de usuario: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_insertar_tipo_usuario", methods=["POST"])
# @jwt_required()
def api_insertar_tipo_usuario():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo = data.get("tipo")
        descripcion = data.get("descripcion")
        imagen = data.get("imagen")  # Base64

        if not tipo or not descripcion or not imagen:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requieren tipo, descripcion e imagen"
            return jsonify(dictRespuesta)

        controlador_tipos_usuario.insertar_tipo_usuario(tipo, descripcion, imagen)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de usuario insertado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar el tipo de usuario: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_tipo_usuario", methods=["POST"])
# @jwt_required()
def api_actualizar_tipo_usuario():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo_usuario_id = data.get("id")
        tipo = data.get("tipo")
        descripcion = data.get("descripcion")
        imagen = data.get("imagen")  # Base64
        disponibilidad = data.get("disponibilidad")

        if not tipo_usuario_id or not tipo or not descripcion or not imagen or disponibilidad is None:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requieren id, tipo, descripcion, imagen y disponibilidad"
            return jsonify(dictRespuesta)

        controlador_tipos_usuario.actualizar_tipo_usuario(tipo_usuario_id, tipo, descripcion, imagen, disponibilidad)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de usuario actualizado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar el tipo de usuario: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_tipo_usuario", methods=["POST"])
# @jwt_required()
def api_eliminar_tipo_usuario():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo_usuario_id = data.get("id")

        if not tipo_usuario_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del tipo de usuario"
            return jsonify(dictRespuesta)

        controlador_tipos_usuario.eliminar_tipo_usuario(tipo_usuario_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de usuario eliminado con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar el tipo de usuario: {str(e)}"
        return jsonify(dictRespuesta)

##############FIN APIS TIPO_USUARIO################

########################APIS CARACTERISTICA##############
@app.route("/api_obtener_caracteristicas", methods=["GET"])
# @jwt_required()
def api_obtener_caracteristicas():
    dictRespuesta = {}
    try:
        caracteristicas = controlador_caracteristicas.obtener_Caracteristicas()
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Características obtenidas con éxito"
        dictRespuesta["data"] = caracteristicas
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener las características: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_caracteristica", methods=["POST"])
# @jwt_required()
def api_obtener_caracteristica():
    dictRespuesta = {}
    try:
        data = request.get_json()
        caracteristica_id = data.get("id")

        if not caracteristica_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la característica"
            return jsonify(dictRespuesta)

        caracteristica = controlador_caracteristicas.obtener_caracteristica_por_id(caracteristica_id)

        if caracteristica:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Característica obtenida con éxito"
            dictRespuesta["data"] = {
                "id": caracteristica[0],
                "campo": caracteristica[1],
                "disponibilidad": caracteristica[2]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Característica no encontrada"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la característica: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_insertar_caracteristica", methods=["POST"])
# @jwt_required()
def api_insertar_caracteristica():
    dictRespuesta = {}
    try:
        data = request.get_json()
        campo = data.get("campo")

        if not campo:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere campo"
            return jsonify(dictRespuesta)

        id_caracteristica = controlador_caracteristicas.insertar_caracteristica(campo)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica insertada con éxito"
        dictRespuesta["data"] = {"id": id_caracteristica}
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar la característica: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_actualizar_caracteristica", methods=["POST"])
# @jwt_required()
def api_actualizar_caracteristica():
    dictRespuesta = {}
    try:
        data = request.get_json()
        caracteristica_id = data.get("id")
        campo = data.get("campo")
        disponibilidad = data.get("disponibilidad")

        if not caracteristica_id or not campo or disponibilidad is None:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requieren id, campo y disponibilidad"
            return jsonify(dictRespuesta)

        controlador_caracteristicas.actualizar_caracteristica(campo, disponibilidad, None, None, caracteristica_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica actualizada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la característica: {str(e)}"
        return jsonify(dictRespuesta)

@app.route("/api_eliminar_caracteristica", methods=["POST"])
# @jwt_required()
def api_eliminar_caracteristica():
    dictRespuesta = {}
    try:
        data = request.get_json()
        caracteristica_id = data.get("id")

        if not caracteristica_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la característica"
            return jsonify(dictRespuesta)

        controlador_caracteristicas.eliminar_caracteristica(caracteristica_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Característica eliminada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la característica: {str(e)}"
        return jsonify(dictRespuesta)

#####################FIN APIS CARACTERISTICAS#################


###########################APIS REDES SOCIALES###############33
@app.route("/api_obtener_redes_sociales", methods=["GET"])
# @jwt_required()
def api_obtener_redes_sociales():
    dictRespuesta = {}
    try:
        redes_sociales = controlador_redes_sociales.obtener_redes_sociales()
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Redes sociales obtenidas con éxito"
        dictRespuesta["data"] = redes_sociales
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener las redes sociales: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_obtener_red_social", methods=["POST"])
# @jwt_required()
def api_obtener_red_social():
    dictRespuesta = {}
    try:
        data = request.get_json()
        red_id = data.get("id")

        if not red_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la red social"
            return jsonify(dictRespuesta)

        red_social = controlador_redes_sociales.obtener_redes_sociales_por_id(red_id)

        if red_social:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Red social obtenida con éxito"
            dictRespuesta["data"] = {
                "id": red_social[0],
                "nomRed": red_social[1],
                "faicon_red": red_social[2],
                "enlace": red_social[3]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Red social no encontrada"

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la red social: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_insertar_red_social", methods=["POST"])
# @jwt_required()
def api_insertar_red_social():
    dictRespuesta = {}
    try:
        data = request.get_json()
        nomRed = data.get("nomRed")
        faiconRed = data.get("faiconRed")
        enlace = data.get("enlace")

        if not nomRed or not faiconRed or not enlace:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requieren nomRed, faiconRed y enlace"
            return jsonify(dictRespuesta)

        red_id = controlador_redes_sociales.insertar_redes_sociales_api(nomRed, faiconRed, enlace)
        red = clsRedesSociales(red_id, nomRed, faiconRed, enlace)
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Red social insertada con éxito"
        dictRespuesta["data"] = red.__dict__

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar la red social: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_actualizar_red_social", methods=["POST"])
# @jwt_required()
def api_actualizar_red_social():
    dictRespuesta = {}
    try:
        data = request.get_json()
        red_id = data.get("id")
        nomRed = data.get("nomRed")
        faiconRed = data.get("faiconRed")
        enlace = data.get("enlace")

        if not red_id or not nomRed or not faiconRed or not enlace:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requieren id, nomRed, faiconRed y enlace"
            return jsonify(dictRespuesta)

        controlador_redes_sociales.actualizar_redes_sociales_por_id(nomRed, faiconRed, enlace, red_id)
        red = clsRedesSociales(red_id, nomRed, faiconRed, enlace)
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Red social actualizada con éxito"
        dictRespuesta["data"] = red.__dict__

        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la red social: {str(e)}"
        return jsonify(dictRespuesta)


@app.route("/api_eliminar_red_social", methods=["POST"])
# @jwt_required()
def api_eliminar_red_social():
    dictRespuesta = {}
    try:
        data = request.get_json()
        red_id = data.get("id")

        if not red_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la red social"
            return jsonify(dictRespuesta)

        controlador_redes_sociales.eliminar_redes_sociales(red_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Red social eliminada con éxito"
        return jsonify(dictRespuesta)

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar la red social: {str(e)}"
        return jsonify(dictRespuesta)
    
#######################FIN APIS REDES SOCIALES################

##########################APIS INFORMACION DOMUS#################
@app.route("/api_obtener_informacion_domus", methods=["GET"])
# @jwt_required()
def api_obtener_informacion_domus():
    dictRespuesta = {}
    try:
        datos = controlador_informacion_domus.obtener_informacion_domus()
        if datos:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Información obtenida con éxito"
            dictRespuesta["data"] = {
                "id": datos[0],
                "correo": datos[1],
                "numero": datos[2],
                "imgLogo": datos[3],
                "imgIcon": datos[4],
                "descripcion": datos[5],
                "historia": datos[6],
                "vision": datos[7],
                "valores": datos[8],
                "mision": datos[9]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "No se encontró información"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la información: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_obtener_informacion_domus_por_id", methods=["POST"])
# @jwt_required()
def api_obtener_informacion_domus_por_id():
    dictRespuesta = {}
    try:
        data = request.get_json()
        id = data.get("id")

        if not id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la información"
            return jsonify(dictRespuesta)

        datos = controlador_informacion_domus.obtener_informacion_domus_por_id(id)
        if datos:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Información obtenida con éxito"
            dictRespuesta["data"] = {
                "id": datos[0],
                "correo": datos[1],
                "numero": datos[2],
                "imgLogo": datos[3],
                "imgIcon": datos[4],
                "descripcion": datos[5],
                "historia": datos[6],
                "vision": datos[7],
                "valores": datos[8],
                "mision": datos[9]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Información no encontrada"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la información: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_actualizar_informacion_domus", methods=["POST"])
# @jwt_required()
def api_actualizar_informacion_domus():
    dictRespuesta = {}
    try:
        data = request.get_json()

        # Crear un objeto InformacionDomus con los datos recibidos
        informacion_domus = clsInformacionDomus(
            p_id=data.get("id"),
            p_correo=data.get("correo"),
            p_numero=data.get("numero"),
            p_imgLogo=data.get("imgLogo"),
            p_imgIcon=data.get("imgIcon"),
            p_descripcion=data.get("descripcion"),
            p_historia=data.get("historia"),
            p_vision=data.get("vision"),
            p_valores=data.get("valores"),
            p_mision=data.get("mision")
        )

        # Actualizar la información en la base de datos usando el objeto
        controlador_informacion_domus.actualizar_informacion_domus_por_id(
            correo=informacion_domus.correo,
            numero=informacion_domus.numero,
            imgLogo=None,
            imgIcon=None,
            descripcion=informacion_domus.descripcion,
            historia=informacion_domus.historia,
            vision=informacion_domus.vision,
            valores=informacion_domus.valores,
            mision=informacion_domus.mision,
            id=informacion_domus.id
        )

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Información actualizada con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar la información: {str(e)}"
    
    return jsonify(dictRespuesta)

#####################FIN APIS INFORMACION DOMUS#################

##################APIS tipo_contenido##########3

@app.route("/api_insertar_tipo_contenido_info", methods=["POST"])
def api_insertar_tipo_contenido_info():
    dictRespuesta = {}
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        faicon_cont = data.get("faicon_cont")

        if not nombre or not descripcion or not faicon_cont:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (nombre, descripcion, faicon_cont)"
            return jsonify(dictRespuesta)

        # Llamar la función de inserción
        controlador_contenido_info.insertar_tipo_contenido_info(nombre, descripcion, faicon_cont)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de contenido insertado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar tipo de contenido: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_tipo_contenido_info", methods=["GET"])
def api_obtener_tipo_contenido_info():
    dictRespuesta = {}
    try:
        # Obtener los datos desde la base de datos
        tipo_contenidos = controlador_contenido_info.obtener_datos_contenido_info()
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipos de contenido obtenidos con éxito"
        dictRespuesta["data"] = tipo_contenidos
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los tipos de contenido: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_tipo_contenido_info_por_id", methods=["POST"])
def api_obtener_tipo_contenido_info_por_id():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo_contenido_id = data.get("id")

        if not tipo_contenido_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del tipo de contenido"
            return jsonify(dictRespuesta)

        # Obtener el tipo de contenido específico
        tipo_contenido = controlador_contenido_info.obtener_tipo_contenido_info_por_id(tipo_contenido_id)

        if tipo_contenido:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Tipo de contenido obtenido con éxito"
            dictRespuesta["data"] = tipo_contenido
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Tipo de contenido no encontrado"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener tipo de contenido por ID: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_actualizar_tipo_contenido_info", methods=["POST"])
def api_actualizar_tipo_contenido_info():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo_contenido_id = data.get("id")
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")
        faicon_cont = data.get("faicon_cont")
        disponibilidad = data.get("disponibilidad")

        if not tipo_contenido_id or not nombre or not descripcion or not faicon_cont:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (id, nombre, descripcion, faicon_cont)"
            return jsonify(dictRespuesta)

        # Actualizar el tipo de contenido
        controlador_contenido_info.actualizar_tipo_contenido_info_por_id(nombre, descripcion, faicon_cont, disponibilidad, tipo_contenido_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de contenido actualizado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar tipo de contenido: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_eliminar_tipo_contenido_info", methods=["POST"])
def api_eliminar_tipo_contenido_info():
    dictRespuesta = {}
    try:
        data = request.get_json()
        tipo_contenido_id = data.get("id")

        if not tipo_contenido_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del tipo de contenido"
            return jsonify(dictRespuesta)

        # Eliminar el tipo de contenido
        controlador_contenido_info.eliminar_tipo_contenido_info(tipo_contenido_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Tipo de contenido eliminado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar tipo de contenido: {str(e)}"
    return jsonify(dictRespuesta)

###############3FIN APIS TIPO CONTENID#####

#######################APIS CONTENIDO INFO###############
@app.route("/api_insertar_contenido_info", methods=["POST"])
def api_insertar_contenido_info():
    dictRespuesta = {}
    try:
        data = request.get_json()
        titulo = data.get("titulo")
        cuerpo = data.get("cuerpo")
        tipo_contenido_infoid = data.get("tipo_contenido_infoid")

        if not titulo or not cuerpo or not tipo_contenido_infoid:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (titulo, cuerpo, tipo_contenido_infoid)"
            return jsonify(dictRespuesta)

        # Llamar la función de inserción
        controlador_contenido_info.insertar_contenido_info(titulo, cuerpo, tipo_contenido_infoid)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Contenido insertado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar contenido: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_contenido_info", methods=["GET"])
def api_obtener_contenido_info():
    dictRespuesta = {}
    try:
        # Obtener los datos desde la base de datos
        contenidos = controlador_contenido_info.obtener_datos_contenido_info()
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Contenidos obtenidos con éxito"
        dictRespuesta["data"] = contenidos
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener los contenidos: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_contenido_info_por_id", methods=["POST"])
def api_obtener_contenido_info_por_id():
    dictRespuesta = {}
    try:
        data = request.get_json()
        contenido_id = data.get("id")

        if not contenido_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del contenido"
            return jsonify(dictRespuesta)

        # Obtener el contenido específico
        contenido = controlador_contenido_info.obtener_contenido_info_por_id(contenido_id)

        if contenido:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Contenido obtenido con éxito"
            dictRespuesta["data"] = {
                "id": contenido[0],
                "titulo": contenido[1],
                "cuerpo": contenido[2],
                "tipo_contenido_infoid": contenido[3]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Contenido no encontrado"

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener contenido por ID: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_actualizar_contenido_info", methods=["POST"])
def api_actualizar_contenido_info():
    dictRespuesta = {}
    try:
        data = request.get_json()
        contenido_id = data.get("id")
        titulo = data.get("titulo")
        cuerpo = data.get("cuerpo")
        tipo_contenido_infoid = data.get("tipo_contenido_infoid")

        if not contenido_id or not titulo or not cuerpo or not tipo_contenido_infoid:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (id, titulo, cuerpo, tipo_contenido_infoid)"
            return jsonify(dictRespuesta)

        # Actualizar el contenido
        controlador_contenido_info.actualizar_contenido_info_por_id(titulo, cuerpo, tipo_contenido_infoid, contenido_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Contenido actualizado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar contenido: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_eliminar_contenido_info", methods=["POST"])
def api_eliminar_contenido_info():
    dictRespuesta = {}
    try:
        data = request.get_json()
        contenido_id = data.get("id")

        if not contenido_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del contenido"
            return jsonify(dictRespuesta)

        # Eliminar el contenido
        controlador_contenido_info.eliminar_contenido_info(contenido_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Contenido eliminado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar contenido: {str(e)}"
    return jsonify(dictRespuesta)


##############FIN APIS CONTENIDO_INFO


#######################APIS CUPONES##############
@app.route("/api_insertar_cupon", methods=["POST"])
def api_insertar_cupon():
    dictRespuesta = {}
    try:
        data = request.get_json()
        codigo = data.get("codigo")
        fecha_inicio = data.get("fecha_inicio")
        fecha_vencimiento = data.get("fecha_vencimiento")
        cant_descuento = data.get("cant_descuento")

        if not codigo or not fecha_inicio or not fecha_vencimiento or not cant_descuento:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (codigo, fecha_inicio, fecha_vencimiento, cant_descuento)"
            return jsonify(dictRespuesta)

        # Crear un objeto de la clase Cupon
        cupon = clsCupon(None, codigo, None, fecha_inicio, fecha_vencimiento, cant_descuento)

        # Insertar el cupón
        controlador_cupon.insertar_cupon(cupon.codigo, cupon.fecha_inicio, cupon.fecha_vencimiento, cupon.cant_descuento)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Cupón insertado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar cupón: {str(e)}"
    return jsonify(dictRespuesta)

@app.route("/api_obtener_cupones", methods=["GET"])
def api_obtener_cupones():
    dictRespuesta = {}
    try:
        # Obtener todos los cupones
        cupones = controlador_cupon.obtener_cupones()
        
        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Cupones obtenidos con éxito"
        dictRespuesta["data"] = cupones
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener cupones: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_obtener_cupon_por_id", methods=["POST"])
def api_obtener_cupon_por_id():
    dictRespuesta = {}
    try:
        data = request.get_json()
        cupon_id = data.get("id")

        if not cupon_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del cupón"
            return jsonify(dictRespuesta)

        # Obtener el cupón específico
        cupon = controlador_cupon.obtener_cupon_por_id(cupon_id)

        if cupon:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Cupón obtenido con éxito"
            dictRespuesta["data"] = {
                "id": cupon[0],
                "codigo": cupon[1],
                "fecha_registro": cupon[2],
                "fecha_inicio": cupon[3],
                "fecha_vencimiento": cupon[4],
                "cant_descuento": cupon[5],
                "disponibilidad": cupon[6]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Cupón no encontrado"

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener cupón por ID: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_actualizar_cupon", methods=["POST"])
def api_actualizar_cupon():
    dictRespuesta = {}
    try:
        data = request.get_json()
        cupon_id = data.get("id")
        codigo = data.get("codigo")
        fecha_inicio = data.get("fecha_inicio")
        fecha_vencimiento = data.get("fecha_vencimiento")
        cant_descuento = data.get("cant_descuento")
        disponibilidad = data.get("disponibilidad")

        if not cupon_id or not codigo or not fecha_inicio or not fecha_vencimiento or not cant_descuento or disponibilidad is None:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (id, codigo, fecha_inicio, fecha_vencimiento, cant_descuento, disponibilidad)"
            return jsonify(dictRespuesta)

        # Crear un objeto de la clase Cupon
        cupon = clsCupon(cupon_id, codigo, None, fecha_inicio, fecha_vencimiento, cant_descuento)

        # Actualizar el cupón
        controlador_cupon.actualizar_cupon_por_id(cupon.codigo, cupon.fecha_inicio, cupon.fecha_vencimiento, cupon.cant_descuento, disponibilidad, cupon.id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Cupón actualizado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar cupón: {str(e)}"
    return jsonify(dictRespuesta)


@app.route("/api_eliminar_cupon", methods=["POST"])
def api_eliminar_cupon():
    dictRespuesta = {}
    try:
        data = request.get_json()
        cupon_id = data.get("id")

        if not cupon_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del cupón"
            return jsonify(dictRespuesta)

        # Eliminar el cupón
        controlador_cupon.eliminar_cupon(cupon_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Cupón eliminado con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar cupón: {str(e)}"
    return jsonify(dictRespuesta)


######################FIN APIS CUPONES############3


# EJECUTAR

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
