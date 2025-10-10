from flask import Blueprint, render_template, request, redirect, session, make_response , url_for
from controladores import (
    controlador_usuario_cliente ,
    controlador_metodo_pago ,
    controlador_estado_pedido ,
    controlador_pedido ,
    controlador_detalle ,
)

pedidos_bp = Blueprint('pedido', __name__)


@pedidos_bp.route("/pedidos=<int:user_id>")
def pedidos(user_id):
    usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    img = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)
    pedidos = controlador_pedido.obtener_listado_pedidos_usuario_fecha_id(user_id)
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()

    return render_template("misPedidos.html", user_id=user_id, usuario=usuario, img=img , pedidos = pedidos , metodos = metodos)


@pedidos_bp.route("/ver_detalle_pedido=<int:id>")
def ver_detalle_pedido(id):
    detalles = controlador_detalle.obtener_listado_detalle_por_id_pedido(id)
    pedido = controlador_pedido.obtener_pedido_id(id)
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_detalle_pedido.html", detalles=detalles , pedido_id=id , pedido = pedido , estados = estados , metodos = metodos)



@pedidos_bp.route("/listado_pedidos")
def pedido():
    pedidos=controlador_pedido.obtener_listado_pedidos()
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_pedidos.html", pedidos = pedidos , estados = estados , metodos = metodos)


@pedidos_bp.route("/listado_pedidos_buscar")
def pedido_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    pedidos = controlador_pedido.buscar_listado_pedidos_usuario(nombreBusqueda)
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_pedidos.html", pedidos = pedidos , estados = estados , metodos = metodos , nombreBusqueda = nombreBusqueda)


@pedidos_bp.route("/eliminar_pedido", methods=["POST"])
def eliminar_pedido():
    id = request.form["id"]
    result=controlador_pedido.buscar_pedido_por_id(id)

    if result:
        return render_template("listado_pedidos.html", error="El pedido tiene detalles asociados y no se puede eliminar. Redirigiendo...", show_modal=True)
    else:
        controlador_pedido.eliminar_pedido(id)
        return redirect("/listado_pedidos")


@pedidos_bp.route("/detalle_pedido=<int:id>")
def detalle_pedido(id):
    detalles = controlador_detalle.obtener_listado_detalle_por_id_pedido(id)
    pedido = controlador_pedido.obtener_pedido_id(id)
    estados = controlador_estado_pedido.obtener_listado_estados_pedido()
    metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
    return render_template("listado_detalle_pedido.html", detalles=detalles , pedido_id=id , pedido = pedido , estados = estados , metodos = metodos)


@pedidos_bp.route("/eliminar_detalle_pedido", methods=["POST"])
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


@pedidos_bp.route("/editar_detalle=<int:producto_id>&editar_detalle=<int:pedido_id>", methods=["GET", "POST"])
def editar_detalle(producto_id, pedido_id):
    detalle = controlador_detalle.obtener_detalle_por_ids(producto_id, pedido_id)

    productos =controlador_detalle.obtenerProductos()

    return render_template("editar_detalle.html", detalle=detalle, productos=productos, producto_id=producto_id, pedido_id=pedido_id)


@pedidos_bp.route("/actualizar_detalle_pedido", methods=["POST"])
def actualizar_detalle_pedido():
    producto_id = request.form["producto_id"]
    pedido_id = request.form["pedido_id"]
    cantidad = request.form["cantidad"]

    controlador_detalle.editar_detalle(producto_id, pedido_id, cantidad)

    return redirect(url_for('detalle_pedido', id=pedido_id))





