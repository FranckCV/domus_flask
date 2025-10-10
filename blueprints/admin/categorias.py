from flask import render_template, Blueprint, request, redirect, flash, session, url_for, jsonify, send_file, make_response
admin_categorias_bp = Blueprint('admin_categorias', __name__)

from clases import clsCategoria
from controladores import controlador_categorias, controlador_subcategorias, controlador_usuario_admin




@admin_categorias_bp.route("/agregar_categoria")
def formulario_agregar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_categoria.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_categorias_bp.route("/guardar_categoria", methods=["POST"])
def guardar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        categoria = request.form["categoria"]
        faicon_cat = request.form["faicon_cat"]

        obj = clsCategoria(
            p_id = None,
            p_categoria = categoria,
            p_faicon_cat = faicon_cat,
            p_disponibilidad = 1
        )

        controlador_categorias.insertar_categoria(obj.categoria, obj.faicon_cat, obj.disponibilidad)
        return redirect("/listado_categorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_categorias_bp.route("/listado_categorias")
def categorias():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        categorias = controlador_categorias.obtener_listado_categorias()
        subcategorias = controlador_subcategorias.obtener_subcategorias()
        return render_template("listado_categorias.html", categorias=categorias, subcategorias=subcategorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_categorias_bp.route("/eliminar_categoria", methods=["POST"])
def eliminar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        categoria = controlador_categorias.obtener_categoria_id_relacion(id)
        result = categoria[4]

        if result != 0:
            return render_template("listado_categorias.html", error="La categoría tiene elementos asociados y no se puede eliminar. Redirigiendo en 3 segundos...", show_modal=True)
        else:
            controlador_categorias.eliminar_categoria(id)
            return redirect("/listado_categorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_categorias_bp.route("/formulario_editar_categoria=<int:id>")
def editar_categoria(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        categoria = controlador_categorias.obtener_categoria_por_id(id)
        return render_template("editar_categoria.html", categoria=categoria)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_categorias_bp.route("/actualizar_categoria", methods=["POST"])
def actualizar_categoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        categoria = request.form["categoria"]
        faicon_cat = request.form["faicon_cat"]
        disponibilidad = request.form["disponibilidad"]
        obj = clsCategoria(
            p_id = id,
            p_categoria = categoria,
            p_faicon_cat = faicon_cat,
            p_disponibilidad = disponibilidad
        )
        controlador_categorias.actualizar_categoria(obj.categoria, obj.faicon_cat, obj.disponibilidad, obj.id)
        return redirect("/listado_categorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa




