from flask import Flask, render_template, request, redirect, flash, jsonify
import controlador_marcas
import controlador_categorias
import controlador_productos
import controlador_imagenes_productos
import controlador_imagenes_novedades
import controlador_caracteristicas_productos
import controlador_subcategorias

app = Flask(__name__)

@app.context_processor
def inject_globals():
    categoriasMenu = controlador_categorias.obtener_categorias()
    marcasMenu = controlador_marcas.obtener_marcas_menu(10) 
    logo_foto = 'img/elementos/logoDomus.png'
    return dict(marcasMenu=marcasMenu , logo_foto = logo_foto , categoriasMenu = categoriasMenu)


# PAGINAS GENERALES

@app.route("/") #falta
def index():
    productos = controlador_productos.obtenerEnTarjetasMasRecientes()
    marcasBloque = controlador_marcas.obtener_marcas_index(2,10)
    return render_template("index.html", marcasBloque = marcasBloque , productos = productos)


@app.route("/marcas") #falta
def marcas():
    marcas = controlador_marcas.obtener_marcas()
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
    return render_template("novedades.html")



@app.route("/promociones") #falta
def promociones():
    return render_template("promociones.html")




# PAGINAS ESPECIFICAS

@app.route("/selectedCategoria=<int:id>")  #falta
def categoria(id):
    categoria = controlador_categorias.obtener_categoria_por_id(id)
    subcategorias = controlador_subcategorias.obtenerSubcategoriasXCategoria(id)
    return render_template("categoria.html", categoria = categoria, subcategorias = subcategorias)


@app.route("/selectedMarca=<int:id>")  #falta
def marca(id):
    marca = controlador_marcas.obtener_marca_por_id(id)
    
    return render_template("marca.html", marca = marca)


@app.route("/selectedProducto=<int:id>")  #falta
def producto(id):
    producto = controlador_productos.obtener_por_id(id)
    marca = controlador_marcas.obtener_marca_por_id(producto[9])
    imgs_producto = controlador_imagenes_productos.obtener_imagenes_por_producto(producto[0])
    caracteristicasPrincipales = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,1)
    caracteristicasSecundarias = controlador_caracteristicas_productos.obtenerCaracteristicasxProducto(id,0)
    return render_template("selectedProducto.html" , producto = producto , marca = marca, imgs_producto = imgs_producto, caracteristicasPrincipales = caracteristicasPrincipales, caracteristicasSecundarias = caracteristicasSecundarias)


@app.route("/selectedNovedad?<int:tipo_id>=<int:id>")  #falta
def novedad(id,tipo_id):
    if tipo_id == 3:
        return render_template("promocionSelect.html")
    else:
        return redirect("/novedades")





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
    return render_template("carrito.html")






# PAGINAS USUARIO EMPLEADO




# PAGINAS USUARIO ADMINISTRADOR







# EJECUTAR

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
