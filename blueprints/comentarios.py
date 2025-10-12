from flask import Blueprint, render_template, request, redirect , session , jsonify , url_for
from controladores import (
    controlador_categorias,
    controlador_marcas,
    controlador_pedido,
    controlador_productos,
    controlador_novedades ,
    controlador_detalle ,
    controlador_carrito ,
    controlador_metodo_pago
)

from settings import cupon
from datetime import datetime , time , date

comentarios_bp = Blueprint('comnetarios', __name__)


