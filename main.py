from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response
from flask_jwt import JWT, jwt_required, current_identity
import hashlib
import base64
import datetime
import controlador_marcas
import controlador_categorias
import controlador_productos
import controlador_imagenes_productos
import controlador_tipos_novedad
import controlador_imagenes_novedades
import controlador_caracteristicas_productos
import controlador_caracteristicas_subcategorias
import controlador_caracteristicas
import controlador_subcategorias
import controlador_usuario_cliente
import controlador_novedades
import controlador_tipos_img_novedad
import controlador_carrito
import controlador_detalle
import controlador_contenido_info
import controlador_tipos_usuario
import controlador_pedido
import controlador_metodo_pago
import controlador_motivo_comentario
import controlador_comentario
import controlador_estado_pedido
import controlador_metodo_pago
import controlador_redes_sociales
import controlador_informacion_domus


# class User(object):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def __str__(self):
#         return "User(id='%s')" % self.id

# def authenticate(username, password):
#     data = controlador_users.obtener_user_por_email(username)
#     user = User(data[0],data[1],data[2])
#     if user and user.password.encode('utf-8') == password.encode('utf-8'):
#         return user

# def identity(payload):
#     user_id = payload['identity']
#     data = controlador_users.obtener_user_por_id(user_id)
#     user = User(data[0],data[1],data[2])
#     return user



class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and user.password.encode('utf-8') == password.encode('utf-8'):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

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


@app.context_processor
def inject_globals():
    # General
    categoriasMenu = controlador_categorias.obtener_categorias_disponibles()
    marcasMenu = controlador_marcas.obtener_marcas_menu(10) 
    logo_foto = logo_domus
    redes_footer = controlador_redes_sociales.obtener_redes_sociales()
    conts_info_footer = controlador_contenido_info.obtener_tipos_contenido()
    datos_domus_main = controlador_informacion_domus.obtener_informacion_domus()

    return dict(marcasMenu=marcasMenu , logo_foto = logo_foto , categoriasMenu = categoriasMenu , redes_footer = redes_footer , conts_info_footer = conts_info_footer , datos_domus_main = datos_domus_main)


# PAGINAS GENERALES

@app.route("/") #falta
def index():
    marcasBloque = controlador_marcas.obtener_marcas_index(10)
    productosRecientes = controlador_productos.obtenerEnTarjetasMasRecientes()
    productosPopulares = controlador_productos.obtenerEnTarjetasMasPopulares()
    novedadesBanner = controlador_novedades.obtenerBannersNovedadesRecientes()
    novedadesRecientes = controlador_novedades.obtenerNovedadesRecientes()
    return render_template("index.html", novedadesRecientes = novedadesRecientes , marcasBloque = marcasBloque , productosRecientes = productosRecientes , productosPopulares = productosPopulares , novedadesBanner = novedadesBanner )


@app.route("/nuestras_marcas")
def nuestras_marcas():
    marcas = controlador_marcas.obtener_todas_marcas_recientes()
    return render_template("nuestras_marcas.html", marcas = marcas)


@app.route("/catalogo") #falta
def catalogo():
    productos = controlador_productos.obtenerEnTarjetasMasRecientes()
    categoriasFiltro = controlador_categorias.obtener_categorias_subcategorias()    
    return render_template("catalogo.html", productos = productos, categoriasFiltro = categoriasFiltro)


@app.route("/novedades") #falta
def novedades():
    productosOfertas = controlador_productos.obtenerEnTarjetasOfertas()
    return render_template("novedades.html" , productosOfertas = productosOfertas)


@app.route("/promociones") #falta
def promociones():
    promociones = controlador_novedades.mostrarNovedadesPromociones()
    return render_template("promociones.html" , promociones = promociones)


@app.route('/anuncios')
def anuncios():
    anuncios = controlador_novedades.mostrarNovedadesAnuncios()
    return render_template('anuncios.html', anuncios=anuncios)


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


# PAGINAS FORMULARIOS

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

# PAGINAS USUARIO CLIENTE




######################CARRO######################
@app.route("/carrito") 
def carrito():
    productosPopulares = controlador_productos.obtenerEnTarjetasMasRecientes()
    productos = controlador_detalle.obtener_Detalle()  
    error_message = request.args.get("error_message")  
    
    return render_template("carrito.html", productosPopulares=productosPopulares, productos=productos, error_message=error_message or "")


from flask import request, redirect, url_for

@app.route("/agregar_carrito", methods=["POST"]) 
def agregar_carrito():
    producto_id = request.form["producto_id"]
    estado = 1
    usuario_id = 1
    
    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    
    if pedido_id is None:
        pedido_id = controlador_carrito.insertar_pedido(usuario_id, estado)
    
    result=controlador_carrito.insertar_detalle(producto_id, pedido_id)
    
    referrer = request.referrer
    
    if result is None:
         # Si el usuario estaba en la página del carrito, redirige al carrito
        if "carrito" in referrer:
            return redirect(url_for('carrito'))
        else:
            # Mantener en la página actual devolviendo un código 204 (sin contenido)
            return '', 204
    else:
        return redirect(url_for('carrito', error_message=str(result)))


@app.route("/aumentar_carro", methods=["POST"])
def aumentar_carro():
    producto_id = request.form.get("producto_id")
    print(f"Producto ID recibido: {producto_id}") 
    usuario_id = 1 
    estado = 1 

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    print(f"Pedido ID encontrado: {pedido_id}")  

    if pedido_id:
        result=controlador_carrito.aumentar_producto(pedido_id,producto_id)
        if result is None:
            print("Producto aumentado correctamente.")
            return redirect('/carrito')
        else:
           return redirect(url_for('carrito', error_message=str(result)))
    else:
        print("No se encontró un pedido activo.")


@app.route("/disminuir_carro", methods=["POST"])
def disminuir_carro():
    producto_id = request.form["producto_id"]
    usuario_id = 1
    estado = 1

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

    if pedido_id:
        controlador_carrito.eliminar_producto(pedido_id,producto_id)
    
    return redirect('/carrito')


@app.route("/confirmar_carrito", methods=["POST"])
def confirmar_carrito():
    estado = 1
    usuario_id = 1
    
    valor_descuento=request.form.get('total_descuento')
    
    pedido_id=controlador_carrito.verificarIdPedido(usuario_id,estado)        

    subtotal=0
    productos_carrito = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)
    
    for producto in productos_carrito:
        cantidad = producto[3]  
        precio_unitario = producto[2]  
        total_producto = cantidad * precio_unitario
        subtotal += total_producto
    
    print(f"Total del pedido: {subtotal}")
    print(f"Descuento aplicado: {valor_descuento}")
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
        return redirect('/carrito')


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
    usuario_id = 1  
    estado_cancelado = 1    
    pedido_id=controlador_carrito.ultimoPedido(usuario_id)    
    controlador_carrito.cancelar_pedido(usuario_id, estado_cancelado,pedido_id)
    return redirect('/carrito')




# PAGINAS USUARIO ADMINISTRADOR

@app.route("/error_adm") 
def error_adm():
    return render_template("error_admin.html")


@app.route('/cuenta_administrativa')
def cuenta_administrativa():
    return render_template('cuenta_administrativa.html')


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")





@app.route("/agregar_marca")
def formulario_agregar_marca():
    return render_template("agregar_marca.html")


@app.route("/guardar_marca", methods=["POST"])
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
def marcas():
    marcas = controlador_marcas.obtener_listado_marcas()
    return render_template("listado_marcas.html", marcas=marcas, active='marcas')


@app.route("/listado_marcas_buscar")
def marcas_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    marcas = controlador_marcas.buscar_listado_marcas_nombre(nombreBusqueda)

    return render_template("listado_marcas.html", marcas=marcas, active='marcas' , nombreBusqueda = nombreBusqueda)


@app.route("/eliminar_marca", methods=["POST"])
def eliminar_marca():
    controlador_marcas.eliminar_marca(request.form["id"])
    return redirect("/listado_marcas")


@app.route("/formulario_editar_marca=<int:id>")
def editar_marca(id):
    marca = controlador_marcas.obtener_listado_marca_por_id(id)
    return render_template("editar_marca.html", marca=marca)


@app.route("/actualizar_marca", methods=["POST"])
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
def caracteristicas_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
    categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
    caracteristicas = controlador_caracteristicas.buscar_listado_Caracteristicas_nombre(nombreBusqueda)    
    categorias = controlador_categorias.obtener_categorias()
    subcategorias =controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_caracteristicas.html", caracteristicas = caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro , subcategorias=subcategorias , categorias = categorias , nombreBusqueda = nombreBusqueda)


@app.route("/listado_caracteristicas")
def caracteristicas():
    subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
    categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
    caracteristicas = controlador_caracteristicas.obtener_listado_Caracteristicas()    
    categorias = controlador_categorias.obtener_categorias()
    subcategorias =controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_caracteristicas.html", caracteristicas = caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro , subcategorias=subcategorias , categorias = categorias)


@app.route("/agregar_caracteristica")
def formulario_agregar_caracteristica():
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("agregar_caracteristica.html" , subcategorias = subcategorias,categorias = categorias)


@app.route("/guardar_caracteristica", methods=["POST"])
def guardar_caracteristica():
    campo = request.form["campo"]
    subcategoria_id = request.form["subcategorySelect"]
    id_carac = controlador_caracteristicas.insertar_caracteristica(campo)
    controlador_caracteristicas.insertar_caracteristica_subcategoria(id_carac,subcategoria_id)
    return redirect("/listado_caracteristicas")


@app.route("/eliminar_caracteristica", methods=["POST"])
def eliminar_caracteristica():
    controlador_caracteristicas.eliminar_caracteristica(request.form["id"])
    return redirect("/listado_caracteristicas")

# @app.route("/eliminar_caracteristica", methods=["POST"])
# def eliminar_caracteristica():
#     id = request.form["id"]
    
#     # Verificamos si la característica está asociada a subcategorías o productos
#     tiene_subcategorias = controlador_caracteristicas.buscar_en_caracteristica_subcategoria(id)
#     tiene_productos = controlador_caracteristicas.buscar_en_caracteristica_producto(id)

#     if tiene_subcategorias or tiene_productos:
#         # Si está asociada, mostramos el error
#         return render_template("listado_caracteristicas.html", error="La característica está asociada a subcategorías o productos y no se puede eliminar. Redirigiendo en 3 segundos...", show_modal=True)
#     else:
#         # Si no está asociada, procedemos a eliminar
#         controlador_caracteristicas.eliminar_caracteristica(id)
#         return redirect("/listado_caracteristicas")



@app.route("/formulario_editar_caracteristica=<int:id>")
def editar_caracteristica(id):
    carac = controlador_caracteristicas.obtener_caracteristica_por_id(id)
    sub_id = controlador_caracteristicas.obtener_carac_subcat_por_carac_id(id)
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("editar_caracteristica.html", caracteristica=carac , categorias = categorias , subcategorias = subcategorias,sub_id = sub_id)


@app.route("/actualizar_caracteristica", methods=["POST"])
def actualizar_caracteristica():
    id = request.form["id"]
    sub_id = request.form["sub_id"] 
    campo = request.form["campo"]
    disp = request.form["disponibilidad"]
    subcategoria_id = request.form["subcategorySelect"]
    controlador_caracteristicas.actualizar_caracteristica(campo, disp, subcategoria_id, sub_id ,id)
    return redirect("/listado_caracteristicas")






########################     SUBCATEGORIA      #########################

@app.route("/listado_subcategorias")
def subcategorias():
    categorias = controlador_categorias.obtener_listado_categorias()
    subcategorias =controlador_subcategorias.obtener_listado_subcategorias()
    return render_template("listado_subcategorias.html", categorias=categorias,subcategorias = subcategorias)


@app.route("/listado_subcategorias_buscar")
def subcategorias_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    categorias = controlador_categorias.obtener_listado_categorias()
    subcategorias =controlador_subcategorias.buscar_listado_subcategorias_nombre(nombreBusqueda)
    return render_template("listado_subcategorias.html", categorias=categorias,subcategorias = subcategorias , nombreBusqueda = nombreBusqueda)


@app.route("/agregar_subcategoria")
def formulario_agregar_subcategoria():
    categorias = controlador_categorias.obtener_categorias()
    return render_template("agregar_subcategoria.html",categorias=categorias,active='categorias')


@app.route("/guardar_subcategoria", methods=["POST"])
def guardar_subcategoria():
    nombre = request.form["nombre"] 
    faicon_subcat = request.form["faicon_subcat"] 
    categoria_id = request.form["categoria_id"] 
    controlador_subcategorias.insertar_subcategoria(nombre,faicon_subcat,1,categoria_id)
    return redirect("/listado_subcategorias")


@app.route("/eliminar_subcategoria", methods=["POST"])
def eliminar_subcategoria():
    controlador_subcategorias.eliminar_subcategoria(request.form["id"])
    return redirect("/listado_subcategorias")


@app.route("/formulario_editar_subcategoria=<int:id>")
def editar_subcategoria(id):
    subcategoria = controlador_subcategorias.obtener_subcategoria_por_id(id)
    categorias = controlador_categorias.obtener_categorias()
    return render_template("editar_subcategoria.html", subcategoria=subcategoria, categorias=categorias)


@app.route("/actualizar_subcategoria", methods=["POST"])
def actualizar_subcategoria():
    id = request.form["id"]
    nombre = request.form["nombre"] 
    faicon_subcat = request.form["faicon_subcat"] 
    disponibilidad = request.form["disponibilidad"] 
    categoria_id = request.form["categoria_id"] 
    controlador_subcategorias.actualizar_subcategoria(nombre,faicon_subcat,disponibilidad,categoria_id,id)
    return redirect("/listado_subcategorias")


########################     CATEGORIA      #########################

@app.route("/agregar_categoria")
def formulario_agregar_categoria():
    return render_template("agregar_categoria.html")


@app.route("/guardar_categoria", methods=["POST"])
def guardar_categoria():
    categoria = request.form["categoria"] 
    faicon_cat = request.form["faicon_cat"] 
    controlador_categorias.insertar_categoria(categoria,faicon_cat,1)
    return redirect("/listado_categorias")


@app.route("/listado_categorias")
def categorias():
    categorias = controlador_categorias.obtener_listado_categorias()
    subcategorias =controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_categorias.html", categorias=categorias,subcategorias = subcategorias)


@app.route("/eliminar_categoria", methods=["POST"])
def eliminar_categoria():
    id = request.form["id"]
    categoria = controlador_categorias.obtener_categoria_id_relacion(id)
    result = categoria[4]

    if result != 0:
        return render_template("listado_categorias.html", error="La categoría tiene elementos asociados y no se puede eliminar. Redirigiendo en 3 segundos...", show_modal=True)
    else:
        controlador_categorias.eliminar_categoria(id)
        return redirect("/listado_categorias")


@app.route("/formulario_editar_categoria=<int:id>")
def editar_categoria(id):
    categoria = controlador_categorias.obtener_categoria_por_id(id)
    return render_template("editar_categoria.html", categoria=categoria)


@app.route("/actualizar_categoria", methods=["POST"])
def actualizar_categoria():
    id = request.form["id"]
    categoria = request.form["categoria"] 
    faicon_cat = request.form["faicon_cat"] 
    disponibilidad = request.form["disponibilidad"] 
    controlador_categorias.actualizar_categoria(categoria,faicon_cat,disponibilidad,id)
    return redirect("/listado_categorias")


######################### PARA COMENTARIO ##############################

@app.route("/comentarios_listado")
def comentarios_listado():
    comentarios = controlador_comentario.obtener_listado_comentarios()
    motivos = controlador_motivo_comentario.obtener_motivos_disponibles()

    return render_template("listado_comentarios.html", comentarios=comentarios, motivos=motivos)


@app.route("/ver_comentario=<int:id>")
def ver_comentario(id):
    comentario = controlador_comentario.ver_comentario_por_id(id)
    motivos = controlador_motivo_comentario.obtener_listado_motivos()

    return render_template("ver_comentario.html", comentario=comentario, motivos=motivos , id = id)


@app.route("/comentarios_listado_buscar")
def comentarios_listado_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    comentarios = controlador_comentario.buscar_listado_comentarios_palabra(nombreBusqueda)
    motivos = controlador_motivo_comentario.obtener_motivos_disponibles()
    
    return render_template("listado_comentarios.html", comentarios=comentarios, motivos=motivos , nombreBusqueda = nombreBusqueda)


@app.route("/guardar_comentario", methods=["POST"])
def guardar_comentario():
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


@app.route("/eliminar_comentario", methods=["POST"])
def eliminar_comentario():
    controlador_comentario.eliminar_comentario(request.form["id"])
    return redirect("/comentarios_listado")


@app.route("/estado_comentario", methods=["POST"])
def estado_comentario():
    controlador_comentario.estado_comentario(request.form["id"])
    # return redirect("/comentarios_listado")
    return redirect(request.referrer)


@app.route("/estado_comentario_respondido", methods=["POST"])
def estado_comentario_respondido():
    controlador_comentario.estado_comentario_respondido(request.form["id"])
    return redirect(request.referrer)


######################### FIN COMENTARIO ##############################

@app.route("/motivos_comentario_listado")
def motivos_comentario_listado():
    motivos = controlador_motivo_comentario.obtener_listado_motivos()
    return render_template("listado_motivos_comentarios.html", motivos=motivos)


@app.route("/motivos_comentario_buscar")
def motivos_comentario_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    motivos = controlador_motivo_comentario.buscar_listado_motivos_nombre(nombreBusqueda)
    return render_template("listado_motivos_comentarios.html", motivos=motivos , nombreBusqueda = nombreBusqueda)


@app.route("/agregar_motivo_comentario")
def formulario_agregar_motivo_comentario():
    return render_template("agregar_motivo_comentario.html")


@app.route("/guardar_motivo_comentario", methods=["POST"])
def guardar_motivo_comentario():
    motivo = request.form["motivo"]
    controlador_motivo_comentario.insertar_motivo(motivo, 1)
    return redirect("/motivos_comentario_listado")


@app.route("/eliminar_motivo_comentario", methods=["POST"])
def eliminar_motivo_comentario():
    controlador_motivo_comentario.eliminar_motivo(request.form["id"])
    return redirect("/motivos_comentario_listado")


@app.route("/formulario_editar_motivo_comentario=<int:id>")
def editar_motivo_comentario(id):
    motivo_comentario = controlador_motivo_comentario.obtener_motivo_por_id(id)
    return render_template("editar_motivo_comentario.html", motivo_comentario=motivo_comentario)


@app.route("/actualizar_motivo_comentario", methods=["POST"])
def actualizar_motivo_comentario(): 
    id = request.form["id"]
    motivo = request.form["motivo"]
    disponibilidad = request.form["disponibilidad"]
    controlador_motivo_comentario.actualizar_motivo(motivo, disponibilidad, id)
    return redirect("/motivos_comentario_listado")


######################### FIN MOTIVO COMENTARIO ##############################


import controlador_empleados


######################### PARA USUARIO EMPLEADO ##############################

@app.route("/empleados_listado")
def empleados_listado():
    usuarios = controlador_empleados.obtener_listado_usuarios_empleados()
    tipos_usuarios = controlador_tipos_usuario.obtener_tipos_usuario()
    imagenes = controlador_empleados.obtener_listado_imagenes_usuario_empleado()

    return render_template("listado_empleados.html", usuarios=usuarios, tipos_usuarios=tipos_usuarios , imagenes = imagenes)


@app.route("/empleados_listado_buscar")
def empleados_listado_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    usuarios = controlador_empleados.buscar_listado_usuarios_empleados_nombre(nombreBusqueda)
    tipos_usuarios = controlador_tipos_usuario.obtener_tipos_usuario()
    imagenes = controlador_empleados.obtener_listado_imagenes_usuario_empleado()
    return render_template("listado_empleados.html", usuarios=usuarios, tipos_usuarios=tipos_usuarios , nombreBusqueda = nombreBusqueda , imagenes = imagenes)


@app.route("/ver_empleado=<int:id>")
def ver_empleado(id):
    usuario = controlador_empleados.ver_info_usuario_empleado(id)
    imagen = controlador_empleados.obtener_imagen_usuario_empleado_id(id)
    return render_template("ver_usuario_empleado.html", usuario = usuario , imagen = imagen)


@app.route("/agregar_empleado")
def formulario_agregar_empleado():
    return render_template("agregar_empleado.html")


@app.route("/guardar_empleado", methods=["POST"])
def guardar_empleado():
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    doc_identidad = request.form["doc_identidad"]
    
    # Verificar si se subió una imagen
    img_usuario = request.files["img_usuario"].read() if "img_usuario" in request.files and request.files["img_usuario"].filename != '' else None
    
    genero = request.form["genero"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]  # Aquí se mantiene la contraseña sin cifrado
    
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


@app.route("/actualizar_empleado", methods=["POST"])
def actualizar_empleado():
    id = request.form["id"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    doc_identidad = request.form["doc_identidad"]
    
    img_usuario = request.files["img_usuario"].read() if "img_usuario" in request.files and request.files["img_usuario"].filename != '' else None
    
    genero = request.form["genero"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]  # Aquí también se mantiene la contraseña sin cifrado
    disponibilidad = request.form["disponibilidad"]

    controlador_empleados.actualizar_usuario(
        nombres, apellidos, doc_identidad, img_usuario, genero, 
        fecha_nacimiento, telefono, correo, contraseña, disponibilidad, id
    )
    return redirect("/empleados_listado")


@app.route("/formulario_editar_empleado=<int:id>")
def editar_empleado(id):
    usuario = controlador_empleados.obtener_usuario_por_id(id) 
    imagen = controlador_empleados.obtener_imagen_usuario_empleado_id(id)  
    return render_template("editar_empleado.html", usuario=usuario , imagen = imagen)


@app.route("/eliminar_empleado", methods=["POST"])
def eliminar_empleado():
    controlador_empleados.eliminar_usuario(request.form["id"])
    return redirect("/empleados_listado")

######################### FIN USUARIO EMPLEADO ##############################




########## INICIO PRODUCTOS ##########

@app.route("/agregar_producto")
def formulario_agregar_producto():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("agregar_producto.html", marcas = marcas, subcategorias = subcategorias , categorias = categorias)

@app.route("/guardar_producto", methods=["POST"])
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
def productos():
    productos = controlador_productos.obtener_listado_productos()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias)


@app.route("/listado_productos_buscar")
def productos_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    productos = controlador_productos.buscar_listado_productos_nombre(nombreBusqueda)
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias , nombreBusqueda = nombreBusqueda)


@app.route("/eliminar_producto", methods=["POST"])
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
def editar_producto(id):
    producto = controlador_productos.obtener_info_por_id(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("editar_producto.html", producto=producto,marcas=marcas, subcategorias=subcategorias,categorias = categorias)

@app.route("/actualizar_producto", methods=["POST"])
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

########## FIN PRODUCTOS ##########

#########################PARA TIPO NOVEDAD##############################

@app.route("/listado_tipos_novedad")
def listado_tipos_novedad():
    tipos_novedad = controlador_tipos_novedad.obtener_listado_tipos_novedad()
    return render_template("listado_tipos_novedad.html", tipos_novedad=tipos_novedad)


@app.route("/agregar_tipo_novedad")
def formulario_agregar_tipo_novedad():
    return render_template("agregar_tipo_novedad.html")


@app.route("/guardar_tipo_novedad", methods=["POST"])
def guardar_tipo_novedad():
    nombre_tipo = request.form["nombre_tipo"]
    controlador_tipos_novedad.insertar_tipo_novedad(nombre_tipo)
    return redirect("/listado_tipos_novedad") #aqui debo mostrar todo el listado de novedades y tipos


@app.route("/eliminar_tipo_novedad", methods=["POST"])
def eliminar_tipo_novedad():
    controlador_tipos_novedad.eliminar_tipo_novedad(request.form["id"])
    return redirect("/listado_tipos_novedad")


@app.route("/formulario_editar_tipo_novedad=<int:id>")
def editar_tipo_novedad(id):
    tipo_novedad = controlador_tipos_novedad.obtener_tipo_novedad_por_id(id)
    id_tipo = id
    return render_template("editar_tipo_novedad.html", tipo_novedad=tipo_novedad, id_tipo = id_tipo)


@app.route("/actualizar_tipo_novedad", methods=["POST"])
def actualizar_tipo_novedad(): 
    id = request.form["id"]
    nombre_tipo = request.form["nombre_tipo"]
    disponibilidad = request.form["disponibilidad"]
    controlador_tipos_novedad.actualizar_tipo_novedad(nombre_tipo, disponibilidad , id )
    return redirect("/listado_tipos_novedad")

#########################FIN TIPONOVEDAD##############################


#########################PARA NOVEDAD##############################

@app.route("/agregar_novedad")
def formulario_agregar_novedad():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("agregar_novedad.html", marcas=marcas, subcategorias=subcategorias, categorias = categorias, tipos_novedad=tipos_novedad, tipos_img_novedad = tipos_img_novedad)

@app.route("/guardar_novedad", methods=["POST"])
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
        controlador_imagenes_novedades.insertar_imagen_novedad(nom_file, data, 1, idNovedad)

    # return render_template('agregar_img_novedad.html', novedad_id=idNovedad, tipos_img_novedad = tipos_img_novedad)
    return redirect("/listado_novedades")

@app.route("/guardar_img_novedad", methods=["POST"])
def guardar_img_novedad():
    novedad_id = request.form["novedad_id"]
    nomImagen = request.form["nomImagen"]
    tipo_img_novedad_id = request.form["tipo_img_novedad"]
    img = request.files["imagen"]

    if img:
        imagen = img.read()
        controlador_imagenes_novedades.insertar_imagen_novedad(nomImagen, imagen, tipo_img_novedad_id, novedad_id)
    
    return render_template("agregar_img_novedad.html", novedad_id=novedad_id, tipos_img_novedad=controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles(), imagen_agregada=True)


@app.route("/listado_novedades")
def novedades_listado():
    novedades = controlador_novedades.obtener_listado_novedades()
    imgs_nov = controlador_imagenes_novedades.obtener_todas_imagenes_novedad()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias , categorias=categorias , imgs_nov = imgs_nov)


@app.route("/listado_novedades_buscar")
def novedades_listado_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    novedades = controlador_novedades.buscar_listado_novedades_nombre_titulo(nombreBusqueda)
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias , nombreBusqueda = nombreBusqueda)


@app.route("/ver_novedad=<int:id>")
def ver_novedad(id):
    novedad = controlador_novedades.obtener_novedad_id(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    imagenes = controlador_imagenes_novedades.obtener_imagenes_novedad_id(id)
    return render_template("ver_novedad.html", novedad=novedad, marcas=marcas , subcategorias = subcategorias, id = id ,tiposNovedad = tiposNovedad , imagenes = imagenes , categorias = categorias)


@app.route("/eliminar_novedad", methods=["POST"])
def eliminar_novedad():
    controlador_novedades.eliminarNovedad(request.form["id"])
    return redirect("/listado_novedades")


@app.route("/formulario_editar_novedad=<int:id>")
def editar_novedad(id):
    novedad = controlador_novedades.obtenerNovedadPorId(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    return render_template("editar_novedad.html", novedad=novedad, marcas=marcas, subcategorias=subcategorias, tipos_novedad=tiposNovedad, novedad_id = id , categorias = categorias)

@app.route("/actualizar_novedad", methods=["POST"])
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


@app.route("/agregar_img_novedad=<int:novedad_id>")
def formulario_agregar_img_novedad(novedad_id):
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("agregar_img_novedad.html", novedad_id=novedad_id, tipos_img_novedad=tipos_img_novedad)


@app.route("/img_novedades_listado=<int:novedad_id>")
def img_novedades_listado(novedad_id):
    novedad_info = novedad_id
    img_novedades = controlador_imagenes_novedades.obtener_imagenes_novedad_por_id(novedad_id=novedad_id)
    return render_template("listado_img_novedades.html", img_novedades=img_novedades, novedad_id=novedad_id)


@app.route("/eliminar_img_novedad", methods=["POST"])
def eliminar_img_novedad():
    controlador_imagenes_novedades.eliminar_imagen_novedad(request.form["id"])
    novedad_id = request.form["novedad_id"]
    return redirect(f"/img_novedades_listado={novedad_id}")


@app.route("/formulario_editar_img_novedad=<int:id>")
def editar_img_novedad(id):
    img_novedad = controlador_imagenes_novedades.obtener_imagenes_novedad_por_id(id)
    novedad_id = controlador_imagenes_novedades.obtener_novedad_id_por_imagen_id(id)
    print(novedad_id)
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("editar_img_novedad.html", img_novedad=img_novedad, tipos_img_novedad=tipos_img_novedad, novedad_id = novedad_id, id=id)


@app.route("/actualizar_img_novedad", methods=["POST"])
def actualizar_img_novedad():
    id = request.form["id"]
    nom_imagen = request.form["nomImagen"]
    tipo_img_novedad_id = request.form["tipo_img_novedad"]
    novedad_id = request.form["novedad_id"]

    imagen = request.files["imagen"].read() if "imagen" in request.files else None

    # print(f"ID: {id}")
    # print(f"Nombre de Imagen: {nom_imagen}")
    # print(f"Tipo de Imagen ID: {tipo_img_novedad_id}")
    # print(f"Novedad ID: {novedad_id}")

    controlador_imagenes_novedades.actualizar_imagen_novedad(id, nom_imagen, imagen, tipo_img_novedad_id, novedad_id)
    return redirect(f"/img_novedades_listado={novedad_id}")


#######################################para tipo IMG NOVEDAD##################


@app.route("/tipos_img_novedad_listado")
def tipos_img_novedad_listado():
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_listado_tipos_img_novedad()
    return render_template("listado_tipos_img_novedad.html", tipos_img_novedad=tipos_img_novedad)

@app.route("/agregar_tipo_img_novedad")
def formulario_agregar_tipo_img_novedad():
    return render_template("agregar_tipo_img_novedad.html")

@app.route("/guardar_tipo_img_novedad", methods=["POST"])
def guardar_tipo_img_novedad():
    tipo = request.form["tipo"]
    controlador_tipos_img_novedad.insertar_tipo_img_novedad(tipo, 1)
    return redirect("/tipos_img_novedad_listado")

@app.route("/formulario_editar_tipo_img_novedad=<int:id>")
def editar_tipo_img_novedad(id):
    tipo_img_novedad = controlador_tipos_img_novedad.obtener_tipo_img_novedad_por_id(id)
    return render_template("editar_tipo_img_novedad.html", tipo_img_novedad=tipo_img_novedad)

@app.route("/actualizar_tipo_img_novedad", methods=["POST"])
def actualizar_tipo_img_novedad():
    id = request.form["id"]
    tipo = request.form["tipo"]
    disponibilidad = request.form["disponibilidad"]
    controlador_tipos_img_novedad.actualizar_tipo_img_novedad(id, tipo, disponibilidad)
    return redirect("/tipos_img_novedad_listado")

@app.route("/eliminar_tipo_img_novedad", methods=["POST"])
def eliminar_tipo_img_novedad():
    id = request.form["id"]
    controlador_tipos_img_novedad.eliminar_tipo_img_novedad(id)
    return redirect("/tipos_img_novedad_listado")


#################  TIPO CONTENIDO INFO  ####################### 


@app.route("/ver_tipo_contenido_info=<int:id>")
def ver_tipo_contenido_info(id):
    contenido = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
    articulos = controlador_contenido_info.obtener_datos_contenido_por_tipo(id)
    return render_template("ver_contenido_info.html", articulos = articulos , contenido = contenido)


@app.route("/listado_tipo_contenido_info")
def listado_tipo_contenido_info():
    tipos = controlador_contenido_info.obtener_listado_tipos_contenido()
    return render_template("listado_tipo_contenido_info.html", tipos = tipos)


@app.route("/listado_tipo_contenido_info_buscar")
def listado_tipo_contenido_info_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    tipos = controlador_contenido_info.buscar_listado_tipos_contenido_nombre(nombreBusqueda)
    return render_template("listado_tipo_contenido_info.html", tipos = tipos , nombreBusqueda = nombreBusqueda)


@app.route("/agregar_tipo_contenido_info")
def formulario_agregar_tipo_contenido_info():
    return render_template("agregar_tipo_contenido_info.html")


@app.route("/guardar_tipo_contenido_info", methods=["POST"])
def guardar_tipo_contenido_info():
    nombre = request.form["nombre"] 
    descripcion = request.form["descripcion"] 
    faicon_cont = request.form["icono"]
    controlador_contenido_info.insertar_tipo_contenido_info(nombre , descripcion , faicon_cont)
    return redirect("/listado_tipo_contenido_info")


@app.route("/actualizar_tipo_contenido_info", methods=["POST"])
def actualizar_tipo_contenido_info():
    id = request.form["id"]
    nombre = request.form["nombre"]
    faicon_cont = request.form["icono"] 
    descripcion = request.form["descripcion"]
    disponibilidad = request.form["disponibilidad"]
    controlador_contenido_info.actualizar_tipo_contenido_info_por_id(nombre,descripcion,faicon_cont,disponibilidad,id)
    return redirect("/listado_tipo_contenido_info")


@app.route("/formulario_editar_tipo_contenido_info=<int:id>")
def editar_tipo_contenido_info(id):
    tipo = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
    return render_template("editar_tipo_contenido_info.html", tipo=tipo)


@app.route("/eliminar_tipo_contenido_info", methods=["POST"])
def eliminar_tipo_contenido_info():
    controlador_contenido_info.eliminar_tipo_contenido_info(request.form["id"])
    return redirect("/listado_tipo_contenido_info")



#################  CONTENIDO INFO  ####################### 

@app.route("/listado_contenido_info")
def listado_contenido_info():
    datos = controlador_contenido_info.obtener_datos_contenido()
    secciones = controlador_contenido_info.obtener_listado_tipos_contenido()
    return render_template("listado_contenido_info.html", datos = datos , secciones = secciones)


@app.route("/listado_contenido_info_buscar")
def listado_contenido_info_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    datos = controlador_contenido_info.buscar_datos_contenido_info_titulo(nombreBusqueda)
    secciones = controlador_contenido_info.obtener_listado_tipos_contenido()
    return render_template("listado_contenido_info.html", datos = datos , secciones = secciones , nombreBusqueda = nombreBusqueda)


@app.route("/agregar_contenido_info")
def formulario_agregar_contenido_info():
    secciones = controlador_contenido_info.obtener_tipos_contenido()
    return render_template("agregar_contenido_info.html" , secciones = secciones)


@app.route("/guardar_contenido_info", methods=["POST"])
def guardar_contenido_info():
    titulo = request.form["titulo"] 
    cuerpo = request.form["cuerpo"] 
    tipo = request.form["tipo"]
    controlador_contenido_info.insertar_contenido_info(titulo , cuerpo , tipo)
    return redirect("/listado_contenido_info")


@app.route("/actualizar_contenido_info", methods=["POST"])
def actualizar_contenido_info():
    id = request.form["id"]
    cuerpo = request.form["cuerpo"]
    titulo = request.form["titulo"] 
    tipo = request.form["tipo"]
    controlador_contenido_info.actualizar_contenido_info_por_id(titulo , cuerpo , tipo,id)
    return redirect("/listado_contenido_info")


@app.route("/formulario_editar_contenido_info=<int:id>")
def editar_contenido_info(id):
    secciones = controlador_contenido_info.obtener_tipos_contenido()
    tipo = controlador_contenido_info.obtener_contenido_info_por_id(id)
    return render_template("editar_contenido_info.html", tipo=tipo , secciones = secciones)


@app.route("/eliminar_contenido_info", methods=["POST"])
def eliminar_contenido_info():
    controlador_contenido_info.eliminar_contenido_info(request.form["id"])
    return redirect("/listado_contenido_info")



################### ESTADOS DE PEDIDO ####################

@app.route("/listado_estado_pedido")
def listado_estado_pedido():
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    return render_template("listado_estados_pedidos.html", estados = estados)


@app.route("/formulario_agregar_estado_pedido")
def formulario_agregar_estado_pedido():
    return render_template("agregar_estado_pedido.html")


@app.route("/guardar_estado_pedido", methods=["POST"])
def guardar_estado_pedido():
    nombre = request.form["nombre"]
    controlador_estado_pedido.insertar_estado_pedido(nombre)
    return redirect("/listado_estado_pedido")


@app.route("/actualizar_estado_pedido", methods=["POST"])
def actualizar_estado_pedido():
    id = request.form["id"]
    nombre = request.form["nombre"]
    controlador_estado_pedido.actualizar_estado_pedido_por_id(nombre,id)
    return redirect("/listado_estado_pedido")


@app.route("/formulario_editar_estado_pedido=<int:id>")
def editar_estado_pedido(id):
    estado = controlador_estado_pedido.obtener_estado_pedido_por_id(id)
    return render_template("editar_estado_pedido.html", estado=estado)


@app.route("/eliminar_estado_pedido", methods=["POST"])
def eliminar_estado_pedido():
    controlador_estado_pedido.eliminar_estado_pedido(request.form["id"])
    return redirect("/listado_estado_pedido")



################### METODOS PAGO ####################


@app.route("/listado_metodo_pago")
def listado_metodo_pago():
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_metodo_pago.html", metodos = metodos)


@app.route("/formulario_agregar_metodo_pago")
def formulario_agregar_metodo_pago():
    return render_template("agregar_metodo_pago.html")


@app.route("/guardar_metodo_pago", methods=["POST"])
def guardar_metodo_pago():
    nombre = request.form["nombre"]
    controlador_metodo_pago.insertar_metodo_pago(nombre)
    return redirect("/listado_metodo_pago")


@app.route("/actualizar_metodo_pago", methods=["POST"])
def actualizar_metodo_pago():
    id = request.form["id"]
    nombre = request.form["nombre"]
    disponibilidad = request.form["disponibilidad"]
    controlador_metodo_pago.actualizar_metodo_pago_por_id(nombre,disponibilidad,id)
    return redirect("/listado_metodo_pago")


@app.route("/formulario_editar_metodo_pago=<int:id>")
def editar_metodo_pago(id):
    metodo = controlador_metodo_pago.obtener_metodo_pago_por_id(id)
    return render_template("editar_metodo_pago.html", metodo=metodo)


@app.route("/eliminar_metodo_pago", methods=["POST"])
def eliminar_metodo_pago():
    controlador_metodo_pago.eliminar_metodo_pago(request.form["id"])
    return redirect("/listado_metodo_pago")



################### REDES SOCIALES ####################


@app.route("/listado_redes_sociales")
def listado_redes_sociales():
    redes = controlador_redes_sociales.obtener_redes_sociales()
    return render_template("listado_redes_sociales.html", redes = redes)


@app.route("/formulario_agregar_redes_sociales")
def formulario_agregar_redes_sociales():
    return render_template("agregar_redes_sociales.html")


@app.route("/guardar_redes_sociales", methods=["POST"])
def guardar_redes_sociales():
    nombre = request.form["nombre"]
    enlace = request.form["enlace"]
    icono = request.form["icono"]
    controlador_redes_sociales.insertar_redes_sociales(nombre,icono,enlace)
    return redirect("/listado_redes_sociales")


@app.route("/actualizar_redes_sociales", methods=["POST"])
def actualizar_redes_sociales():
    id = request.form["id"]
    nombre = request.form["nombre"]
    enlace = request.form["enlace"]
    icono = request.form["icono"]
    controlador_redes_sociales.actualizar_redes_sociales_por_id(nombre,icono,enlace,id)
    return redirect("/listado_redes_sociales")


@app.route("/formulario_editar_redes_sociales=<int:id>")
def editar_redes_sociales(id):
    red = controlador_redes_sociales.obtener_redes_sociales_por_id(id)
    return render_template("editar_redes_sociales.html", red=red)


@app.route("/eliminar_redes_sociales", methods=["POST"])
def eliminar_redes_sociales():
    controlador_redes_sociales.eliminar_redes_sociales(request.form["id"])
    return redirect("/listado_redes_sociales")

######################## CUPONES #######################
# @app.route("/listado_cupones")
# def listado_cupones():
#     redes = controlador_redes_sociales.obtener_redes_sociales()
#     return render_template("listado_redes_sociales.html", redes = redes)



############### DATOS PRINCIPALES ############################

@app.route("/listado_datos_principales")
def listado_datos_principales():
    info = controlador_informacion_domus.obtener_informacion_domus()
    return render_template("ver_datos_principales.html", info = info)


@app.route("/formulario_editar_datos_principales=<int:id>")
def editar_datos_principales(id):
    info = controlador_informacion_domus.obtener_informacion_domus_por_id(id)
    return render_template("editar_datos_principales.html", info = info)


@app.route("/actualizar_datos_principales", methods=["POST"])
def actualizar_datos_principales():
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

    controlador_informacion_domus.actualizar_informacion_domus_por_id(correo,numero,logo,icon,descripcion,historia,vision,valores,mision,id)
    return redirect("/listado_datos_principales")






##########################PARA TIPOS USUARIO################
@app.route("/listado_tipos_usuario")
def listado_tipos_usuario():
    tipos_usuario = controlador_tipos_usuario.obtener_listado_tipos_usuario()
    # if tipos_usuario:
    #     print(f"id: {tipos_usuario[0][0]}")
    #     print(f"nombre: {tipos_usuario[0][1]}")
    #     print(f"descripción: {tipos_usuario[0][2]}")
    # else:
    #     print("No se encontraron registros en la tabla TIPO_USUARIO")
    return render_template("listado_tipos_usuario.html", tipos_usuario=tipos_usuario)

@app.route("/agregar_tipo_usuario")
def formulario_agregar_tipo_usuario():
    return render_template("agregar_tipo_usuario.html")

@app.route("/guardar_tipo_usuario", methods=["POST"])
def guardar_tipo_usuario():
    tipo = request.form["tipo"]
    descripcion = request.form["descripcion"]
    imagen= request.files["img_user"]
    img_binario = imagen.read()

    controlador_tipos_usuario.insertar_tipo_usuario(tipo, descripcion,img_binario)
    return redirect("/listado_tipos_usuario")

@app.route("/formulario_editar_tipo_usuario=<int:id>")
def editar_tipo_usuario(id):
    tipo_usuario = controlador_tipos_usuario.obtener_tipo_usuario_por_id(id)
    return render_template("editar_tipo_usuario.html", tipo_usuario=tipo_usuario)

@app.route("/actualizar_tipo_usuario", methods=["POST"])
def actualizar_tipo_usuario():
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
    # disponibilidad = request.form.get("disponibilidad")
    # disp = 0

    # if disponibilidad:
    #     disp = 1
    # else: 
    #     disp = 0

    controlador_tipos_usuario.actualizar_tipo_usuario(id, tipo, descripcion , img_binario , disp)
    return redirect("/listado_tipos_usuario")

@app.route("/eliminar_tipo_usuario", methods=["POST"])
def eliminar_tipo_usuario():
    id = request.form["id"]
    controlador_tipos_usuario.eliminar_tipo_usuario(id)
    return redirect("/listado_tipos_usuario")

####################FIN TIPOS USUARIO########################

####################PARA CLIENTES#######################

@app.route("/listado_clientes")
def listado_clientes():
    usuarios_clientes = controlador_usuario_cliente.obtener_listado_usuarios_clientes()
    imagenes = controlador_usuario_cliente.obtener_listado_imagenes_usuario_cliente()
    return render_template("listado_clientes.html", usuarios_clientes=usuarios_clientes , imagenes = imagenes)


@app.route("/listado_clientes_buscar")
def listado_clientes_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    usuarios_clientes = controlador_usuario_cliente.buscar_listado_usuarios_clientes_nombre(nombreBusqueda)
    imagenes = controlador_usuario_cliente.obtener_listado_imagenes_usuario_cliente()
    return render_template("listado_clientes.html", usuarios_clientes=usuarios_clientes , nombreBusqueda = nombreBusqueda , imagenes = imagenes)


@app.route("/ver_cliente=<int:id>")
def ver_cliente(id):
    usuario = controlador_usuario_cliente.ver_info_usuario_cliente(id)
    imagen = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
    pedidos = controlador_pedido.obtener_listado_pedidos_usuario_id(id)
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("ver_usuario_cliente.html", usuario = usuario , pedidos = pedidos , estados = estados , metodos = metodos , imagen = imagen)


@app.route("/agregar_usuario_cliente")
def formulario_agregar_usuario_cliente():
    return render_template("iniciar_sesion.html") ##falta miau


@app.route("/formulario_editar_cliente=<int:id>")
def editar_cliente(id):
    usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(id)
    imagen = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
    return render_template("editar_cliente.html", usuario=usuario , imagen = imagen)


@app.route("/actualizar_cliente", methods=["POST"])
def actualizar_cliente():
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


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    id = request.form["id"]
    controlador_usuario_cliente.eliminar_usuario_cliente(id)
    return redirect("/listado_clientes")




####################FIN CLIENTES########################








#########################INICIO DE SESIÓN####################################
#PARA GUARDAR

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
        disponibilidad=1
        tipo_usuario = 3

        # h = hashlib.new('sha256')
        # h.update(bytes(password, encoding='utf-8'))
        # epassword = h.hexdigest()

        result = controlador_usuario_cliente.insertar_usuario(
            nombres, apellidos, dni, genero, fecha_nacimiento, telefono, correo, password, disponibilidad, tipo_usuario
        )
        print(result)
        if result == 1:
            return render_template("iniciar_sesion.html", mostrar=True)
        elif result == 0:
            return render_template("iniciar_sesion.html", mostrar=False)
        else:
            return "Error al procesar la solicitud", 400 
    except Exception as e:
        print(f"Error en registrar_cliente: {e}")
        return "Error en el servidor", 500 


@app.route("/login", methods=['POST'])
def login():
    
    email = request.form.get('email-login')
    password = request.form.get('password-login')
    
    user=controlador_usuario_cliente
    
    return render_template('iniciar_sesion.html')


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

#####################FIN INICIO DE SESIÓN######################
###################################CONFIRMAR PEDIDO###############################
@app.route("/confirmar_compra", methods=['POST'])
def confirmar_compra():
    usuario_id = 1
    fecha_compra = datetime.date.today()
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


################################################################
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


# EJECUTAR

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
