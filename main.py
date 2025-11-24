from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from flask_jwt import JWT, jwt_required, current_identity
from utils import encstringsha256
from datetime import timedelta
from blueprints.api.utils import response_error , response_success

# from utils import *
from controladores import (
    controlador_categorias,
    controlador_marcas,
    controlador_productos,
    controlador_novedades ,
    controlador_redes_sociales ,
    controlador_informacion_domus ,
    controlador_lista_deseos ,
    controlador_usuario_cliente ,
    controlador_contenido_info
)
from clase_user_v1.usuario import Usuario

app = Flask(__name__)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=60)
app.config['SECRET_KEY'] = 'super-secret'
app.debug = True


def authenticate(username, password):
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_email(username)
    if not data:
        return None
    user = Usuario(id=data[0], correo=data[1], contrasenia=data[2], tipo_usuario_id=data[3])

    if user and user.contrasenia == encstringsha256(password):
        return user

    return None


def identity(payload):
    """Obtiene el usuario a partir del JWT"""
    try:
        user_id = payload.get('identity')
        if not user_id:
            return None

        data = controlador_usuario_cliente.obtener_usuario_cliente_por_id2(user_id)

        if not data:
            return None

        user = Usuario(
            id=data[0],
            correo=data[1],
            contrasenia=data[2],
            tipo_usuario_id=data[3]
        )
        return user
    except Exception as e:
        print(f"Error en identity: {e}")
        return None


jwt = JWT(app, authenticate, identity)


from blueprints import (
    auth_bp,
    general_bp,
    carrito_bp,
    pedidos_bp,
    perfil_bp,
    comentarios_bp,
    dbms_bp ,
    admin_dashboard_bp,
    admin_categorias_bp,
    admin_subcategorias_bp,
    admin_productos_bp,
    admin_marcas_bp,
    admin_caracteristicas_bp,
    admin_empleados_bp,
    admin_usuarios_clientes_bp,
    admin_novedades_bp,
    admin_configuracion_bp,
    admin_contenido_bp,
    admin_comentario_bp,
    api_v1_bp,
    api_bp
)


app.register_blueprint(auth_bp)
app.register_blueprint(general_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(comentarios_bp)
app.register_blueprint(dbms_bp, url_prefix='/dbms')

app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
app.register_blueprint(admin_categorias_bp, url_prefix='/admin')
app.register_blueprint(admin_subcategorias_bp, url_prefix='/admin')
app.register_blueprint(admin_productos_bp, url_prefix='/admin')
app.register_blueprint(admin_marcas_bp, url_prefix='/admin')
app.register_blueprint(admin_caracteristicas_bp, url_prefix='/admin')
app.register_blueprint(admin_empleados_bp, url_prefix='/admin')
app.register_blueprint(admin_usuarios_clientes_bp, url_prefix='/admin')
app.register_blueprint(admin_novedades_bp, url_prefix='/admin')
app.register_blueprint(admin_configuracion_bp, url_prefix='/admin')
app.register_blueprint(admin_contenido_bp, url_prefix='/admin')
app.register_blueprint(admin_comentario_bp, url_prefix='/admin')

app.register_blueprint(api_v1_bp, url_prefix='/api_v1')
app.register_blueprint(api_bp, url_prefix='/api')


@app.before_request
def verify_token():
    if request.path.startswith('/api/'):
        jwt_required()(lambda: None)()


@app.context_processor
def inject_globals():
    categoriasMenu = controlador_categorias.obtener_categorias_disponibles()
    marcasMenu = controlador_marcas.obtener_marcas_menu(10)
    logo_foto = 'img/elementos/logoDomus.png'
    redes_footer = controlador_redes_sociales.obtener_redes_sociales()
    conts_info_footer = controlador_contenido_info.obtener_tipos_contenido()
    datos_domus_main = controlador_informacion_domus.obtener_informacion_domus()
    logueado_dato = session.get('id') is not None
    user_id = session.get('id') if logueado_dato else None
    lista_deseos = controlador_lista_deseos.obtenerListaDeseos(session.get('id'))
    lista_deseos_ids = [producto[0] for producto in lista_deseos]
    return dict(
        marcasMenu=marcasMenu,
        logo_foto=logo_foto,
        categoriasMenu=categoriasMenu,
        redes_footer=redes_footer,
        conts_info_footer=conts_info_footer,
        datos_domus_main=datos_domus_main,
        logueado=logueado_dato,
        user_id=user_id ,
        lista_deseos_ids=lista_deseos_ids
    )


@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


@app.route("/")
def main_page():
    return redirect(url_for('general.index'))



@app.route("/sql_api", methods=["POST"])
def sql_api():
    try:
        data = request.get_json()
        tipo = data.get("tipo")  # "fetchall", "fetchone", "execute", "execute_last_id"
        sql = data.get("sql")
        args = data.get("args", [])

        if not tipo or not sql:
            return jsonify({"error": "Faltan parámetros obligatorios: 'tipo' y 'sql'"}), 400

        import bd

        if tipo == "fetchall":
            result = bd.sql_select_fetchall(sql, args)
            return jsonify({"status": "ok", "result": result})
        elif tipo == "fetchone":
            result = bd.sql_select_fetchone(sql, args)
            return jsonify({"status": "ok", "result": result})
        elif tipo == "execute":
            bd.sql_execute(sql, args)
            return jsonify({"status": "ok"})
        elif tipo == "execute_last_id":
            last_id = bd.sql_execute_lastrowid(sql, args)
            return jsonify({"status": "ok", "last_id": last_id})
        else:
            return jsonify({"error": "Tipo de operación inválido"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/bd_operation", methods=["POST"])
def bd_operation():
    try:
        data = request.get_json()
        tipo = data.get("tipo")  # "fetchall", "fetchone", "execute", "execute_last_id"
        sql = data.get("sql")
        args = data.get("args", [])

        if not tipo or not sql:
            return jsonify({"error": "Faltan parámetros obligatorios: 'tipo' y 'sql'"}), 400

        import bd

        if tipo == "fetchall":
            result = bd.sql_select_fetchall(sql, args)
            return jsonify({"status": "ok", "result": result})
        elif tipo == "fetchone":
            result = bd.sql_select_fetchone(sql, args)
            return jsonify({"status": "ok", "result": result})
        elif tipo == "execute":
            bd.sql_execute(sql, args)
            return jsonify({"status": "ok"})
        elif tipo == "execute_last_id":
            last_id = bd.sql_execute_lastrowid(sql, args)
            return jsonify({"status": "ok", "last_id": last_id})
        else:
            return jsonify({"error": "Tipo de operación inválido"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/login_movil", methods=['POST'])
def login_movil():
    try:
        body = request.json.get('body_request', {})

        correo = body.get("correo")
        contrasenia = body.get("contrasenia")

        if not correo or not contrasenia:
            return response_error("Debe proporcionar correo y contraseña")

        usuario = controlador_usuario_cliente.get_usuario_correo(correo)

        if not usuario:
            return response_error("Usuario no válido. Si es cliente, regístrese.")

        epassword = encstringsha256(contrasenia)

        stored_password = usuario.get("contrasenia")

        if epassword == stored_password:
            msg = "Inicio de sesión exitoso"
            data = usuario
            # print(f"Esto responde el login {response_success(msg, data)}")
            return response_success(msg, data)
        else:
            return response_error("Credenciales incorrectas")

    except Exception as e:
        return response_error(str(e))





@app.route("/registrar_usuario",methods = ['POST'])
def registrar_usuario():
    try:
        body = request.json.get('body_request',{})

        nombres = body.get("nombres")
        apellidos = body.get("apellidos")
        doc_identidad = body.get("doc_identidad")
        genero = body.get("genero")
        telefono = body.get("telefono")
        correo = body.get("correo")
        contrasenia = body.get("contrasenia")

        usuario_id = controlador_usuario_cliente.register_usuario_cliente(nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia)
        if usuario_id == 0:
            msg = 'Error al resgistrar usuario'
            data = { 'usuario_id' : usuario_id }
        else:
            msg = 'Usuario registrado exitosamente'
            data = { 'usuario_id' : usuario_id }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)