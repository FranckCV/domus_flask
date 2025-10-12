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

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route("/carrito")
def carrito():
    usuario_id = session.get('id')

    if usuario_id is not None:
        productosPopulares = controlador_productos.obtenerEnTarjetasMasRecientes()
        print(session.get('id'))
        productos = controlador_detalle.obtener_Detalle(session.get('id'))
        error_message = request.args.get("error_message")

        return render_template("carrito.html", productosPopulares=productosPopulares, productos=productos, error_message=error_message or "")
    else:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Regístrese para agregar al carrito")


@carrito_bp.route('/obtener_cantidad_carrito', methods=['GET'])
def obtener_cantidad_carrito():
    usuario_id = session.get('id')

    if not usuario_id:
        return jsonify({"cantidad": 0}), 200

    cantidad_carrito = controlador_detalle.obtenerCantidadDetallePorUsuario(usuario_id)

    return jsonify({"cantidad": cantidad_carrito}), 200


@carrito_bp.route("/obtener_resumen_carrito", methods=["GET"])
def obtener_resumen_carrito():
    usuario_id = session.get('id')

    if usuario_id is None:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    carrito = controlador_detalle.obtener_DetalleConDic(usuario_id)

    subtotal = 0
    for producto in carrito:
        subtotal += producto['precio'] * producto['cantidad']

    descuento = 0
    if cupon in request.args:
        descuento = subtotal * 0.20

    total = subtotal - descuento

    return jsonify({
        'carrito': carrito,
        'subtotal': subtotal,
        'descuento': descuento,
        'total': total
    })


@carrito_bp.route("/agregar_carrito", methods=["POST"])
def agregar_carrito():
    producto_id = request.form["producto_id"]
    estado = 1
    usuario_id = session.get('id')

    if usuario_id is not None:
        pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

        if pedido_id is None:
            pedido_id = controlador_carrito.insertar_pedido(usuario_id, estado)

        result = controlador_carrito.insertar_detalle(producto_id, pedido_id)
        referrer = request.referrer

        if result is not None:
            if referrer and "carrito" in referrer:
                return redirect(url_for('carrito'))
            else:
                return '', 204
        else:
            return redirect(url_for('carrito', error_message="No se pudo agregar el producto al carrito."))

    else:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Regístrese para agregar al carrito")


@carrito_bp.route("/aumentar_carro", methods=["POST"])
def aumentar_carro():
    producto_id = request.form.get("producto_id")
    usuario_id = session.get('id')
    estado = 1

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

    if pedido_id:
        result=controlador_carrito.aumentar_producto(pedido_id,producto_id)
        if result is None:
            return redirect('/carrito')
        else:
           return redirect(url_for('carrito', error_message=str(result)))
    else:
        print("No se encontró un pedido activo.")


@carrito_bp.route("/disminuir_carro", methods=["POST"])
def disminuir_carro():
    producto_id = request.form["producto_id"]
    usuario_id =session.get('id')
    estado = 1

    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)

    if pedido_id:
        controlador_carrito.eliminar_producto(pedido_id,producto_id)

    return redirect('/carrito')


@carrito_bp.route("/confirmar_carrito", methods=["POST"])
def confirmar_carrito():
    estado = 1
    usuario_id = session.get('id')

    valor_descuento=request.form.get('total_descuento')

    pedido_id=controlador_carrito.verificarIdPedido(usuario_id,estado)

    subtotal=0
    productos_carrito = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)

    for producto in productos_carrito:
        cantidad = producto[3]
        precio_unitario = producto[2]
        producto_id = producto[4]
        total_producto = cantidad * precio_unitario


        subtotal += total_producto

    # print(f"Total del pedido: {subtotal}")
    # print(f"Descuento aplicado: {valor_descuento}")
    #Obtengo el pedido_id del usuario
    pedido_id = controlador_carrito.verificarIdPedido(usuario_id, estado)
    #Obtengo el detalle de ese pedido_id
    existencias = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)

    metodos_pago = controlador_metodo_pago.obtener_metodo_pago()

    if existencias and len(existencias) > 0:
        return render_template("resumen_de_Pedido.html",
                               existencias=existencias,
                               total_pagar=subtotal,
                               valor_descuento=valor_descuento,
                               metodos_pago=metodos_pago)
    else:
        return redirect(url_for('carrito', error_message="El carrito no puede estar vacío"))


@carrito_bp.route("/resumen_de_pedido")
def resumen_de_pedido():
    usuario=1
    pedido_id=controlador_carrito.ultimoPedido(usuario)
    metodos_pago =controlador_metodo_pago.obtener_metodo_pago()
    print("los metodos son:",metodos_pago)
    existencias = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)
    # metodoID = request.form["metodo_pago"]
    # controlador_pedido.actualizar_MetPago_Pedido(pedido_id,metodoID)
    return render_template("resumen_de_Pedido.html", metodos_pago=metodos_pago, existencias=existencias)


@carrito_bp.route('/cancelar_compra')
def cancelar_compra():
    usuario_id = session.get('id')
    estado_cancelado = 1
    pedido_id=controlador_carrito.ultimoPedido(usuario_id)
    controlador_carrito.cancelar_pedido(usuario_id, estado_cancelado,pedido_id)
    return redirect('/carrito')


@carrito_bp.route("/confirmar_compra", methods=['POST'])
def confirmar_compra():
    usuario_id = session.get('id')
    fecha_compra = date.today()
    metodo_pago = request.form.get('metodo_pago')
    estado = 2

    pedido_id = controlador_carrito.ultimoPedido(usuario_id)

    subtotal = 0
    productos_carrito = controlador_detalle.obtener_Detalle_por_Id_pedido(pedido_id)

    for producto in productos_carrito:
        cantidad = producto[3]
        precio_unitario = producto[2]
        producto_id = producto[4]
        total_producto = cantidad * precio_unitario
        controlador_detalle.reducir_detalle(producto_id, cantidad)
        subtotal += total_producto

    controlador_pedido.actualizarPedido(pedido_id, fecha_compra, subtotal,metodo_pago,estado,usuario_id)

    return redirect("/")



