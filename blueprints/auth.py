from flask import Blueprint, render_template, request, redirect, session, make_response
from controladores import (
    controlador_usuario_cliente ,
    controlador_usuario_admin ,
)
from utils import encstringsha256
auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/iniciar_sesion")
def iniciar_sesion():
    return render_template("iniciar_sesion.html")


@auth_bp.route("/registrate")
def registrate():
    return render_template("registrate.html")


@auth_bp.route("/registrar_cliente", methods=["POST"])
def registrar_cliente():
    try:
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        dni = request.form["dni"]
        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        password = request.form["password"]
        disponibilidad = 1
        tipo_usuario = 3

        epassword = encstringsha256(password)

        result = controlador_usuario_cliente.insertar_usuario(
            nombres, apellidos, dni, genero, fecha_nacimiento, telefono, correo, epassword, disponibilidad, tipo_usuario
        )

        if result == 1:

            usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_email(correo)
            user_id = usuario[0]

            session['username'] = correo
            session['id'] = user_id
            resp = make_response(redirect(f"/perfil={user_id}"))
            resp.set_cookie('username', correo)
            return resp
        elif result == 0:
            return render_template(
                "iniciar_sesion.html",
                mostrar_modal=True,
                mensaje_modal="El correo usado ya fue registrado. Por favor, intente con otro."
            )
        else:
            return "Error al procesar la solicitud", 400
    except Exception as e:
        print(f"Error en registrar_cliente: {e}")
        return render_template(
            "iniciar_sesion.html",
            mostrar_modal=True,
            mensaje_modal="Error en el servidor. Por favor, intente más tarde."
        )


@auth_bp.route("/login", methods=['POST'])
def login():
    email = request.form.get('email-login')
    password = request.form.get('password-login')
    user = controlador_usuario_cliente.obtener_usuario_cliente_por_email(email)

    # if user and user[2]==epassword:
    #     session['username']=email
    #     resp=make_response(redirect("/"))
    #     resp.set_cookie('username',email)
    #     return resp
    if user:
        epassword = encstringsha256(password)
        if user[2] == epassword:
            session['id'] = user[0]
            session['username'] = email
            session['tipo_usuarioid'] = controlador_usuario_admin.obtenerTipoU(email)
            resp = make_response(redirect("/"))
            resp.set_cookie('username', email)
            return resp
        else:
            return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Contraseña incorrecta.")
    else:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Usuario no válido. Si es cliente, regístrese.")


@auth_bp.route("/logout")
def logout():
    session.clear()

    resp = make_response(redirect('/'))

    resp.delete_cookie('username')

    return resp


@auth_bp.route("/cambiar_contrasenia_cliente", methods=['GET', 'POST'])
def cambiar_contrasenia_cliente():
    user_id = session.get('id')
    usuario = controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    img = controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)

    if request.method == 'POST':
        current_password = request.form['current-password']
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']

        if new_password != confirm_password:
            error_message = "Las contraseñas no coinciden."
            return render_template('cambiarContraseñaCliente.html', error_message=error_message, user_id=user_id, usuario=usuario, img=img)

        if usuario and usuario[9] == encstringsha256(current_password):
            controlador_usuario_cliente.cambiar_contrasenia(user_id, encstringsha256(new_password))

            session.clear()

            resp = make_response(redirect('/iniciar_sesion'))
            resp.delete_cookie('username')
            return resp

        else:
            error_message = "La contraseña actual es incorrecta."
            return render_template('cambiarContraseñaCliente.html', error_message=error_message, user_id=user_id, usuario=usuario, img=img)

    return render_template('cambiarContraseñaCliente.html', user_id=user_id, usuario=usuario, img=img)





