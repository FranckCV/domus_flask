from flask import render_template, Blueprint, request, redirect, flash, session, url_for, jsonify, send_file, make_response

from clases import clsSubcategoria
from controladores import (
    controlador_categorias, controlador_subcategorias, 
    controlador_usuario_admin
)
admin_subcategorias_bp = Blueprint('admin_subcategorias', __name__)



@admin_subcategorias_bp.route("/listado_subcategorias")
def subcategorias():
    if 'usuario' in session:
        username = session['usuario']  # Recuperar el usuario desde la sesión
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener el tipo de usuario

        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        # Si el tipo de usuario no es 2, continuar con el resto del flujo
        categorias = controlador_categorias.obtener_listado_categorias()
        subcategorias = controlador_subcategorias.obtener_listado_subcategorias()

        # Renderizar la plantilla con los datos
        return render_template(
            "listado_subcategorias.html",
            categorias=categorias,
            subcategorias=subcategorias
        )
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_subcategorias_bp.route("/listado_subcategorias_buscar")
def subcategorias_buscar():
    if 'usuario' in session:
        username = session['usuario']  # Recuperar el usuario desde la sesión
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener el tipo de usuario

        # Verificar si el tipo de usuario es 2 y redirigir al dashboard si es así
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        # Si el tipo de usuario no es 2, continuar con la búsqueda
        nombreBusqueda = request.args.get("buscarElemento")
        categorias = controlador_categorias.obtener_listado_categorias()
        subcategorias = controlador_subcategorias.buscar_listado_subcategorias_nombre(nombreBusqueda)

        return render_template(
            "listado_subcategorias.html",
            categorias=categorias,
            subcategorias=subcategorias,
            nombreBusqueda=nombreBusqueda
        )
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_subcategorias_bp.route("/agregar_subcategoria")
def formulario_agregar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        categorias = controlador_categorias.obtener_categorias()
        return render_template("agregar_subcategoria.html", categorias=categorias, active='categorias')
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_subcategorias_bp.route("/guardar_subcategoria", methods=["POST"])
def guardar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        faicon_subcat = request.form["faicon_subcat"]
        categoria_id = request.form["categoria_id"]

        objSub = clsSubcategoria(
            p_id = None,
            p_subcategoria = nombre,
            p_faicon_subcat = faicon_subcat,
            p_disponibilidad = 1,
            p_CATEGORIAid = categoria_id
        )

        controlador_subcategorias.insertar_subcategoria(objSub.subcategoria, objSub.faicon_subcat, objSub.disponibilidad, objSub.CATEGORIAid)
        return redirect("/listado_subcategorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_subcategorias_bp.route("/eliminar_subcategoria", methods=["POST"])
def eliminar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_subcategorias.eliminar_subcategoria(request.form["id"])
        return redirect("/listado_subcategorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_subcategorias_bp.route("/formulario_editar_subcategoria=<int:id>")
def editar_subcategoria(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        subcategoria = controlador_subcategorias.obtener_subcategoria_por_id(id)
        categorias = controlador_categorias.obtener_categorias()
        return render_template("editar_subcategoria.html", subcategoria=subcategoria, categorias=categorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_subcategorias_bp.route("/actualizar_subcategoria", methods=["POST"])
def actualizar_subcategoria():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        faicon_subcat = request.form["faicon_subcat"]
        disponibilidad = request.form["disponibilidad"]
        categoria_id = request.form["categoria_id"]

        objSub = clsSubcategoria(
            p_id = id,
            p_subcategoria = nombre,
            p_faicon_subcat = faicon_subcat,
            p_disponibilidad = disponibilidad,
            p_CATEGORIAid = categoria_id
        )
        print("equideeee")
        controlador_subcategorias.actualizar_subcategoria(objSub.subcategoria, objSub.faicon_subcat, objSub.disponibilidad, objSub.CATEGORIAid, objSub.id)
        return redirect("/listado_subcategorias")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa

