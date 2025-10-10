from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from flask_jwt import JWT, jwt_required, current_identity
import hashlib
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
app.config['SECRET_KEY'] = 'super-secret'
app.debug = True


def authenticate(username, password):
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_email(username)
    if not data:
        return None
    user = Usuario(id=data[0], correo=data[1], contrasenia=data[2], tipo_usuario_id=data[3])

    if user and user.contrasenia == hashlib.sha256(password.encode('utf-8')).hexdigest():
        if user.tipo_usuario_id in [1, 2, 3]:
            return user

    return None

def identity(payload):
    user_id = payload['identity']
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    user = Usuario(id=data[0], correo=data[1], contrasenia=data[2])
    return user

jwt = JWT(app, authenticate, identity)


from blueprints import (
    auth_bp,
    general_bp,
    carrito_bp,
    pedidos_bp,
    perfil_bp,
    comentarios_bp,
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)