from flask import Flask, render_template, request, redirect, flash, jsonify
import controlador_marcas
import controlador_categorias
import controlador_productos
import controlador_imagenes_productos
import controlador_tipos_novedad
import controlador_imagenes_novedades
import controlador_caracteristicas_productos
import controlador_subcategorias
import controlador_usuario_cliente
import controlador_novedades
import controlador_tipos_img_novedad

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
            marca = controlador_marcas.obtener_marca_disponible_por_id(producto[9])
            imgs_producto = controlador_imagenes_productos.obtener_imagenes_por_producto(id)
            caracteristicasPrincipales = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,1)
            caracteristicasSecundarias = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,0)
            productosSimilares = controlador_productos.obtener_en_tarjetas_subcategoria(id,producto[10],12)
            productosMarca = controlador_productos.obtener_en_tarjetas_marca(id,producto[9],12)
            return render_template("selectedProducto.html" , productosSimilares = productosSimilares , productosMarca = productosMarca , producto = producto , marca = marca, imgs_producto = imgs_producto, caracteristicasPrincipales = caracteristicasPrincipales, caracteristicasSecundarias = caracteristicasSecundarias)
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

@app.route("/carrito") #falta
def carrito():
    productosPopulares = controlador_productos.obtenerEnTarjetasMasRecientes()
    return render_template("carrito.html" , productosPopulares = productosPopulares)






# PAGINAS USUARIO EMPLEADO




# PAGINAS USUARIO ADMINISTRADOR



@app.route('/cuenta_administrativa')
def cuenta_administrativa():
    return render_template('cuenta_administrativa.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

########## INICIO MARCAS ##########

@app.route("/agregar_marca")
def formulario_agregar_marca():
    return render_template("agregar_marca.html")

@app.route("/guardar_marca", methods=["POST"])
def guardar_marca():
    marca = request.form["marca"] 
    logo= request.files["logo"] 
    logo_binario = logo.read()
    controlador_marcas.insertar_marca(marca,logo_binario)
    return redirect("/marcas")

@app.route("/marcas")
def marcas():
    marcas = controlador_marcas.obtener_marcas()
    return render_template("marcas.html", marcas=marcas, active='marcas')

@app.route("/eliminar_marca", methods=["POST"])
def eliminar_marca():
    controlador_marcas.eliminar_marca(request.form["id"])
    return redirect("/marcas")

@app.route("/formulario_editar_marca/<int:id>")
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
    return redirect("/marcas")

########## FIN MARCAS ##########

########## INICIO CATEGORIA ##########
@app.route("/agregar_categoria")
def formulario_agregar_categoria():
    return render_template("agregar_categoria.html")

@app.route("/guardar_categoria", methods=["POST"])
def guardar_categoria():
    categoria = request.form["categoria"] 
    faicon_cat = request.form["faicon_cat"] 
    disponibilidad = request.form["disponibilidad"] 
    controlador_categorias.insertar_categoria(categoria,faicon_cat,disponibilidad)
    return redirect("/categorias")
    
@app.route("/categorias")
def categorias():
    categorias = controlador_categorias.obtener_categorias()
    subcategorias =controlador_subcategorias.obtener_subcategorias()
    return render_template("categorias.html", categorias=categorias,subcategorias = subcategorias)

@app.route("/eliminar_categoria", methods=["POST"])
def eliminar_categoria():
    controlador_categorias.eliminar_categoria(request.form["id"])
    return redirect("/categorias")

@app.route("/formulario_editar_categoria/<int:id>")
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
    return redirect("/categorias")
########## FIN CATEGORIA ##########

########## INICIO SUB-CATEGORIA ##########
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
    return redirect("/categorias")

@app.route("/eliminar_subcategoria", methods=["POST"])
def eliminar_subcategoria():
    controlador_subcategorias.eliminar_subcategoria(request.form["id"])
    return redirect("/categorias")

@app.route("/formulario_editar_subcategoria/<int:id>")
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
    return redirect("/categorias")
########## FIN SUB-CATEGORIA ##########


########## INICIO PRODUCTOS ##########

@app.route("/agregar_producto")
def formulario_agregar_producto():
    marcas = controlador_marcas.obtener_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("agregar_producto.html", marcas = marcas, subcategorias = subcategorias)

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
    subcategoria_id= request.form["subcategoria_id"]  
    controlador_productos.insertar_producto(nombre,price_regular,price_online,precio_oferta ,infoAdicional,stock ,fecha_registro,disponibilidad,marca_id,subcategoria_id)
    return redirect("/productos")

@app.route("/productos")
def productos():
    productos = controlador_productos.obtener_productos()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("productos.html", productos=productos, marcas=marcas , subcategorias=subcategorias , categorias = categorias)

@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    controlador_productos.eliminar_producto(request.form["id"])
    return redirect("/productos")

@app.route("/formulario_editar_producto/<int:id>")
def editar_producto(id):
    producto = controlador_productos.obtener_por_id(id)
    marcas = controlador_marcas.obtener_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("editar_producto.html", producto=producto,marcas=marcas, subcategorias=subcategorias)

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
    subcategoria_id= request.form["subcategoria_id"]  
    controlador_productos.actualizar_producto(nombre,price_regular,price_online,precio_oferta ,infoAdicional,stock ,fecha_registro,disponibilidad,marca_id,subcategoria_id, id)
    return redirect("/productos")

########## FIN PRODUCTOS ##########

#########################PARA TIPO NOVEDAD##############################

@app.route("/agregar_tipo_novedad")
def formulario_agregar_tipo_novedad():
    return render_template("agregar_tipo_novedad.html")

@app.route("/guardar_tipo_novedad", methods=["POST"])
def guardar_tipo_novedad():
    nombre_tipo = request.form["nombre_tipo"]
    controlador_tipos_novedad.insertar_tipo_novedad(nombre_tipo)
    return redirect("/novedades_listado") #aqui debo mostrar todo el listado de novedades y tipos

@app.route("/eliminar_tipo_novedad", methods=["POST"])
def eliminar_tipo_novedad():
    controlador_tipos_novedad.eliminar_tipo_novedad(request.form["id"])
    return redirect("/novedades_listado")

@app.route("/formulario_editar_tipo_novedad/<int:id>")
def editar_tipo_novedad(id):
    tipo_novedad = controlador_tipos_novedad.obtener_tipo_novedad_por_id(id)
    return render_template("editar_tipo_novedad.html", tipo_novedad=tipo_novedad)

@app.route("/actualizar_tipo_novedad", methods=["POST"])
def actualizar_tipo_novedad(): 
    id = request.form["id"]
    nombre_tipo = request.form["nombre_tipo"]
    controlador_tipos_novedad.actualizar_tipo_novedad(nombre_tipo, id)
    return redirect("/novedades_listado")

#########################FIN TIPONOVEDAD##############################


#########################PARA NOVEDAD##############################

@app.route("/agregar_novedad")
def formulario_agregar_novedad():
    marcas = controlador_marcas.obtener_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    return render_template("agregar_novedad.html", marcas=marcas, subcategorias=subcategorias, tipos_novedad=tipos_novedad)

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

    idNovedad = controlador_novedades.insertarNovedad(nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id)
    
    guardar_img_novedad(idNovedad=idNovedad)
    
    return redirect("/novedades_listado")

def guardar_img_novedad(idNovedad):
    novedad_id = idNovedad
    nom_imagen = 'Por definir'
    tipo_img_novedad_id = 1 #por defecto este ps luego se edita XDD
    
    if "imagenes" in request.files:
        imagenes = request.files.getlist("imagenes")
        
        for imagen in imagenes:
            imagen_data = imagen.read()
            controlador_novedades.insertarImagenNovedad(nom_imagen, imagen_data, tipo_img_novedad_id, novedad_id)

@app.route("/novedades_listado")
def novedades_listado():
    novedades = controlador_novedades.obtenerTodasLasNovedades()
    marcas = controlador_marcas.obtener_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("novedades_listado.html", novedades=novedades, marcas=marcas, subcategorias=subcategorias)

@app.route("/eliminar_novedad", methods=["POST"])
def eliminar_novedad():
    controlador_novedades.eliminarNovedad(request.form["id"])
    return redirect("/novedades_listado")

@app.route("/formulario_editar_novedad/<int:id>")
def editar_novedad(id):
    novedad = controlador_novedades.obtenerNovedadPorId(id)
    marcas = controlador_marcas.obtener_marcas()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    print(tiposNovedad)
    return render_template("editar_novedad.html", novedad=novedad, marcas=marcas, subcategorias=subcategorias, tiposNovedad=tiposNovedad)

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
    return redirect("/novedades_listado")

#########################FIN NOVEDAD####################################

# #########################PARA NOVEDAD##############################

# @app.route("/agregar_novedad")
# def formulario_agregar_novedad():
#     marcas = controlador_marcas.obtener_marcas()
#     subcategorias = controlador_subcategorias.obtener_subcategorias()
#     tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
#     return render_template("agregar_novedad.html", marcas=marcas, subcategorias=subcategorias, tipos_novedad=tipos_novedad)

# @app.route("/guardar_novedad", methods=["POST"])
# def guardar_novedad():
#     nombre = request.form["nombre"]
#     titulo = request.form["titulo"]
#     fecha_inicio = request.form["fecha_inicio"]
#     fecha_vencimiento = request.form["fecha_vencimiento"]
#     terminos = request.form["terminos"]
#     disponibilidad = request.form["disponibilidad"]
#     marca_id = request.form["marca"]
#     subcategoria_id = request.form["subcategoria"]
#     tipo_novedad_id = request.form["tipo_novedad"]

#     imagen = request.files["imagen"].read() if "imagen" in request.files else None

#     controlador_novedades.insertarNovedad(nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id, imagen)
#     return redirect("/novedades_listado")

# @app.route("/novedades_listado")
# def novedades_listado():
#     novedades = controlador_novedades.obtenerTodasLasNovedades()
#     marcas = controlador_marcas.obtener_marcas()
#     subcategorias = controlador_subcategorias.obtener_subcategorias()
#     return render_template("novedades_listado.html", novedades=novedades, marcas=marcas, subcategorias=subcategorias)

# @app.route("/eliminar_novedad", methods=["POST"])
# def eliminar_novedad():
#     controlador_novedades.eliminarNovedad(request.form["id"])
#     return redirect("/novedades_listado")

# @app.route("/formulario_editar_novedad/<int:id>")
# def editar_novedad(id):
#     novedad = controlador_novedades.obtenerNovedadPorId(id)
#     marcas = controlador_marcas.obtener_marcas()
#     subcategorias = controlador_subcategorias.obtener_subcategorias()
#     tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
#     print(tiposNovedad)
#     return render_template("editar_novedad.html", novedad=novedad, marcas=marcas, subcategorias=subcategorias, tiposNovedad=tiposNovedad)

# @app.route("/actualizar_novedad", methods=["POST"])
# def actualizar_novedad():
#     id = request.form["id"]
#     nombre = request.form["nombre"]
#     titulo = request.form["titulo"]
#     fecha_inicio = request.form["fecha_inicio"]
#     fecha_vencimiento = request.form["fecha_vencimiento"]
#     terminos = request.form["terminos"]
#     disponibilidad = request.form["disponibilidad"]
#     marca_id = request.form["marca_id"]
#     subcategoria_id = request.form["subcategoria_id"]
#     tipo_novedad_id = request.form["tipo_novedad_id"]

#     imagen = request.files["imagen"].read() if "imagen" in request.files else None

#     controlador_novedades.actualizarNovedad(nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id, imagen, id)
#     return redirect("/novedades_listado")

# IMG NOVEDAD

@app.route("/agregar_img_novedad/<int:novedad_id>")
def formulario_agregar_img_novedad(novedad_id):
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("agregar_img_novedad.html", novedad_id=novedad_id, tipos_img_novedad=tipos_img_novedad)

# @app.route("/guardar_img_novedad", methods=["POST"])
# def guardar_img_novedad():
#     novedad_id = request.form["novedad_id"]
#     nom_imagen = request.form["nomImagen"]
#     tipo_img_novedad_id = request.form["tipo_img_novedad"]
    
#     if "imagenes" in request.files:
#         imagenes = request.files.getlist("imagenes")
        
#         for imagen in imagenes:
#             imagen_data = imagen.read()
#             controlador_novedades.insertarImagenNovedad(nom_imagen, imagen_data, tipo_img_novedad_id, novedad_id)
    
#     return redirect("/novedades_listado")

@app.route("/img_novedades_listado/<int:novedad_id>")
def img_novedades_listado(novedad_id):
    img_novedades = controlador_novedades.obtenerImagenesNovedad(novedad_id)
    return render_template("img_novedades_listado.html", img_novedades=img_novedades, novedad_id=novedad_id)

@app.route("/eliminar_img_novedad", methods=["POST"])
def eliminar_img_novedad():
    controlador_novedades.eliminarImagenNovedad(request.form["id"])
    novedad_id = request.form["novedad_id"]
    return redirect(f"/img_novedades_listado/{novedad_id}")

@app.route("/formulario_editar_img_novedad/<int:id>")
def editar_img_novedad(id):
    img_novedad = controlador_novedades.obtenerImagenNovedadPorId(id)
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("editar_img_novedad.html", img_novedad=img_novedad, tipos_img_novedad=tipos_img_novedad)

@app.route("/actualizar_img_novedad", methods=["POST"])
def actualizar_img_novedad():
    id = request.form["id"]
    nom_imagen = request.form["nomImagen"]
    tipo_img_novedad_id = request.form["tipo_img_novedad"]
    
    imagen = request.files["imagen"].read() if "imagen" in request.files else None

    controlador_novedades.actualizarImagenNovedad(nom_imagen, imagen, tipo_img_novedad_id, id)
    novedad_id = request.form["novedad_id"]
    return redirect(f"/img_novedades_listado/{novedad_id}")

#########################FIN NOVEDAD####################################


#########################INICIO DE SESIÓN####################################
#PARA GUARDAR
@app.route("/registrar_cliente", methods=["POST"])
def registrar_cliente():

    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    dni = request.form["dni"]
    genero = request.form["genero"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]
    password = request.form["password"]

    result=controlador_usuario_cliente.insertar_usuario(
        nombres, apellidos, dni, genero, fecha_nacimiento, telefono, correo, password,True
    )
    if(result==1):
        return render_template("iniciar_sesion.html", mostrar=True)
    elif(result==0):
        return render_template("iniciar_sesion.html", mostrar=False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email-login')
        password = request.form.get('password-login')
    return render_template('iniciar_sesion.html')


#####################FIN INICIO DE SESIÓN######################
# EJECUTAR


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
