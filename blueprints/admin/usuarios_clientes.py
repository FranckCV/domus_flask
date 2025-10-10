from flask import Blueprint, render_template, redirect, url_for, session , flash , request , make_response
from functools import wraps
from controladores import (
    controlador_estado_pedido,
    controlador_metodo_pago,
    controlador_pedido ,
    controlador_usuario_admin,
    controlador_usuario_cliente ,
)

admin_usuarios_clientes_bp = Blueprint('admin_usuarios_clientes', __name__)

def login_requerido(func):
    @wraps(func)  # Conserva el nombre y docstring de la función decorada
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:  # Si no hay sesión activa
            return redirect(url_for('login_admin'))  # Redirigir al login
        return func(*args, **kwargs)  # Ejecutar la función original si está autenticado
    return envoltura


@admin_usuarios_clientes_bp.route("/listado_clientes")
@login_requerido
def listado_clientes():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuarios_clientes = controlador_usuario_cliente.obtener_listado_usuarios_clientes()
        imagenes = controlador_usuario_cliente.obtener_listado_imagenes_usuario_cliente()
        return render_template("listado_clientes.html", usuarios_clientes=usuarios_clientes , imagenes = imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_usuarios_clientes_bp.route("/listado_clientes_buscar")
@login_requerido
def listado_clientes_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        usuarios_clientes = controlador_usuario_cliente.buscar_listado_usuarios_clientes_nombre(nombreBusqueda)
        imagenes = controlador_usuario_cliente.obtener_listado_imagenes_usuario_cliente()
        return render_template("listado_clientes.html", usuarios_clientes=usuarios_clientes , nombreBusqueda = nombreBusqueda , imagenes = imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_usuarios_clientes_bp.route("/ver_cliente=<int:id>")
@login_requerido
def ver_cliente(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_usuario_cliente.ver_info_usuario_cliente(id)
        imagen = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
        pedidos = controlador_pedido.obtener_listado_pedidos_usuario_id(id)
        estados = controlador_estado_pedido.obtener_listado_estados_pedido()
        metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
        return render_template("ver_usuario_cliente.html", usuario = usuario , pedidos = pedidos , estados = estados , metodos = metodos , imagen = imagen)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_usuarios_clientes_bp.route("/formulario_editar_cliente=<int:id>")
@login_requerido
def editar_cliente(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(id)
        imagen = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
        return render_template("editar_cliente.html", usuario=usuario , imagen = imagen)

    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_usuarios_clientes_bp.route("/actualizar_cliente", methods=["POST"])
@login_requerido
def actualizar_cliente():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        img_usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(id)

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        doc_identidad = request.form["doc_identidad"]
        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        disponibilidad = request.form["disponibilidad"]

        imagen = request.files["img_usuario"]
        if imagen.filename == '':
            img_bin = img_usuario[4]
        else:
            img_bin = imagen.read()

        controlador_usuario_cliente.actualizar_usuario_cliente(id, nombres, apellidos, doc_identidad, genero, fecha_nacimiento, telefono, correo, disponibilidad,img_bin)
        return redirect("/listado_clientes")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_usuarios_clientes_bp.route("/eliminar_cliente", methods=["POST"])
@login_requerido
def eliminar_cliente():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        controlador_usuario_cliente.eliminar_usuario_cliente(id)
        return redirect("/listado_clientes")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa

