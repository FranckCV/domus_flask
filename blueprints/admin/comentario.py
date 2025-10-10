from flask import Blueprint, render_template, redirect, url_for, session , flash , request , make_response

from clases import clsComentario, clsMotivoComentario
from controladores import controlador_comentario, controlador_motivo_comentario, controlador_usuario_admin
admin_comentario_bp = Blueprint('admin_comentario', __name__)


@admin_comentario_bp.route("/comentarios_listado")
def comentarios_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        comentarios = controlador_comentario.obtener_listado_comentarios()
        motivos = controlador_motivo_comentario.obtener_motivos_disponibles()

        return render_template("listado_comentarios.html", comentarios=comentarios, motivos=motivos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/ver_comentario=<int:id>")

def ver_comentario(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        comentario = controlador_comentario.ver_comentario_por_id(id)
        motivos = controlador_motivo_comentario.obtener_listado_motivos()

        return render_template("ver_comentario.html", comentario=comentario, motivos=motivos, id=id)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/comentarios_listado_buscar")

def comentarios_listado_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        comentarios = controlador_comentario.buscar_listado_comentarios_palabra(nombreBusqueda)
        motivos = controlador_motivo_comentario.obtener_motivos_disponibles()

        return render_template("listado_comentarios.html", comentarios=comentarios, motivos=motivos, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/guardar_comentario", methods=["POST"])

def guardar_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        motivo_comentario_id = request.form["motivo_comentario_id"]
        mensaje = request.form["mensaje"]

        # Estado por defecto: pendiente (1)
        estado = 0

        # Usuario id como null (si no está disponible)
        usuario_id = None

        obj = clsComentario(
            p_id = None,
            p_nombres = nombres,
            p_apellidos = apellidos,
            p_email = email,
            p_celular = telefono,
            p_mensaje = mensaje,
            p_fecha_registro = None,
            p_estado = 0,
            p_MOTIVO_COMENTARIOid = motivo_comentario_id,
            p_USUARIOid = None
        )

        controlador_comentario.insertar_comentario(obj.nombres, obj.apellidos, obj.email, obj.celular, obj.mensaje, obj.estado, obj.MOTIVO_COMENTARIOid, obj.USUARIOid)

        return redirect("/")
    else:
        return redirect(url_for('/'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/eliminar_comentario", methods=["POST"])

def eliminar_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_comentario.eliminar_comentario(request.form["id"])
        return redirect("/comentarios_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/estado_comentario", methods=["POST"])

def estado_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_comentario.estado_comentario(request.form["id"])
        return redirect(request.referrer)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/estado_comentario_respondido", methods=["POST"])

def estado_comentario_respondido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_comentario.estado_comentario_respondido(request.form["id"])
        return redirect(request.referrer)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa








@admin_comentario_bp.route("/motivos_comentario_listado")

def motivos_comentario_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        motivos = controlador_motivo_comentario.obtener_listado_motivos()
        return render_template("listado_motivos_comentarios.html", motivos=motivos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/motivos_comentario_buscar")

def motivos_comentario_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        motivos = controlador_motivo_comentario.buscar_listado_motivos_nombre(nombreBusqueda)
        return render_template("listado_motivos_comentarios.html", motivos=motivos, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/agregar_motivo_comentario")

def formulario_agregar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_motivo_comentario.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/guardar_motivo_comentario", methods=["POST"])

def guardar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        motivo = request.form["motivo"]

        obj = clsMotivoComentario(
            p_id = None,
            p_motivo = motivo,
            p_disponibilidad = 1
        )

        controlador_motivo_comentario.insertar_motivo(obj.motivo, obj.disponibilidad)
        return redirect("/motivos_comentario_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/eliminar_motivo_comentario", methods=["POST"])

def eliminar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_motivo_comentario.eliminar_motivo(request.form["id"])
        return redirect("/motivos_comentario_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/formulario_editar_motivo_comentario=<int:id>")

def editar_motivo_comentario(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        motivo_comentario = controlador_motivo_comentario.obtener_motivo_por_id(id)
        return render_template("editar_motivo_comentario.html", motivo_comentario=motivo_comentario)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@admin_comentario_bp.route("/actualizar_motivo_comentario", methods=["POST"])

def actualizar_motivo_comentario():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        motivo = request.form["motivo"]
        disponibilidad = request.form["disponibilidad"]

        obj = clsMotivoComentario(
            p_id = id,
            p_motivo = motivo,
            p_disponibilidad = disponibilidad
        )

        controlador_motivo_comentario.actualizar_motivo(obj.motivo, obj.disponibilidad , obj.id)
        return redirect("/motivos_comentario_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa



