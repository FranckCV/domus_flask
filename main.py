from flask import Flask, render_template, request, redirect, flash, jsonify
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

app = Flask(__name__)

logo_domus = 'img/elementos/logoDomus.png'





@app.context_processor
def inject_globals():
    # General
    categoriasMenu = controlador_categorias.obtener_categorias_disponibles()
    marcasMenu = controlador_marcas.obtener_marcas_menu(10) 
    logo_foto = logo_domus

    # Administrativa
    gogogogogog = logo_domus

    return dict(marcasMenu=marcasMenu , logo_foto = logo_foto , categoriasMenu = categoriasMenu , gogogogogog = gogogogogog)


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
    
    # novedades
    # productos
    # filtro categoria
    # filtro subcategoria

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

@app.route("/selectedAnuncio=<int:id>")
def anuncio(id):
    try:
        anuncio = controlador_novedades.anuncioselect(id)
        if anuncio:
            return render_template("selectedAnuncio.html", anuncio=anuncio)
        else:
            return redirect("/error")
    except Exception as e:
        print(f"Error: {e}")
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
            return render_template("selectedCategoria.html", productosCategoria = productosCategoria , categoria = categoria, subcategorias = subcategorias , novedadesCategoria = novedadesCategoria)
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

            return render_template("selectedMarca.html", marca = marca , novedadesMarca = novedadesMarca , imagenMarcaFondo = imagenMarcaFondo , productosMarca = productosMarca , subcategoriasMarca = subcategoriasMarca)
            
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
            caracteristicasPrincipales = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,1)
            caracteristicasSecundarias = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,0)
            productosSimilares = controlador_productos.obtener_en_tarjetas_subcategoria(id,producto[10],12)
            productosMarca = controlador_productos.obtener_en_tarjetas_marca(id,producto[9],12)
            return render_template("selectedProducto.html" , productosSimilares = productosSimilares , productosMarca = productosMarca , producto = producto , marca = marca, imgs_producto = imgs_producto, caracteristicasPrincipales = caracteristicasPrincipales, caracteristicasSecundarias = caracteristicasSecundarias, categoria = categoria)
        else:
            return redirect("/error")
    except:
        return redirect("/error")


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



# @app.route("/selectedNovedad?<int:tipo_id>=<int:id>")  #falta
# def novedad(id,tipo_id):
#     if tipo_id == 3:
#         return render_template("promocionSelect.html")
#     else:
#         return redirect("/novedades")





# PAGINAS INFORMATIVAS

@app.route("/servicio_cliente") #falta
def servicio_cliente():
    return render_template("servicioCliente.html")


@app.route("/nosotros") #falta
def nosotros():
    return render_template("nosotros.html")


@app.route("/devoluciones") #falta
def devoluciones():
    return render_template("devoluciones.html")


@app.route("/terminos") #falta
def terminos():
    return render_template("terminos.html")


@app.route("/faq") #falta
def faq():
    return render_template("faq.html")


@app.route("/reclamos") #falta
def reclamos():
    return render_template("reclamos.html")


@app.route("/garantias") #falta
def garantias():
    return render_template("garantias.html")


@app.route("/puntos_venta") #falta
def puntos_venta():
    return render_template("puntosVenta.html")




# PAGINAS FORMULARIOS

@app.route("/contactanos") #falta   
def contactanos():
    return render_template("contactanos.html")


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
    productos = controlador_detalle.obtener_Detalle()  # Obtener los productos en el carrito
    return render_template("carrito.html", productosPopulares=productosPopulares, productos=productos)

@app.route("/agregar_carrito", methods=["POST"]) 
def agregar_carrito():
    producto_id = request.form["producto_id"] 
    estado = 1
    usuario_id = 1
    
    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    
    if pedido_id is None:
        pedido_id = controlador_carrito.insertar_pedido(usuario_id, estado)
    
    controlador_carrito.insertar_detalle(producto_id, pedido_id)
    
    # Redirige a la vista del carrito
    return '',204

@app.route("/aumentar_carro", methods=["POST"])
def aumentar_carro():
    producto_id = request.form.get("producto_id")
    print(f"Producto ID recibido: {producto_id}") 
    usuario_id = 1 
    estado = 1 

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    print(f"Pedido ID encontrado: {pedido_id}")  

    if pedido_id:
        controlador_carrito.aumentar_producto(pedido_id,producto_id)
        print("Producto aumentado correctamente.")
    else:
        print("No se encontró un pedido activo.")
    
    return redirect('/carrito')


@app.route("/disminuir_carro", methods=["POST"])
def disminuir_carro():
    producto_id = request.form["producto_id"]
    usuario_id = 1
    estado = 1

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

    if pedido_id:
        controlador_carrito.eliminar_producto(pedido_id,producto_id)
    
    return redirect('/carrito')

#PARA CONFIRMAR CARRE
@app.route("/confirmar_carrito", methods=["POST"])
def confirmar_carrito():
    estado = 1
    usuario_id = 1  
    total = request.form.get('total_form')
    
    if total:
        total = float(total)
    
    print(f"Total del pedido: {total}")
    
    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    existencias = controlador_detalle.obtener_Detalle_por_Id(pedido_id)
    fecha_compra = datetime.date.today()
    productos_carrito = controlador_detalle.obtener_Detalle_por_Id(pedido_id)
    
    subtotal = 0
    for producto in productos_carrito:
        cantidad = producto['cantidad']
        precio_unitario = producto['precio']
        descuento = producto.get('descuento', 0)
        total_producto = cantidad * (precio_unitario - descuento)
        subtotal += total_producto
    
    # Actualiza el pedido si hay existencias
    if existencias and len(existencias) > 0:
        estado = 2
        controlador_carrito.actualizar_estado_pedido(usuario_id, estado)
        controlador_pedido.actualizarPedido(pedido_id, fecha_compra, subtotal)

        # Renderiza el resumen de pedido con el total y existencias
        return render_template("resumen_de_pedido.html", 
                               existencias=existencias, 
                               total_pagar=total, 
                               descuento_aplicado=(descuento > 0))
    else:
        return redirect('carrito')



######################################FIN CARRO#############################################    
#######################################RESUMEN DE CARRITO##############################################
@app.route("/resumen_de_pedido") #falta
def resumen_de_pedido():
    usuario=1
    pedido_id=controlador_carrito.ultimoPedido(usuario)
    
    metodos_pago =controlador_metodo_pago.obtener_Metodo_pago()
    existencias = controlador_detalle.obtener_Detalle_por_Id(pedido_id)
    return render_template("resumen_de_pedido.html", metodos_pago=metodos_pago, existencias=existencias)

@app.route('/cancelar_compra', methods=['POST'])
def cancelar_compra():
    usuario_id = 1  
    estado_cancelado = 1

    controlador_carrito.actualizar_estado_pedido(usuario_id, estado_cancelado)

    return redirect('carrito')


#############################################################################################################
# PAGINAS USUARIO EMPLEADO












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
    controlador_marcas.insertar_marca(marca,logo_binario)
    return redirect("/listado_marcas")


@app.route("/listado_marcas")
def marcas():
    marcas = controlador_marcas.obtener_listado_marcas()
    return render_template("listado_marcas.html", marcas=marcas, active='marcas')


@app.route("/eliminar_marca", methods=["POST"])
def eliminar_marca():
    controlador_marcas.eliminar_marca(request.form["id"])
    return redirect("/listado_marcas")


@app.route("/formulario_editar_marca=<int:id>")
def editar_marca(id):
    marca = controlador_marcas.obtener_marca_por_id(id)
    return render_template("editar_marca.html", marca=marca)


@app.route("/actualizar_marca", methods=["POST"])
def actualizar_marca():
    id = request.form["id"]
    marca = request.form["marca"] 
    logo= request.files["logo"] 
    logo_binario = logo.read()  
    controlador_marcas.actualizar_marca(marca,logo_binario,id)
    return redirect("/listado_marcas")



    # CARACTERISTICAS

@app.route("/listado_caracteristicas")
def caracteristicas():
    subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
    categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
    caracteristicas = controlador_caracteristicas_subcategorias.obtenerCaracteristicas_Subcategorias()    
    categorias = controlador_categorias.obtener_categorias()
    subcategorias =controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_caracteristicas.html", caracteristicas = caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro , subcategorias=subcategorias , categorias = categorias)


@app.route("/agregar_caracteristica")
def formulario_agregar_caracteristica():
    return render_template("agregar_caracteristica.html")


@app.route("/guardar_caracteristica", methods=["POST"])
def guardar_caracteristica():
    campo = request.form["marca"]
    controlador_caracteristicas.insertar_caracteristica(campo)
    return redirect("/listado_caracteristicas")


@app.route("/eliminar_caracteristica", methods=["POST"])
def eliminar_caracteristica():
    controlador_caracteristicas.eliminar_caracteristica(request.form["id"])
    return redirect("/listado_caracteristicas")


@app.route("/formulario_editar_caracteristica=<int:id>")
def editar_caracteristica(id):
    carac = controlador_caracteristicas.obtener_caracteristica_por_id(id)
    return render_template("editar_caracteristica.html", caracteristica=carac)


@app.route("/actualizar_caracteristica", methods=["POST"])
def actualizar_caracteristica():
    id = request.form["id"]
    campo = request.form["campo"]
    disp = request.form["disponibilidad"]
    controlador_caracteristicas.actualizar_caracteristica(campo, disp, id)
    return redirect("/listado_caracteristicas")






    # CATEGORIAS / SUBCATEGORIAS   

@app.route("/agregar_categoria")
def formulario_agregar_categoria():
    return render_template("agregar_categoria.html")


@app.route("/guardar_categoria", methods=["POST"])
def guardar_categoria():
    categoria = request.form["categoria"] 
    faicon_cat = request.form["faicon_cat"] 
    disponibilidad = request.form["disponibilidad"] 
    controlador_categorias.insertar_categoria(categoria,faicon_cat,disponibilidad)
    return redirect("/listado_categorias")


@app.route("/listado_categorias")
def categorias():
    categorias = controlador_categorias.obtener_categorias()
    subcategorias =controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_categorias.html", categorias=categorias,subcategorias = subcategorias)


@app.route("/eliminar_categoria", methods=["POST"])
def eliminar_categoria():
    controlador_categorias.eliminar_categoria(request.form["id"])
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


@app.route("/agregar_subcategoria")
def formulario_agregar_subcategoria():
    categorias = controlador_categorias.obtener_categorias()
    return render_template("agregar_subcategoria.html",categorias=categorias,active='categorias')


@app.route("/guardar_subcategoria", methods=["POST"])
def guardar_subcategoria():
    nombre = request.form["nombre"] 
    faicon_subcat = request.form["faicon_subcat"] 
    disponibilidad = request.form["disponibilidad"] 
    categoria_id = request.form["categoria_id"] 
    controlador_subcategorias.insertar_subcategoria(nombre,faicon_subcat,disponibilidad,categoria_id)
    return redirect("/listado_categorias")


@app.route("/eliminar_subcategoria", methods=["POST"])
def eliminar_subcategoria():
    controlador_subcategorias.eliminar_subcategoria(request.form["id"])
    return redirect("/listado_categorias")


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
    return redirect("/listado_categorias")
########## FIN SUB-CATEGORIA ##########



########## INICIO PRODUCTOS ##########

@app.route("/agregar_producto")
def formulario_agregar_producto():
    marcas = controlador_marcas.obtener_listado_marcas()
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
    fecha_registro= request.form["fecha_registro"]
    disponibilidad= request.form["disponibilidad"] 
    marca_id= request.form["marca_id"] 
    subcategoria_id= request.form["subcategorySelect"]  
    controlador_productos.insertar_producto(nombre,price_regular,price_online,precio_oferta ,infoAdicional,stock ,fecha_registro,disponibilidad,marca_id,subcategoria_id)
    return redirect("/listado_productos")

@app.route("/listado_productos")
def productos():
    productos = controlador_productos.obtener_productos()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias)

@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    controlador_productos.eliminar_producto(request.form["id"])
    return redirect("/listado_productos")

@app.route("/formulario_editar_producto=<int:id>")
def editar_producto(id):
    producto = controlador_productos.obtener_por_id(id)
    marcas = controlador_marcas.obtener_listado_marcas()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("editar_producto.html", producto=producto,marcas=marcas, subcategorias=subcategorias,categorias = categorias)

@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto(): 
    id = request.form["id"]
    nombre = request.form["nombre"] 
    price_online= request.form["price_online"] 
    price_regular= request.form["price_regular"] 
    precio_oferta= request.form["precio_oferta"] 
    infoAdicional= request.form["infoAdicional"] 
    stock= request.form["stock"] 
    fecha_registro= request.form["fecha_registro"]
    disponibilidad= request.form["disponibilidad"] 
    marca_id= request.form["marca_id"] 
    subcategoria_id= request.form["subcategorySelect"]  
    controlador_productos.actualizar_producto(nombre,price_regular,price_online,precio_oferta ,infoAdicional,stock ,fecha_registro,disponibilidad,marca_id,subcategoria_id, id)
    return redirect("/listado_productos")

########## FIN PRODUCTOS ##########

#########################PARA TIPO NOVEDAD##############################

@app.route("/agregar_tipo_novedad")
def formulario_agregar_tipo_novedad():
    return render_template("agregar_tipo_novedad.html")

@app.route("/guardar_tipo_novedad", methods=["POST"])
def guardar_tipo_novedad():
    nombre_tipo = request.form["nombre_tipo"]
    controlador_tipos_novedad.insertar_tipo_novedad(nombre_tipo)
    return redirect("/listado_novedades") #aqui debo mostrar todo el listado de novedades y tipos

@app.route("/eliminar_tipo_novedad", methods=["POST"])
def eliminar_tipo_novedad():
    controlador_tipos_novedad.eliminar_tipo_novedad(request.form["id"])
    return redirect("/listado_novedades")

@app.route("/formulario_editar_tipo_novedad=<int:id>")
def editar_tipo_novedad(id):
    #tipo_novedad = controlador_tipos_novedad.obtener_tipo_novedad_por_id(id)
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()

    return render_template("editar_tipo_novedad.html", tipos_novedad=tipos_novedad)

@app.route("/actualizar_tipo_novedad", methods=["POST"])
def actualizar_tipo_novedad(): 
    id = request.form["id"]
    nombre_tipo = request.form["nombre_tipo"]
    controlador_tipos_novedad.actualizar_tipo_novedad(nombre_tipo, id)
    return redirect("/listado_novedades")

#########################FIN TIPONOVEDAD##############################


#########################PARA NOVEDAD##############################

@app.route("/agregar_novedad")
def formulario_agregar_novedad():
    marcas = controlador_marcas.obtener_listado_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("agregar_novedad.html", marcas=marcas, subcategorias=subcategorias, tipos_novedad=tipos_novedad, tipos_img_novedad = tipos_img_novedad)

@app.route("/guardar_novedad", methods=["POST"])
def guardar_novedad():
    nombre = request.form["nombre"]
    titulo = request.form["titulo"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    terminos = request.form["terminos"]
    disponibilidad = request.form["disponibilidad"]
    marca_id = request.form["marca"]
    subcategoria_id = request.form["subcategoria"]
    tipo_novedad_id = request.form["tipo_novedad"]

    idNovedad = controlador_novedades.insertarNovedad(
        nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id
    )

    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()

    return render_template('agregar_img_novedad.html', novedad_id=idNovedad, tipos_img_novedad = tipos_img_novedad)


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
    novedades = controlador_novedades.obtenerTodasLasNovedades()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_listado_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias)


@app.route("/eliminar_novedad", methods=["POST"])
def eliminar_novedad():
    controlador_novedades.eliminarNovedad(request.form["id"])
    return redirect("/listado_novedades")


@app.route("/formulario_editar_novedad=<int:id>")
def editar_novedad(id):
    novedad = controlador_novedades.obtenerNovedadPorId(id)
    marcas = controlador_marcas.obtener_listado_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    print(tiposNovedad)
    return render_template("editar_novedad.html", novedad=novedad, marcas=marcas, subcategorias=subcategorias, tipos_novedad=tiposNovedad, novedad_id = id)

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
    subcategoria_id = request.form["subcategoria_id"]
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
    return render_template("img_novedades_listado.html", img_novedades=img_novedades, novedad_id=novedad_id)


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
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad()
    return render_template("tipos_img_novedad_listado.html", tipos_img_novedad=tipos_img_novedad)

@app.route("/agregar_tipo_img_novedad")
def formulario_agregar_tipo_img_novedad():
    return render_template("agregar_tipo_img_novedad.html")

@app.route("/guardar_tipo_img_novedad", methods=["POST"])
def guardar_tipo_img_novedad():
    tipo = request.form["tipo"]
    disponibilidad = int(request.form["disponibilidad"])
    controlador_tipos_img_novedad.insertar_tipo_img_novedad(tipo, disponibilidad)
    return redirect("/tipos_img_novedad_listado")

@app.route("/formulario_editar_tipo_img_novedad=<int:id>")
def editar_tipo_img_novedad(id):
    tipo_img_novedad = controlador_tipos_img_novedad.obtener_tipo_img_novedad_por_id(id)
    return render_template("editar_tipo_img_novedad.html", tipo_img_novedad=tipo_img_novedad)

@app.route("/actualizar_tipo_img_novedad", methods=["POST"])
def actualizar_tipo_img_novedad():
    id = request.form["id"]
    tipo = request.form["tipo"]
    disponibilidad = int(request.form["disponibilidad"])
    controlador_tipos_img_novedad.actualizar_tipo_img_novedad(id, tipo, disponibilidad)
    return redirect("/tipos_img_novedad_listado")

@app.route("/eliminar_tipo_img_novedad", methods=["POST"])
def eliminar_tipo_img_novedad():
    id = request.form["id"]
    controlador_tipos_img_novedad.eliminar_tipo_img_novedad(id)
    return redirect("/tipos_img_novedad_listado")

#################  TIPO CONTENIDO INFO  ####################### 

@app.route("/listado_tipo_contenido_info")
def listado_tipo_contenido_info():
    tipos = controlador_contenido_info.obtener_listado_tipos_contenido()
    return render_template("listado_tipo_contenido_info.html", tipos = tipos)


@app.route("/agregar_tipo_contenido_info")
def formulario_agregar_tipo_contenido_info():
    return render_template("agregar_tipo_contenido_info.html")


@app.route("/guardar_tipo_contenido_info", methods=["POST"])
def guardar_tipo_contenido_info():
    nombre = request.form["nombre"] 
    descripcion = request.form["descripcion"] 
    faicon_cont = request.form["faicon_cont"]
    controlador_contenido_info.insertar_tipo_contenido_info(nombre , descripcion , faicon_cont)
    return redirect("/listado_tipo_contenido_info")


@app.route("/actualizar_tipo_contenido_info", methods=["POST"])
def actualizar_tipo_contenido_info():
    id = request.form["id"]
    nombre = request.form["nombre"]
    faicon_cont = request.form["faicon_cont"] 
    descripcion = request.form["descripcion"]
    controlador_contenido_info.actualizar_tipo_contenido_info_por_id(nombre,faicon_cont,descripcion,id)
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
    secciones = controlador_contenido_info.obtener_tipos_contenido()
    return render_template("listado_contenido_info.html", datos = datos , secciones = secciones)

# @app.route("/agregar_contenido_info")
# def formulario_agregar_contenido_info():
#     return render_template("agregar_contenido_info.html")


# @app.route("/guardar_contenido_info", methods=["POST"])
# def guardar_contenido_info():
#     marca = request.form["marca"] 
#     logo= request.files["logo"] 
#     logo_binario = logo.read()
#     controlador_marcas.insertar_marca(marca,logo_binario)
#     return redirect("/listado_contenido_info")


# @app.route("/eliminar_contenido_info", methods=["POST"])
# def eliminar_contenido_info():
#     controlador_marcas.eliminar_marca(request.form["id"])
#     return redirect("/listado_contenido_info")


# @app.route("/formulario_editar_contenido_info=<int:id>")
# def editar_contenido_info(id):
#     marca = controlador_marcas.obtener_marca_por_id(id)
#     return render_template("editar_contenido_info.html", marca=marca)


# @app.route("/actualizar_contenido_info", methods=["POST"])
# def actualizar_contenido_info():
#     id = request.form["id"]
#     marca = request.form["marca"] 
#     logo= request.files["logo"] 
#     logo_binario = logo.read()  
#     controlador_marcas.actualizar_marca(marca,logo_binario,id)
#     return redirect("/listado_contenido_info")

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



##########################PARA TIPOS USUARIO################
@app.route("/listado_tipos_usuario")
def listado_tipos_usuario():
    tipos_usuario = controlador_tipos_usuario.obtener_tipos_usuario()
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
    controlador_tipos_usuario.insertar_tipo_usuario(tipo, descripcion)
    return redirect("/listado_tipos_usuario")

@app.route("/formulario_editar_tipo_usuario=<int:id>")
def editar_tipo_usuario(id):
    tipo_usuario = controlador_tipos_usuario.obtener_tipo_usuario_por_id(id)
    return render_template("editar_tipo_usuario.html", tipo_usuario=tipo_usuario)

@app.route("/actualizar_tipo_usuario", methods=["POST"])
def actualizar_tipo_usuario():
    id = request.form["id"]
    tipo = request.form["tipo"]
    descripcion = request.form["descripcion"]
    controlador_tipos_usuario.actualizar_tipo_usuario(id, tipo, descripcion)
    return redirect("/listado_tipos_usuario")

@app.route("/eliminar_tipo_usuario", methods=["POST"])
def eliminar_tipo_usuario():
    id = request.form["id"]
    controlador_tipos_usuario.eliminar_tipo_usuario(id)
    return redirect("/listado_tipos_usuario")

####################FIN TIPOS USUARIO########################



#########################INICIO DE SESIÓN####################################
#PARA GUARDAR
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email-login')
        password = request.form.get('password-login')
    return render_template('iniciar_sesion.html')


#####################FIN INICIO DE SESIÓN######################
###################################CONFIRMAR PEDIDO###############################
@app.route("/confirmar_compra", methods=['POST'])
def confirmar_compra():
    return redirect("/")


############################CANCELAR PEDIDO#########################

#####################################LISTADO PEDIDOS#######################################
@app.route("/listado_pedidos")
def pedido():
    marcas = controlador_marcas.obtener_listado_marcas()
    return render_template("listado_marcas.html", marcas=marcas, active='marcas')


















# EJECUTAR


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
