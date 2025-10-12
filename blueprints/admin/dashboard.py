from flask import Blueprint, render_template, redirect, url_for, session , flash , request , make_response
from functools import wraps
from controladores import (
    controlador_empleados ,
    controlador_usuario_admin ,
)

from utils import encstringsha256

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form.get('username')
        password = request.form.get('password')
        epassword = password

        if password != controlador_empleados.clave_default_empleado():
            epassword = encstringsha256(password)

        # Llamar al controlador para validar las credenciales
        if controlador_usuario_admin.confirmarDatosAdm(username, epassword):
            # Crear sesión
            session['usuario'] = username
            session['tipo_usuarioid'] = controlador_usuario_admin.obtenerTipoU(username)
            session['nombre_c'] = controlador_usuario_admin.obtenerNombresC(username)
            session['doc_identidad'] =controlador_usuario_admin.obtenerdoc(username)
            session['genero'] =controlador_usuario_admin.obtenergenero(username)
            session['fecha_nacimiento'] =controlador_usuario_admin.obtenerfecha_nacimiento(username)
            session['telefono'] =controlador_usuario_admin.obtenertelefono(username)
            resultados = controlador_usuario_admin.obtenerDataU(username)
            contrase = controlador_usuario_admin.obtenerContrasenia(username)
            user_id = controlador_usuario_admin.obtenerID(username)
            if contrase == controlador_empleados.clave_default_empleado():
                return redirect('/cambiar_contrasenia='+str(user_id))
            else:
                return redirect(url_for('dashboard'))  # Redirigir al dashboard

        # Mostrar un mensaje de alerta si las credenciales son inválidas
        flash("Credenciales incorrectas. Inténtalo de nuevo.", "danger")

    return render_template('login-admin.html')  # Renderizar formulario de login


@admin_dashboard_bp.route('/cambiar_contrasenia_administrador', methods=['GET', 'POST'])
def cambiar_contrasenia_administrador():
    user_id = session.get('id')  # ID del administrador desde la sesión
    usuario = controlador_usuario_admin.obtener_usuario_por_id(user_id)  # Obtener datos del administrador

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            error_message = "Las contraseñas no coinciden."
            return render_template('cuenta_administrativa.html', error_message=error_message, usuario=usuario)

        # Validar contraseña actual
        if usuario and usuario[9] == encstringsha256(current_password):
            # Cambiar contraseña
            controlador_usuario_admin.cambiar_contrasenia(user_id, encstringsha256(new_password))
            session.clear()  # Limpiar sesión después del cambio de contraseña
            resp = make_response(redirect('/cuenta_administrativa'))
            resp.delete_cookie('username')
            return resp
        else:
            error_message = "La contraseña actual es incorrecta."
            return render_template('cuenta_administrativa.html', error_message=error_message, usuario=usuario)

    return render_template('cuenta_administrativa.html', usuario=usuario)


