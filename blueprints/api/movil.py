from flask import Blueprint, request, jsonify
from blueprints.api.utils import response_success, response_error 
from datetime import datetime
from utils import encstringsha256

from controladores import (
    controlador_marcas,
    controlador_novedades,
    controlador_pedido,
    controlador_productos,
    controlador_subcategorias,
    controlador_usuario_cliente,
    controlador_lista_deseos,
    controlador_categorias,
)

api_bp = Blueprint('api', __name__)


# GET
@api_bp.route("/homepage")
def homepage():
    try:
        usuario_id = request.args.get("usuario_id")

        novedades = controlador_novedades.get_banners_recientes()
        marcas = controlador_marcas.get_marcas_recientes()
        p_recientes = controlador_productos.get_productos_recientes(usuario_id)
        p_populares = controlador_productos.get_productos_populares(usuario_id)
        categorias = controlador_categorias.obtener_categorias_disponibles()
        
        msg = 'Datos para homepage mostrados exitosamente'
        data = {
            "productos_recientes" : p_recientes ,
            "productos_populares" : p_populares ,
            "marcas" : marcas ,
            "novedades" : novedades ,
            "categorias" : categorias ,
        }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/consultar_producto")
def consultar_producto():
    try:
        usuario_id = request.args.get("usuario_id")
        producto_id = request.args.get("producto_id")

        producto = controlador_productos.get_producto(usuario_id,producto_id)
        rutas = []
        producto['rutas'] = rutas
        
        msg = 'Datos de producto mostrados exitosamente'
        data = producto

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/consultar_usuario")
def consultar_usuario():
    try:
        usuario_id = request.args.get("usuario_id")

        usuario = controlador_usuario_cliente.get_usuario_id(usuario_id)
        lista_deseos = controlador_productos.get_productos_lista_deseos(usuario_id)
        usuario['lista_deseos'] = lista_deseos
        
        msg = 'Datos de usuario mostrados exitosamente'
        data = usuario

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/consultar_pedido")
def consultar_pedido():
    try:
        pedido_id = request.args.get("pedido_id")

        pedido = controlador_pedido.get_pedido_id(pedido_id) or {}
        productos = controlador_productos.get_productos_pedido(pedido_id)
        pedido['productos'] = productos

        msg = 'Datos de pedido mostrados exitosamente'
        data = pedido

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/consultar_carrito")
def consultar_carrito():
    try:
        """
        crear funcion
        """
        usuario_id = request.args.get("usuario_id")
        
        carrito = controlador_pedido.get_carrito_usuarioid(usuario_id)
        productos = controlador_productos.get_productos_pedido(carrito['id'])
        carrito['productos'] = productos
         
        msg = 'Datos de carrito mostrados exitosamente'
        data = carrito

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/listar_pedidos")
def listar_pedidos():
    try:
        usuario_id = request.args.get("usuario_id")

        pedidos = controlador_pedido.get_pedidos_usuario_id(usuario_id)
        
        msg = f'Pedidos de usuario {usuario_id} mostrados exitosamente'
        data = pedidos

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))



# POST

@api_bp.route("/cambiar_contrasenia",methods = ['POST'])
def cambiar_contrasenia():
    try:
        """
        crear funcion
        """
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        contrasenia_actual = body.get("contrasenia_actual")
        contrasenia_nueva = body.get("contrasenia_nueva")

        rpta = controlador_usuario_cliente.change_password(usuario_id,contrasenia_actual,contrasenia_nueva)
        
        msg = 'Contraseña cambiada exitosamente'
        data = {'rpta':rpta }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/editar_perfil",methods = ['POST'])
def editar_perfil():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        nombres = body.get("nombres")
        apellidos = body.get("apellidos")
        doc_identidad = body.get("doc_identidad")
        genero = body.get("genero")
        telefono = body.get("telefono")
        correo = body.get("correo")
        
        controlador_usuario_cliente.update_perfil(usuario_id, nombres, apellidos , doc_identidad , genero, telefono , correo)

        msg = 'Perfil modificado exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/loguear_usuario",methods = ['POST'])
def loguear_usuario():
    try:
        body = request.json.get('body_request',{})

        correo = body.get("correo")
        contrasenia = body.get("contrasenia")

        usuario = controlador_usuario_cliente.get_usuario_correo(correo)
        encpassword = encstringsha256(contrasenia)
        if usuario and encpassword == usuario['contrasenia']:
            msg = 'Inicio de sesión exitoso'
            data = {}
        else:
            msg = 'Credenciales incorrectas'
            data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/registrar_usuario",methods = ['POST'])
def registrar_usuario():
    try:
        body = request.json.get('body_request',{})

        nombres = body.get("nombres")
        apellidos = body.get("apellidos")
        doc_identidad = body.get("doc_identidad")
        genero = body.get("genero")
        telefono = body.get("telefono")
        correo = body.get("correo")
        contrasenia = body.get("contrasenia")
        
        usuario_id = controlador_usuario_cliente.register_usuario_cliente(nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia)
        if usuario_id == 0:
            msg = 'Error al resgistrar usuario'
            data = { 'usuario_id' : usuario_id }
        else: 
            msg = 'Usuario registrado exitosamente'
            data = { 'usuario_id' : usuario_id }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/agregar_producto_carrito",methods = ['POST'])
def agregar_producto_carrito():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")
        cantidad = body.get("cantidad")
        
        carrito_id = controlador_pedido.get_carrito_usuarioid(usuario_id)['id']
        controlador_pedido.insert_detalles_pedido(producto_id, carrito_id, cantidad)

        msg = 'Producto agregado al carrito exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/modificar_producto_carrito",methods = ['POST'])
def modificar_producto_carrito():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")
        cantidad = body.get("cantidad")
        
        carrito_id = controlador_pedido.get_carrito_usuarioid(usuario_id)['id']
        controlador_pedido.update_detalles_pedido(producto_id, carrito_id, cantidad)

        msg = 'Producto modificado en el carrito exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/eliminar_producto_carrito",methods = ['POST'])
def eliminar_producto_carrito():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")

        carrito_id = controlador_pedido.get_carrito_usuarioid(usuario_id)['id']
        controlador_pedido.delete_detalles_pedido(producto_id,carrito_id)

        msg = 'Producto eliminado en el carrito exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/eliminar_producto_lista_deseos",methods = ['POST'])
def eliminar_producto_lista_deseos():
    try:
        """
        crear funcion
        """
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")
        
        controlador_lista_deseos.delete_lista_deseos(producto_id,usuario_id)

        msg = 'Producto eliminado de la lista de desesos exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/agregar_producto_lista_deseos",methods = ['POST'])
def agregar_producto_lista_deseos():
    try:
        """
        crear funcion
        """
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")
        
        controlador_lista_deseos.insert_lista_deseos(producto_id,usuario_id)

        msg = 'Producto agregado de la lista de desesos exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/busqueda_catalogo",methods=['POST'])
def busqueda_catalogo():
    try:
        body = request.json.get('body_request',{})

        usuarioid = body.get("usuarioid")
        busqueda = body.get("busqueda")
        orden = body.get("orden")
        categoria = body.get("categoria")
        subcategoria = body.get("subcategoria")
        precio_max = body.get("precio_max")
        precio_min = body.get("precio_min")

        productos = controlador_productos.get_productos_catalogo(
            usuarioid,
            busqueda,
            orden,
            categoria,
            subcategoria,
            precio_max,
            precio_min
        )
        
        categorias = controlador_categorias.obtener_categorias_disponibles()

        msg = 'Resultados de busqueda mostrados exitosamente'
        data = {
            "lista" : productos ,
            "categorias" : categorias ,
        }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))

@api_bp.route("/comboboxes",methods=['POST'])
def comboboxes():
    try:
        body = request.json.get('body_request',{})

        categorias = controlador_categorias.obtener_categorias_disponibles()
        subcategorias = controlador_subcategorias.obtener_subcategorias()
        marcas = controlador_productos.obtener_marcas_disponibles()

        msg = 'Comboboxes obtenidos exitosamente'
        data = {
            "categorias" : categorias,
            "subcategorias" : subcategorias,
            "marcas" : marcas
        }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))

