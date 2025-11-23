from flask import Blueprint, current_app, request, jsonify
from blueprints.api.utils import response_success, response_error
from datetime import datetime
from utils import encstringsha256
import os
from werkzeug.utils import secure_filename

from controladores import (
    controlador_marcas,
    controlador_novedades,
    controlador_pedido,
    controlador_productos,
    controlador_usuario_cliente,
    controlador_lista_deseos,
    controlador_categorias,
    controlador_metodo_pago,
    controlador_subcategorias ,
)

api_bp = Blueprint('api', __name__)


# GET
@api_bp.route("/homepage")
def homepage():
    try:
        usuario_id = request.args.get("usuario_id")

        marcas = controlador_marcas.get_marcas_recientes()
        categorias = controlador_categorias.obtener_categorias_disponibles()
        novedades = controlador_novedades.get_banners_recientes()
        p_recientes = controlador_productos.get_productos_recientes(usuario_id)
        p_populares = controlador_productos.get_productos_populares(usuario_id)

        msg = 'Datos para homepage mostrados exitosamente'
        data = {
            "productos_recientes" : p_recientes ,
            "productos_populares" : p_populares ,
            "novedades" : novedades ,
            "marcas" : marcas ,
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
        rutas = controlador_productos.get_img_producto_pr_id(producto_id)
        producto['rutas'] = rutas

        msg = 'Datos de producto mostrados exitosamente'
        data = producto

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/consultar_usuario")
def consultar_usuario():
    try:
        usuario_id = request.args.get("usuario_id", type=int)

        lista_deseos = controlador_productos.get_productos_lista_deseos(usuario_id)
        lista_pedidos = controlador_pedido.get_pedidos_usuario_id(usuario_id)

        data = {
            "lista_deseos": lista_deseos,
            "lista_pedidos": lista_pedidos
        }

        return response_success("Datos de usuario mostrados exitosamente", data)

    except Exception as e:
        return response_error(str(e))



@api_bp.route("/consultar_pedido")
def consultar_pedido():
    try:
        pedido_id = request.args.get("pedido_id")

        pedido = controlador_pedido.get_pedido_id(pedido_id) or {}
        productos = controlador_productos.get_productos_pedido(pedido_id)
        pedido['productos'] = productos
        pedido['cantidad'] = len(productos)

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


@api_bp.route("/listar_favoritos")
def listar_favoritos():
    try:
        usuario_id = request.args.get("usuario_id")

        lista_deseos = controlador_productos.get_productos_lista_deseos(usuario_id)

        msg = f'Lista de favoritos de usuario {usuario_id} mostrados exitosamente'
        data = {
            'lista' : lista_deseos
        }

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


# @api_bp.route("/registrar_usuario",methods = ['POST'])
# def registrar_usuario():
#     try:
#         body = request.json.get('body_request',{})

#         nombres = body.get("nombres")
#         apellidos = body.get("apellidos")
#         doc_identidad = body.get("doc_identidad")
#         genero = body.get("genero")
#         telefono = body.get("telefono")
#         correo = body.get("correo")
#         contrasenia = body.get("contrasenia")

#         usuario_id = controlador_usuario_cliente.register_usuario_cliente(nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia)
#         if usuario_id == 0:
#             msg = 'Error al resgistrar usuario'
#             data = { 'usuario_id' : usuario_id }
#         else:
#             msg = 'Usuario registrado exitosamente'
#             data = { 'usuario_id' : usuario_id }

#         return response_success(msg,data)
#     except Exception as e:
#         return response_error(str(e))


@api_bp.route("/agregar_producto_carrito",methods = ['POST'])
def agregar_producto_carrito():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")
        val_cart = controlador_pedido.get_carrito_usuarioid(usuario_id)
        if val_cart:
            carrito_id = val_cart['id']
        else:
            carrito_id = controlador_pedido.insert_new_pedido_carrito(usuario_id)

        det = controlador_pedido.get_detalle_pedido(carrito_id,producto_id)
        pro = controlador_productos.get_producto(usuario_id,producto_id)
        if det:
            if det['cantidad'] + 1 > pro['stock']:
                msg = 'No hay más stock disponible'
            else:
                controlador_pedido.update_plus_detalles_pedido(producto_id, carrito_id)
                msg = 'Producto aumentado en el carrito'
        else:
            if pro['stock'] >= 1:
                controlador_pedido.insert_detalles_pedido(producto_id, carrito_id, 1)
                msg = 'Producto agregado al carrito'
            else:
                msg = 'No hay más stock disponible'
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


@api_bp.route("/aumentar_producto_carrito",methods = ['POST'])
def aumentar_producto_carrito():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")

        carrito_id = controlador_pedido.get_carrito_usuarioid(usuario_id)['id']
        controlador_pedido.update_plus_detalles_pedido(producto_id, carrito_id)

        msg = 'Producto aumentado en el carrito exitosamente'
        data = {}

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/disminuir_producto_carrito",methods = ['POST'])
def disminuir_producto_carrito():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        producto_id = body.get("producto_id")

        carrito_id = controlador_pedido.get_carrito_usuarioid(usuario_id)['id']
        det = controlador_pedido.get_detalle_pedido(carrito_id,producto_id)
        if det and det.get('cantidad',0)==1:
            controlador_pedido.delete_detalles_pedido(producto_id,carrito_id)
        else:
            controlador_pedido.update_minus_detalles_pedido(producto_id, carrito_id)

        msg = 'Producto disminuido en el carrito exitosamente'
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


@api_bp.route("/agregar_producto", methods=['POST'])
def agregar_producto():
    try:
        body = request.form.get('body_request')
        if body:
            import json
            body = json.loads(body)
        else:
            body = {}

        nombre = body.get('nombre')
        price_regular = body.get('price_regular')
        precio_online = body.get('precio_online')
        precio_oferta = body.get('precio_oferta')
        info_adicional = body.get('info_adicional')
        stock = body.get('stock')
        disponibilidad = body.get('disponibilidad')
        marcaid = body.get('marcaid')
        subcategoriaid = body.get('subcategoriaid')

        if not nombre or not precio_online or not stock:
            return response_error("Faltan campos obligatorios: nombre, precio_online o stock")

        file = request.files.get('imagen')
        if not file:
            return response_error("No se ha enviado ninguna imagen")

        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if not allowed_file(file.filename):
            return response_error("Formato de imagen no permitido")

        upload_folder = os.path.join(current_app.root_path, 'static', 'img')
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        path_guardado = os.path.join(upload_folder, filename)
        file.save(path_guardado)

        ruta_relativa = f"/static/img/{filename}"

        import bd
        conn = bd.obtener_conexion()
        cursor = conn.cursor()

        sql_producto = """INSERT INTO producto
            (nombre, price_regular, precio_online, precio_oferta, info_adicional, stock, disponibilidad, marcaid, subcategoriaid)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values_producto = (nombre, price_regular, precio_online, precio_oferta,
                            info_adicional, stock, disponibilidad, marcaid, subcategoriaid)
        cursor.execute(sql_producto, values_producto)
        conn.commit()
        productoid = cursor.lastrowid

        sql_img = """INSERT INTO img_producto (img_nombre, imagen, imgprincipal, productoid)
                        VALUES (%s,%s,%s,%s)"""
        cursor.execute(sql_img, (filename, ruta_relativa, 1, productoid))
        conn.commit()

        cursor.close()
        conn.close()

        msg = "Producto agregado correctamente"
        data = {
            "producto_id": productoid,
            "imagen_guardada": ruta_relativa
        }

        return response_success(msg, data)

    except Exception as e:
        return response_error(str(e))


@api_bp.route("/login_movil", methods=['POST'])
def login_movil():
    try:
        body = request.json.get('body_request', {})

        correo = body.get("correo")
        contrasenia = body.get("contrasenia")

        if not correo or not contrasenia:
            return response_error("Debe proporcionar correo y contraseña")

        usuario = controlador_usuario_cliente.get_usuario_correo(correo)

        if not usuario:
            return response_error("Usuario no válido. Si es cliente, regístrese.")

        epassword = encstringsha256(contrasenia)

        stored_password = usuario.get("contrasenia")

        if epassword == stored_password:
            msg = "Inicio de sesión exitoso"
            data = {
                "id": usuario.get("id"),
                "nombre": usuario.get("nombres"),
                "correo": usuario.get("correo")
            }
            return response_success(msg, data)
        else:
            return response_error("Contraseña incorrecta.")

    except Exception as e:
        return response_error(str(e))



##########################No tocar, sticth trabajando##############################################

@api_bp.route("/metodos_pago", methods=["GET"])
def listar_metodos_pago():
    try:
        data = controlador_metodo_pago.obtener_metodo_pago()
        msg = "Métodos listados"
        return response_success(msg, data)
    except Exception as e:
        return response_error(str(e))




@api_bp.route("/procesar_pago",methods = ['POST'])
def procesar_pago():
    try:
        body = request.json.get('body_request',{})

        usuario_id = body.get("usuario_id")
        pedido = controlador_pedido.get_carrito_usuarioid(usuario_id)

        # if pedido:
        pedido_id = pedido['id']
        controlador_pedido.update_pedido_set_estado(pedido_id, 2)
        carrito_pagado = controlador_pedido.get_pedido_id(pedido_id)
        # if carrito_pagado and carrito_pagado['estado_pedidoid'] == 2:
        controlador_pedido.insert_new_pedido_carrito(usuario_id)
        msg = 'Pedido en carrito pagado exitosamente'
            # else:
                # msg = 'Error al pagar pedido en carrito'
        # else:
            # msg = 'Error al encontrar pedido en carrito'
        data = {
            "pedido_id": pedido_id
        }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))




@api_bp.route("/procesar_pago_carrito", methods=["POST"])
def procesar_pago_carrito():
    try:
        body = request.json.get("body_request", {})

        metodo_pago_id = body.get("metodo_pago_id")
        subtotal = body.get("subtotal")
        pedido_id =  body.get("pedido_id")

        # 2. ACTUALIZAR A PAGADO
        ok = controlador_pedido.actualizar_pedido_pagado(
            pedido_id,
            metodo_pago_id,
            subtotal
        )

        if not ok:
            return response_error("No se pudo actualizar el pedido")

        # 3. RESPUESTA FINAL
        ped = controlador_pedido.get_pedido_id(pedido_id)
        usuario_id = ped['usuarioid']
        cart_id = controlador_pedido.insert_new_pedido_carrito(usuario_id)

        data = {"pedido_id": pedido_id}
        return response_success("Pago procesado correctamente", data)

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




