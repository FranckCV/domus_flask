from flask import Blueprint, current_app, request, jsonify, send_file
from blueprints.api.utils import response_success, response_error
from datetime import datetime
from utils import encstringsha256
import os
import requests
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
    controlador_comprobante,
    controlador_informacion_domus
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


# @api_bp.route("/consultar_usuario")
# def consultar_usuario():
#     try:
#         usuario_id = request.args.get("usuario_id", type=int)

#         lista_deseos = controlador_productos.get_productos_lista_deseos(usuario_id)
#         lista_pedidos = controlador_pedido.get_pedidos_usuario_id(usuario_id)

#         data = {
#             "lista_deseos": lista_deseos,
#             "lista_pedidos": lista_pedidos
#         }

#         return response_success("Datos de usuario mostrados exitosamente", data)

#     except Exception as e:
#         return response_error(str(e))

@api_bp.route("/consultar_usuario")
def consultar_usuario():
    try:
        usuario_id = request.args.get("usuario_id", type=int)

        usuario = controlador_usuario_cliente.get_usuario_id(usuario_id)
        # lista_deseos = controlador_productos.get_productos_lista_deseos(usuario_id)
        # lista_pedidos = controlador_pedido.get_pedidos_usuario_id(usuario_id)

        # data = {
        #     "lista_deseos": lista_deseos,
        #     "lista_pedidos": lista_pedidos,
        #     "usuario" : usuario
        # }

        return response_success("Datos de usuario mostrados exitosamente", usuario)

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
        #genero = body.get("genero")
        telefono = body.get("telefono")
        fecha_nacimiento = body.get("fecha_nacimiento")

        controlador_usuario_cliente.update_perfil(
            usuario_id,
            nombres,
            apellidos,
            doc_identidad,
            telefono,
            fecha_nacimiento
        )

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
        pedido_id = body.get("pedido_id")

        card_nro =  body.get("card_nro",None)
        card_mmaa =  body.get("card_mmaa",None)
        card_titular =  body.get("card_titular",None)

        # 2. ACTUALIZAR A PAGADO
        ok = controlador_pedido.actualizar_pedido_pagado(
            pedido_id,
            metodo_pago_id,
            card_nro ,
            card_mmaa ,
            card_titular 
        )

        if not ok:
            return response_error("No se pudo actualizar el pedido")

        # 3. GENERAR COMPROBANTE AUTOMÁTICAMENTE
        try:
            
            # Datos del comprobante desde el body
            tipo_comprobante = body.get("tipo_comprobante", "boleta")
            
            # Datos del cliente
            datos_cliente = {
                'nombre_completo': body.get("nombre_completo", "Cliente"),
                'doc_identidad': body.get("doc_identidad", "00000000"),
                'tipo_doc': body.get("tipo_doc", "DNI"),
            }
            
            if tipo_comprobante == 'factura':
                datos_cliente['razon_social'] = body.get("razon_social")
                datos_cliente['ruc'] = body.get("ruc")
                datos_cliente['direccion'] = body.get("direccion")
            
            # Obtener productos del pedido
            productos_pedido = controlador_productos.get_productos_pedido(pedido_id)
            
            datos_productos = []
            for prod in productos_pedido:
                datos_productos.append({
                    'cantidad': prod['cantidad'],
                    'nombre': prod['nombre'],
                    'precio_unitario': prod['precio'],
                    'precio_oferta': prod['oferta'],
                    'total': prod['cantidad'] * prod['precio']
                })
            
            # Datos de la empresa
            datos_empresa = {
                'correo': 'contacto@domusmarket.com',
                'telefono': '(01) 234-5678',
                'ruc': '20123456789',
                'direccion': 'Av. En tu corazón 123, Chiclayork, Perú'
            }
            
            # Generar PDF del comprobante (retorna solo el nombre del archivo)
            nombre_archivo = controlador_comprobante.generar_pdf_comprobante(
                pedidoid=pedido_id,
                tipo_comprobante=tipo_comprobante,
                datos_cliente=datos_cliente,
                datos_productos=datos_productos,
                datos_empresa=datos_empresa
            )
            
            # Construir ruta completa para la respuesta
            ruta_completa = controlador_comprobante.obtener_ruta_completa_comprobante(pedido_id, nombre_archivo)
            
            comprobante_generado = True
            ruta_comprobante = ruta_completa
            
        except Exception as e_comp:
            print(f"Error al generar comprobante: {e_comp}")
            import traceback
            traceback.print_exc()
            comprobante_generado = False
            ruta_comprobante = None

        # 4. RESPUESTA FINAL
        ped = controlador_pedido.get_pedido_id(pedido_id)
        usuario_id = ped['usuarioid']

        val_cart = controlador_pedido.get_carrito_usuarioid(usuario_id)
        if not val_cart:
            cart_id = controlador_pedido.insert_new_pedido_carrito(usuario_id)

        data = {
            "pedido_id": pedido_id,
            "comprobante_generado": comprobante_generado,
            "ruta_comprobante": ruta_comprobante,
            "nombre_archivo": nombre_archivo if comprobante_generado else None
        }
        
        return response_success("Pago procesado correctamente", data)

    except Exception as e:
        return response_error(str(e))


@api_bp.route("/descargar_comprobante/<int:pedido_id>", methods=['GET'])
def descargar_comprobante(pedido_id):
    try:
        comprobante = controlador_comprobante.obtener_comprobante_por_pedido(pedido_id)
        
        if not comprobante:
            return response_error("Comprobante no encontrado")
        
        # Construir ruta completa usando la constante
        nombre_archivo = comprobante['ruta_archivo']  # Ahora solo tiene el nombre
        ruta_completa = controlador_comprobante.obtener_ruta_completa_comprobante(pedido_id, nombre_archivo)
        
        if not os.path.exists(ruta_completa):
            return response_error("Archivo no encontrado")
        
        return send_file(
            ruta_completa,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return response_error(str(e))


@api_bp.route("/consultar_documento", methods=['POST'])
def consultar_documento():
    """
    Consulta información de DNI o RUC usando API alternativa gratuita
    
    Body request:
    {
        "body_request": {
            "tipo_documento": "dni" | "ruc",
            "numero_documento": "12345678" | "20123456789"
        }
    }
    
    Response:
    - Para DNI: nombre_completo
    - Para RUC: razon_social, direccion
    """
    try:
        body = request.json.get('body_request', {})
        
        tipo_documento = body.get("tipo_documento", "").lower()
        numero_documento = body.get("numero_documento", "")
        
        if not tipo_documento or not numero_documento:
            return response_error("Debe proporcionar tipo_documento y numero_documento")
        
        if tipo_documento not in ['dni', 'ruc']:
            return response_error("tipo_documento debe ser 'dni' o 'ruc'")
        
        # Validar longitud según tipo
        if tipo_documento == 'dni' and len(numero_documento) != 8:
            return response_error("El DNI debe tener 8 dígitos")
        
        if tipo_documento == 'ruc' and len(numero_documento) != 11:
            return response_error("El RUC debe tener 11 dígitos")
        
        # ============================================
        # API DNI-RUC (Gratuita)
        # ============================================
        
        if tipo_documento == 'dni':
            # API gratuita para DNI
            url = f"https://dniruc.apisperu.com/api/v1/dni/{numero_documento}"
            
            try:
                response_api = requests.get(url, timeout=15, params={"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InBlcmV6ZGowOTA0QGdtYWlsLmNvbSJ9.8rz9gE8oTMuGHoGvePcZA50zZjUDMph_jVX3PK8npWc"})
                
                if response_api.status_code == 200:
                    data_api = response_api.json()
                    
                    # Verificar si hay éxito
                    if data_api.get("success", False):
                        # Extraer nombres y apellidos
                        nombres = data_api.get("nombres", "")
                        apellido_paterno = data_api.get("apellidoPaterno", "")
                        apellido_materno = data_api.get("apellidoMaterno", "")
                        
                        nombre_completo = f"{nombres} {apellido_paterno} {apellido_materno}".strip()
                        
                        msg = "Consulta DNI exitosa"
                        data = {
                            "tipo_documento": "dni",
                            "numero_documento": numero_documento,
                            "nombre_completo": nombre_completo,
                            "nombres": nombres,
                            "apellido_paterno": apellido_paterno,
                            "apellido_materno": apellido_materno
                        }
                        
                        return response_success(msg, data)
                    else:
                        # Log de depuración
                        print(f"DNI API Response: {data_api}")
                        mensaje_error = data_api.get("message", "DNI no encontrado o inválido")
                        return response_error(f"DNI no encontrado: {mensaje_error}")
                else:
                    return response_error(f"Error al consultar DNI: Código {response_api.status_code}")
            
            except requests.Timeout:
                return response_error("Tiempo de espera agotado al consultar DNI")
            except requests.RequestException as e:
                return response_error(f"Error de conexión al consultar DNI: {str(e)}")
        
        elif tipo_documento == 'ruc':
            # API gratuita para RUC
            url = f"https://dniruc.apisperu.com/api/v1/ruc/{numero_documento}"
            
            try:
                response_api = requests.get(url, timeout=15, params={"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InBlcmV6ZGowOTA0QGdtYWlsLmNvbSJ9.8rz9gE8oTMuGHoGvePcZA50zZjUDMph_jVX3PK8npWc"})
                
                print(f"RUC API Status: {response_api.status_code}")
                
                if response_api.status_code == 200:
                    data_api = response_api.json()
                    
                    # Log completo de la respuesta para debug
                    print(f"RUC API Response: {data_api}")
                    
                    # Verificar si hay éxito
                    if data_api.get("success", False):
                        # Extraer datos de la empresa
                        razon_social = data_api.get("razonSocial", "") or data_api.get("nombre", "")
                        direccion = data_api.get("direccion", "")
                        estado = data_api.get("estado", "")
                        condicion = data_api.get("condicion", "")
                        
                        msg = "Consulta RUC exitosa"
                        data = {
                            "tipo_documento": "ruc",
                            "numero_documento": numero_documento,
                            "razon_social": razon_social,
                            "direccion": direccion,
                            "estado": estado,
                            "condicion": condicion
                        }
                        
                        return response_success(msg, data)
                    else:
                        # Extraer mensaje de error de la API
                        mensaje_error = data_api.get("message", "No se encontró información")
                        
                        # Si la API dice que no encontró, intentar extraer lo que sí viene
                        if data_api.get("razonSocial") or data_api.get("nombre"):
                            # Aunque diga success=false, a veces trae datos
                            razon_social = data_api.get("razonSocial", "") or data_api.get("nombre", "")
                            direccion = data_api.get("direccion", "")
                            estado = data_api.get("estado", "")
                            condicion = data_api.get("condicion", "")
                            
                            msg = "Consulta RUC exitosa (con advertencia)"
                            data = {
                                "tipo_documento": "ruc",
                                "numero_documento": numero_documento,
                                "razon_social": razon_social,
                                "direccion": direccion,
                                "estado": estado,
                                "condicion": condicion
                            }
                            
                            return response_success(msg, data)
                        else:
                            return response_error(f"RUC no encontrado: {mensaje_error}. Verifique que el número sea correcto.")
                else:
                    return response_error(f"Error al consultar RUC: Código {response_api.status_code}")
            
            except requests.Timeout:
                return response_error("Tiempo de espera agotado al consultar RUC")
            except requests.RequestException as e:
                return response_error(f"Error de conexión al consultar RUC: {str(e)}")
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return response_error(f"Error al consultar documento: {str(e)}")



UPLOAD_FOLDER = "/home/DomusMarket/mysite/static/img/img_usuario"
ALLOWED = {"jpg", "jpeg", "png", "webp", "gif"}

def allowed_ext(filename):
    return filename.split('.')[-1].lower() in ALLOWED

def get_extension_from_url(url):
    """Extrae la extensión de una URL"""
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1].lower().replace('.', '')
    return ext if ext in ALLOWED else None

@api_bp.route("/cambiar_foto_perfil", methods=["POST"])
def cambiar_foto_perfil():
    try:
        usuario_id = request.form.get("usuario_id")
        url = request.form.get("url", "").strip()
        saved_path = None

        if not usuario_id:
            return response_error("Falta el parámetro usuario_id")

        # == 1) QUITAR FOTO (url vacía y sin archivo) ==
        if "file" not in request.files and url == "":
            # Guardar NULL en la BD
            controlador_usuario_cliente.update_img_usuario(None, usuario_id)
            return response_success("Foto de perfil eliminada", {"img": None})

        # == 2) SUBIR DESDE GALERÍA ==
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename and allowed_ext(file.filename):
                original_filename = secure_filename(file.filename)
                name_without_ext = os.path.splitext(original_filename)[0]
                extension = os.path.splitext(original_filename)[1]

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                newname = f"user_{usuario_id}_{name_without_ext}_{timestamp}{extension}"
                fullpath = os.path.join(UPLOAD_FOLDER, newname)

                file.save(fullpath)
                saved_path = f"/static/img/img_usuario/{newname}"

        # == 3) GUARDAR URL EXTERNA (NO DESCARGAR) ==
        elif url != "":
            saved_path = url

        # Si se generó saved_path, actualizar en BD
        if saved_path is not None:
            controlador_usuario_cliente.update_img_usuario(saved_path, usuario_id)

        return response_success("Foto de perfil modificada", {"img": saved_path})

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
