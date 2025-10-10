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

api_bp = Blueprint('api', __name__)

# HOMEPAGE
@api_bp.route("/listar_novedades_recientes")
def listar_novedades_recientes():
    discos = controlador_categorias.obtener_listado_categorias()
    return jsonify(discos)



# @api_bp.route("/listar_novedades_recientes")
# def listar_novedades_recientes():
#     discos = controlador_categorias.obtener_listado_categorias()
#     return jsonify(discos)


# @api_bp.route("/listar_novedades_recientes")
# def listar_novedades_recientes():
#     discos = controlador_categorias.obtener_listado_categorias()
#     return jsonify(discos)



# @api_bp.route("/listar_novedades_recientes")
# def listar_novedades_recientes():
#     discos = controlador_categorias.obtener_listado_categorias()
#     return jsonify(discos)
