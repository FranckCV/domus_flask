from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from blueprints.api.utils import response_success, response_error 
from datetime import datetime

from controladores import (
    controlador_caracteristicas,
    controlador_caracteristicas_productos,
    controlador_carrito,
    controlador_contenido_info,
    controlador_cupon,
    controlador_detalle,
    controlador_estado_pedido,
    controlador_imagenes_novedades,
    controlador_imagenes_productos,
    controlador_informacion_domus,
    controlador_lista_deseos,
    controlador_marcas,
    controlador_metodo_pago,
    controlador_motivo_comentario,
    controlador_novedades,
    controlador_pedido,
    controlador_productos,
    controlador_redes_sociales,
    controlador_subcategorias,
    controlador_tipos_img_novedad,
    controlador_tipos_novedad,
    controlador_tipos_usuario,
    controlador_usuario_cliente,
    controlador_categorias,
    controlador_comentario
)

from clases import (
    clsCaracteristica,
    clsCaracteristicaProducto ,
    clsCaracteristicas_subcategoria,
    clsCategoria ,
    clsComentario ,
    clsCupon ,
    clsDetallesPedido ,
    clsEstadoPedido ,
    clsImgNovedad ,
    clsImgProducto ,
    clsInformacionDomus ,
    clsListaDeseos ,
    clsMarca ,
    clsMetodoPago ,
    clsMotivoComentario ,
    clsNovedad ,
    clsPedido ,
    clsProducto ,
    clsRedesSociales ,
    clsSubcategoria ,
    clsTipoImgNovedad,
    clsTipoNovedad ,
    clsTipoUsuario ,
    clsUsuario ,
)


api_v1_bp = Blueprint('api_v1', __name__)



# TEST DE API
@api_v1_bp.route("/api_obtenerdiscos")
@jwt_required()
def api_obtenerdiscos():
    discos = controlador_categorias.obtener_listado_categorias()
    return jsonify(discos)



## MARCAS ##
@api_v1_bp.route("/api_guardar_marca", methods=["POST"])
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



@api_v1_bp.route("/api_listado_marcas")
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

@api_v1_bp.route("/api_listar_marca", methods=["POST"])
@jwt_required()
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



@api_v1_bp.route("/api_eliminar_marca", methods=["POST"])
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


@api_v1_bp.route("/api_actualizar_marca", methods=["POST"])
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
@api_v1_bp.route("/api_listado_productos")
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

@api_v1_bp.route("/api_guardar_producto", methods=["POST"])
@jwt_required()  # Si necesitas autenticación, puedes descomentar esta línea
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


@api_v1_bp.route("/api_eliminar_producto", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_producto", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_producto", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listado_subcategorias")
@jwt_required()
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


@api_v1_bp.route("/api_guardar_subcategoria", methods=["POST"])
@jwt_required()  # Si necesitas autenticación, puedes descomentar esta línea
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



@api_v1_bp.route("/api_eliminar_subcategoria", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_subcategoria", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_subcategoria", methods=["POST"])
@jwt_required()  # Si necesitas autenticación, puedes descomentar esta línea
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
@api_v1_bp.route("/api_guardar_categoria", methods=["POST"])
@jwt_required()  # Descomentar si necesitas autenticación
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


@api_v1_bp.route("/api_listado_categorias")
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_categoria", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_categoria", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_categoria", methods=["POST"])
@jwt_required()  # Si es necesario autenticación, puedes dejarlo habilitado
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
@api_v1_bp.route("/api_guardar_usuario_cliente", methods=["POST"])
@jwt_required()  # Descomentar si necesitas autenticación
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


@api_v1_bp.route("/api_listado_usuarios_clientes")
@jwt_required()
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



@api_v1_bp.route("/api_eliminar_usuario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_usuario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_usuario_cliente", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_guardar_comentario", methods=["POST"])
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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



@api_v1_bp.route("/api_listado_comentarios")
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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


@api_v1_bp.route("/api_eliminar_comentario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_comentario", methods=["POST"])
@jwt_required()
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






############################APIS PEDIDO#############################
@api_v1_bp.route("/api_guardar_pedido", methods=["POST"])
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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

@api_v1_bp.route("/api_actualizar_pedido", methods=["POST"])
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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


@api_v1_bp.route("/api_eliminar_pedido", methods=["POST"])
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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

@api_v1_bp.route("/api_listar_pedidos", methods=["GET"])
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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

@api_v1_bp.route("/api_listar_pedido", methods=["POST"])
@jwt_required()  # Aseguramos que solo usuarios autenticados puedan acceder a esta API
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
@api_v1_bp.route("/api_obtener_detalles_por_usuario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_detalles_por_pedido", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_detalle", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_editar_detalle", methods=["POST"])
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


@api_v1_bp.route('/api_guardar_detalle', methods=['POST'])
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
@api_v1_bp.route("/api_guardar_motivo", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_motivo", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_motivos", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_motivo_por_id", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_motivo", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_guardar_tipo_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_tipo_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_tipos_novedad", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_tipo_novedad_por_id", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_tipo_novedad", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_guardar_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_novedades", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_listar_novedad_por_id", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_novedad", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_insertar_caracteristica_producto", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_caracteristicas_producto", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_caracteristica_producto", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_caracteristica_producto", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_caracteristica_producto", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_insertar_metodo_pago", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_metodos_pago", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_obtener_listado_metodos_pago", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_metodo_pago", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_eliminar_metodo_pago", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_metodo_pago", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_tipos_img_novedad", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_tipo_img_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_insertar_tipo_img_novedad", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_tipo_img_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_tipo_img_novedad", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_todas_imagenes_novedad", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_obtener_imagen_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_insertar_imagen_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_imagen_novedad", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_imagen_novedad", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_estados_pedido", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_obtener_estado_pedido", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_insertar_estado_pedido", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_estado_pedido", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_estado_pedido", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_tipos_usuario", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_tipo_usuario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_insertar_tipo_usuario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_tipo_usuario", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_tipo_usuario", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_caracteristicas", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_caracteristica", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_insertar_caracteristica", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_caracteristica", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_caracteristica", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_redes_sociales", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_obtener_red_social", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_insertar_red_social", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_red_social", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_eliminar_red_social", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_obtener_informacion_domus", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_obtener_informacion_domus_por_id", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_informacion_domus", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_insertar_tipo_contenido_info", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_tipo_contenido_info", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_tipo_contenido_info_por_id", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_tipo_contenido_info", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_tipo_contenido_info", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_insertar_contenido_info", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_contenido_info", methods=["GET"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_contenido_info_por_id", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_actualizar_contenido_info", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_eliminar_contenido_info", methods=["POST"])
@jwt_required()
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
@api_v1_bp.route("/api_insertar_cupon", methods=["POST"])
@jwt_required()
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

@api_v1_bp.route("/api_obtener_cupones", methods=["GET"])
@jwt_required()
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


@api_v1_bp.route("/api_obtener_cupon_por_id", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_actualizar_cupon", methods=["POST"])
@jwt_required()
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


@api_v1_bp.route("/api_eliminar_cupon", methods=["POST"])
@jwt_required()
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

######################APIS IMG_PRODUCTO#####################

@api_v1_bp.route("/api_insertar_img_producto", methods=["POST"])
@jwt_required()
def api_insertar_img_producto():
    dictRespuesta = {}
    try:
        data = request.get_json()
        img_nombre = data.get("img_nombre")
        imagen = data.get("imagen")  # La imagen debe estar en Base64
        imgPrincipal = data.get("imgPrincipal")
        producto_id = data.get("producto_id")

        if not img_nombre or not imagen or imgPrincipal is None or not producto_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (img_nombre, imagen, imgPrincipal, producto_id)"
            return jsonify(dictRespuesta)

        # Crear un objeto de la clase ImgProducto
        img_producto = clsImgProducto(None, img_nombre, imagen, imgPrincipal, producto_id)

        # Insertar la imagen de producto
        controlador_imagenes_productos.insertar_img_producto(img_producto.img_nombre, img_producto.imagen, img_producto.imgPrincipal, img_producto.PRODUCTOid)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imagen de producto insertada con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al insertar imagen de producto: {str(e)}"
    return jsonify(dictRespuesta)


@api_v1_bp.route("/api_obtener_imagenes_por_producto", methods=["POST"])
@jwt_required()
def api_obtener_imagenes_por_producto():
    dictRespuesta = {}
    try:
        data = request.get_json()
        producto_id = data.get("id")

        if not producto_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del producto"
            return jsonify(dictRespuesta)

        # Obtener todas las imágenes de un producto
        imagenes = controlador_imagenes_productos.obtener_imagenes_por_producto(producto_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imágenes obtenidas con éxito"
        dictRespuesta["data"] = imagenes
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener imágenes de producto: {str(e)}"
    return jsonify(dictRespuesta)


@api_v1_bp.route("/api_obtener_imagen_por_id", methods=["POST"])
@jwt_required()
def api_obtener_imagen_por_id():
    dictRespuesta = {}
    try:
        data = request.get_json()
        img_id = data.get("id")

        if not img_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la imagen"
            return jsonify(dictRespuesta)

        # Obtener la imagen de producto por su ID
        imagen = controlador_imagenes_productos.obtener_imagen_por_id(img_id)

        if imagen:
            # Convertir la imagen de bytes a Base64
            imagen_base64 = base64.b64encode(imagen[1]).decode('utf-8')

            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Imagen obtenida con éxito"
            dictRespuesta["data"] = {
                "id": imagen[0],
                "imagen": imagen_base64,  # Imagen en formato Base64
                "producto_id": imagen[2]
            }
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Imagen no encontrada"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener imagen de producto: {str(e)}"

    return jsonify(dictRespuesta)

@api_v1_bp.route("/api_actualizar_img_producto", methods=["POST"])
@jwt_required()
def api_actualizar_img_producto():
    dictRespuesta = {}
    try:
        # Obtener los datos del request
        data = request.get_json()

        # Obtener el ID del producto y la nueva imagen en Base64
        img_id = data.get("id")
        imagen_base64 = data.get("imagen")  # La imagen nueva en Base64

        # Validación de los campos requeridos
        if not img_id or not imagen_base64:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (id, imagen)"
            return jsonify(dictRespuesta)

        # Decodificar la imagen de Base64 a bytes
        imagen_bytes = base64.b64decode(imagen_base64)

        # Crear un objeto de la clase ImgProducto con la imagen en bytes
        img_producto = clsImgProducto(p_id=img_id, p_img_nombre=None, p_imagen=imagen_bytes, p_imgPrincipal=1, p_PRODUCTOid=None)

        # Llamar al controlador para actualizar la imagen
        controlador_imagenes_productos.actualizar_img_producto(img_producto.imagen, img_producto.id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imagen de producto actualizada con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al actualizar imagen de producto: {str(e)}"

    return jsonify(dictRespuesta)


@api_v1_bp.route("/api_eliminar_img_producto", methods=["POST"])
@jwt_required()
def api_eliminar_img_producto():
    dictRespuesta = {}
    try:
        data = request.get_json()
        img_id = data.get("id")

        if not img_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID de la imagen"
            return jsonify(dictRespuesta)

        # Eliminar la imagen de producto
        controlador_imagenes_productos.eliminar_img_producto(img_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Imagen de producto eliminada con éxito"
    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al eliminar imagen de producto: {str(e)}"
    return jsonify(dictRespuesta)


####################FIN APIS IMG_PRODUCTO#####################

#######################APIS LISTA DESEOS#################
@api_v1_bp.route("/api_obtener_lista_deseos", methods=["POST"])
@jwt_required()
def api_obtener_lista_deseos():
    dictRespuesta = {}
    try:
        # Obtener los datos del request
        data = request.get_json()

        # Obtener el ID del usuario
        usuario_id = data.get("id")

        # Validación de los campos requeridos
        if not usuario_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Se requiere el ID del usuario"
            return jsonify(dictRespuesta)

        # Llamar a la función para obtener la lista de deseos
        lista_deseos = controlador_lista_deseos.obtenerListaDeseos(usuario_id)

        if lista_deseos:
            dictRespuesta["status"] = 1
            dictRespuesta["mensaje"] = "Lista de deseos obtenida con éxito"
            dictRespuesta["data"] = [{"id": item[0], "nombre": item[1]} for item in lista_deseos]
        else:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "No se encontraron productos en la lista de deseos"

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al obtener la lista de deseos: {str(e)}"

    return jsonify(dictRespuesta)

@api_v1_bp.route("/api_agregar_quitar_lista_deseos", methods=["POST"])
@jwt_required()
def api_agregar_quitar_lista_deseos():
    dictRespuesta = {}
    try:
        data = request.get_json()

        usuario_id = data.get("usuarioid")
        producto_id = data.get("productoid")

        if not usuario_id or not producto_id:
            dictRespuesta["status"] = 0
            dictRespuesta["mensaje"] = "Faltan campos requeridos (usuarioid, productoid)"
            return jsonify(dictRespuesta)

        controlador_lista_deseos.agregar_a_lista_deseos(usuario_id, producto_id)

        dictRespuesta["status"] = 1
        dictRespuesta["mensaje"] = "Producto agregado o quitado de la lista de deseos con éxito"

    except Exception as e:
        dictRespuesta["status"] = -1
        dictRespuesta["mensaje"] = f"Error al agregar o quitar producto: {str(e)}"

    return jsonify(dictRespuesta)

################FIN APIS LISTA DESEOS################



