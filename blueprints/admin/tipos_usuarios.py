from flask import Blueprint, render_template, redirect, url_for, session , flash , request , make_response
from functools import wraps
from controladores import (
    controlador_tipos_usuario ,
    controlador_usuario_admin,
)

admin_tipos_usuarios_bp = Blueprint('admin_tipos_usuarios', __name__)


@admin_tipos_usuarios_bp.route("/listado_tipos_usuario")
def listado_tipos_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_usuario = controlador_tipos_usuario.obtener_listado_tipos_usuario()
        return render_template("listado_tipos_usuario.html", tipos_usuario=tipos_usuario)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_tipos_usuarios_bp.route("/agregar_tipo_usuario")
def formulario_agregar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_usuario.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_tipos_usuarios_bp.route("/guardar_tipo_usuario", methods=["POST"])
def guardar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo = request.form["tipo"]
        descripcion = request.form["descripcion"]
        imagen = request.files["img_user"]
        img_binario = imagen.read()

        controlador_tipos_usuario.insertar_tipo_usuario(tipo, descripcion, img_binario)
        return redirect("/listado_tipos_usuario")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_tipos_usuarios_bp.route("/formulario_editar_tipo_usuario=<int:id>")
def editar_tipo_usuario(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo_usuario = controlador_tipos_usuario.obtener_tipo_usuario_por_id(id)
        return render_template("editar_tipo_usuario.html", tipo_usuario=tipo_usuario)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_tipos_usuarios_bp.route("/actualizar_tipo_usuario", methods=["POST"])
def actualizar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        imagen_user = controlador_tipos_usuario.obtener_img_tipo_usuario_por_id(id)
        tipo = request.form["tipo"]
        descripcion = request.form["descripcion"]
        imagen = request.files["img_user"]

        if imagen.filename == '':
            img_binario = imagen_user[0]
        else:
            img_binario = imagen.read()

        disp = request.form.get("disponibilidad")

        controlador_tipos_usuario.actualizar_tipo_usuario(id, tipo, descripcion, img_binario, disp)
        return redirect("/listado_tipos_usuario")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_tipos_usuarios_bp.route("/eliminar_tipo_usuario", methods=["POST"])
def eliminar_tipo_usuario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        controlador_tipos_usuario.eliminar_tipo_usuario(id)
        return redirect("/listado_tipos_usuario")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa



