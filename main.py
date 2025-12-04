from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from utils import encstringsha256
from datetime import timedelta
from blueprints.api.utils import response_error, response_success
import firebase_admin
from firebase_admin import credentials
import os

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
    controlador_contenido_info,
    controlador_bitacora
)
from clase_user_v1.usuario import Usuario

app = Flask(__name__)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=60)
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-super-secret-y-12'  # Cambia esto por una clave segura    
app.debug = True


# def authenticate(username, password):
#     data = controlador_usuario_cliente.obtener_usuario_cliente_por_email(username)
#     if not data:
#         return None
#     user = Usuario(id=data[0], correo=data[1], contrasenia=data[2], tipo_usuario_id=data[3])

#     if user and user.contrasenia == encstringsha256(password):
#         return user

#     return None


# def identity(payload):
#     """Obtiene el usuario a partir del JWT"""
#     try:
#         user_id = payload.get('identity')
#         if not user_id:
#             return None

#         data = controlador_usuario_cliente.obtener_usuario_cliente_por_id2(user_id)

#         if not data:
#             return None

#         user = Usuario(
#             id=data[0],
#             correo=data[1],
#             contrasenia=data[2],
#             tipo_usuario_id=data[3]
#         )
#         return user
#     except Exception as e:
#         print(f"Error en identity: {e}")
#         return None


jwt = JWTManager(app)

# Inicializar Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred_path = os.path.join(os.path.dirname(__file__), 'firebase-credentials.json')
        print(f"Ruta del archivo de credenciales de Firebase: {cred_path}")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin inicializado correctamente")
        else:
            print("⚠️ Archivo firebase-credentials.json no encontrado")
    except Exception as e:
        print(f"❌ Error al inicializar Firebase: {e}")

def authenticate(username, password):
    """Autentica usuario y retorna objeto Usuario si es válido"""
    from controladores import controlador_usuario_admin, controlador_usuario_cliente
    
    # Buscar en admin
    usuario_admin = controlador_usuario_admin.confirmarDatosAdm(username, password)
    if usuario_admin:
        return Usuario(
            id=usuario_admin['id'],
            nombres=usuario_admin['nombres'],
            apellidos=usuario_admin['apellidos'],
            correo=usuario_admin['correo'],
            tipo_usuario_id=usuario_admin['tipo_usuarioid']
        )
    
    # Buscar en clientes
    usuario_cliente = controlador_usuario_cliente.get_usuario_correo(username)
    if usuario_cliente and encstringsha256(password) == usuario_cliente['contrasenia']:
        return Usuario(
            id=usuario_cliente['id'],
            nombres=usuario_cliente['nombres'],
            apellidos=usuario_cliente['apellidos'],
            correo=usuario_cliente['correo'],
            tipo_usuario_id=usuario_cliente.get('tipo_usuarioid', 3)
        )
    
    return None


@app.route("/auth", methods=['POST'])
def login():
    """Endpoint de autenticación que genera JWT"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"msg": "Usuario y contraseña requeridos"}), 400
        
        user = authenticate(username, password)
        
        if not user:
            return jsonify({"msg": "Credenciales incorrectas"}), 401
        
        # Crear token con información del usuario
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'nombres': user.nombres,
                'correo': user.correo,
                'tipo_usuario': user.tipo_usuario_id
            }
        )
        
        return jsonify(access_token=access_token), 200
    
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# Callback opcional para cargar usuario desde el token
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    from controladores import controlador_usuario_cliente
    usuario = controlador_usuario_cliente.get_usuario_id(identity)
    
    if usuario:
        return Usuario(
            id=usuario['id'],
            nombres=usuario['nombres'],
            apellidos=usuario['apellidos'],
            correo=usuario['correo']
        )
    return None


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
            controlador_bitacora.registrar_bitacora(usuarioid=usuario.get("id"))
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
        fecha_nacimiento = body.get("fecha_nacimiento")

        usuario_id = controlador_usuario_cliente.register_usuario_cliente(nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia,fecha_nacimiento)
        if usuario_id == 0:
            msg = 'Error al resgistrar usuario'
            data = { 'usuario_id' : usuario_id }
        else:
            msg = 'Usuario registrado exitosamente'
            data = { 'usuario_id' : usuario_id }

        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


################## REDES SOCIALES #####################
import firebase_admin
from firebase_admin import auth as firebase_auth
import secrets

@app.route("/login_google", methods=['POST'])
def login_google():
    """
    Login con Google usando Firebase Authentication
    
    Body request:
    {
        "body_request": {
            "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE4MmU...",
            "display_name": "Juan Perez",
            "email": "juan.perez@gmail.com",
            "photo_url": "https://lh3.googleusercontent.com/..."
        }
    }
    """
    try:
        body = request.json.get('body_request', {})
        
        id_token = body.get("id_token")
        display_name = body.get("display_name", "")
        email = body.get("email", "")
        photo_url = body.get("photo_url", "")
        
        if not id_token:
            return response_error("Token de Google requerido")
        
        # 1. VERIFICAR TOKEN DE GOOGLE CON FIREBASE
        try:
            decoded_token = firebase_auth.verify_id_token(id_token, check_revoked=False)
            firebase_uid = decoded_token['uid']
            email_verificado = decoded_token.get('email', email)
            
            print(f"✅ Token válido para: {email_verificado}")
            
        except firebase_auth.InvalidIdTokenError as e:
            print(f"❌ Token inválido: {e}")
            return response_error("Token de Google inválido o expirado")
        except Exception as e:
            print(f"❌ Error al verificar token: {e}")
            return response_error(f"Error al verificar token: {str(e)}")
        
        # 2. BUSCAR SI EL USUARIO YA EXISTE EN LA BD
        usuario_existente = controlador_usuario_cliente.get_usuario_correo(email_verificado)
        
        if usuario_existente:
            # Usuario existente - LOGIN
            usuario_id = usuario_existente['id']
            msg = "Inicio de sesión exitoso"
            es_nuevo_usuario = False
            
            data = {
                "id": usuario_existente['id'],
                "nombres": usuario_existente['nombres'],
                "apellidos": usuario_existente['apellidos'],
                "correo": usuario_existente['correo'],
                "doc_identidad": usuario_existente.get('doc_identidad', ''),
                "telefono": usuario_existente.get('telefono', ''),
                "genero": usuario_existente.get('genero', 1),
                "fecha_nacimiento": str(usuario_existente.get('fecha_nacimiento', '')),
                "img_usuario": usuario_existente.get('img_usuario') or photo_url,
                "disponibilidad": usuario_existente.get('disponibilidad', 1),
                "tipo_usuarioid": usuario_existente.get('tipo_usuarioid', 3),
                "es_nuevo_usuario": es_nuevo_usuario
            }
        
        else:
            # Usuario nuevo - REGISTRO AUTOMÁTICO
            nombre_completo = display_name.strip()
            partes_nombre = nombre_completo.split(' ', 1)
            
            nombres = partes_nombre[0] if len(partes_nombre) > 0 else "Usuario"
            apellidos = partes_nombre[1] if len(partes_nombre) > 1 else "Google"
            
            doc_identidad = "00000000"
            genero = 1
            telefono = "999999999"
            
            import bd
            contrasenia_temporal = encstringsha256(secrets.token_urlsafe(32))
            
            sql = """
                INSERT INTO usuario 
                (nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia, img_usuario, disponibilidad, TIPO_USUARIOid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, 3)
            """
            
            try:
                usuario_id = bd.sql_execute_lastrowid(
                    sql,
                    (nombres, apellidos, doc_identidad, genero, telefono, email_verificado, contrasenia_temporal, photo_url)
                )
                
                if usuario_id <= 0:
                    return response_error("Error al registrar usuario: ID inválido")
                
                msg = "Usuario registrado exitosamente con Google"
                es_nuevo_usuario = True
                
                data = {
                    "id": usuario_id,
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "correo": email_verificado,
                    "doc_identidad": doc_identidad,
                    "telefono": telefono,
                    "genero": genero,
                    "fecha_nacimiento": "",
                    "img_usuario": photo_url,
                    "disponibilidad": 1,
                    "tipo_usuarioid": 3,
                    "es_nuevo_usuario": es_nuevo_usuario
                }
                
                print(f"✅ Usuario registrado con ID: {usuario_id}")
                
            except Exception as e_insert:
                print(f"❌ Error al insertar usuario: {e_insert}")
                import traceback
                traceback.print_exc()
                return response_error(f"Error al insertar usuario en BD: {str(e_insert)}")
        
        # ✅ GENERAR TOKEN JWT USANDO FLASK-JWT-EXTENDED
        access_token = create_access_token(
            identity=str(usuario_id),
            additional_claims={
                'nombres': data['nombres'],
                'correo': email_verificado,
                'tipo_usuario': data['tipo_usuarioid']
            }
        )
        
        print(f"✅ Token JWT generado para usuario {usuario_id}")
        
        # Registrar bitácora
        controlador_bitacora.registrar_bitacora(usuarioid=usuario_id)
        
        # ✅ RESPUESTA CON TOKEN
        return jsonify({
            "status": 1,
            "mensaje": msg,
            "data": data,
            "token": access_token  # ✅ TOKEN JWT
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return response_error(f"Error en login con Google: {str(e)}")
#####

# GITHUB

@app.route("/login_github", methods=['POST'])
def login_github():
    """
    Login con GitHub OAuth
    
    Body request:
    {
        "body_request": {
            "code": "abc123..."
        }
    }
    """
    try:
        body = request.json.get('body_request', {})
        code = body.get("code")
        
        if not code:
            return response_error("Código de GitHub requerido")
        
        # 1. ✅ INTERCAMBIAR CÓDIGO POR ACCESS_TOKEN
        import requests
        from dotenv import load_dotenv
        
        # ✅ CARGAR .env DESDE LA CARPETA DEL PROYECTO
        basedir = os.path.abspath(os.path.dirname(__file__))
        dotenv_path = os.path.join(basedir, '.env')
        
        # Intentar cargar .env si existe
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            print(f"✅ Archivo .env cargado desde: {dotenv_path}")
        else:
            print(f"⚠️ Archivo .env no encontrado en: {dotenv_path}")
        
        # Obtener credenciales
        GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', 'Ov23liyY7OsCPVbgDH4p')
        GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
        
        if not GITHUB_CLIENT_SECRET or GITHUB_CLIENT_SECRET == 'TU_GITHUB_CLIENT_SECRET':
            return response_error("GitHub Client Secret no configurado en el servidor")
        
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        }
        
        try:
            token_response = requests.post(
                token_url,
                data=token_data,
                headers={"Accept": "application/json"},
                timeout=10
            )
            
            if token_response.status_code != 200:
                print(f"❌ Error de GitHub: {token_response.text}")
                return response_error("Error al obtener token de GitHub")
            
            token_json = token_response.json()
            access_token = token_json.get("access_token")
            
            if not access_token:
                error_msg = token_json.get("error_description", "No se recibió access_token")
                print(f"❌ Error en respuesta de GitHub: {error_msg}")
                return response_error(f"Error de GitHub: {error_msg}")
            
            print(f"✅ Access token de GitHub obtenido correctamente")
            
        except requests.exceptions.Timeout:
            print("❌ Timeout al conectar con GitHub")
            return response_error("Error de conexión con GitHub")
        except Exception as e:
            print(f"❌ Error al obtener token: {e}")
            return response_error(f"Error al obtener token: {str(e)}")
        
        # 2. ✅ OBTENER INFORMACIÓN DEL USUARIO
        try:
            user_response = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                },
                timeout=10
            )
            
            if user_response.status_code != 200:
                print(f"❌ Error al obtener datos de usuario: {user_response.text}")
                return response_error("Error al obtener datos de usuario de GitHub")
            
            user_data = user_response.json()
            
            # 3. ✅ OBTENER EMAIL (puede ser privado en GitHub)
            email = user_data.get("email")
            
            if not email:
                email_response = requests.get(
                    "https://api.github.com/user/emails",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json"
                    },
                    timeout=10
                )
                
                if email_response.status_code == 200:
                    emails = email_response.json()
                    # Buscar el email principal y verificado
                    for e in emails:
                        if e.get("primary") and e.get("verified"):
                            email = e.get("email")
                            break
            
            if not email:
                return response_error("No se pudo obtener el email de GitHub. Verifique que su email esté público o agregue el scope 'user:email'")
            
            github_id = str(user_data.get("id"))
            name = user_data.get("name") or user_data.get("login", "Usuario GitHub")
            login = user_data.get("login")
            avatar_url = user_data.get("avatar_url", "")
            
            print(f"✅ Datos de GitHub obtenidos para: {email} (login: {login})")
            
        except requests.exceptions.Timeout:
            print("❌ Timeout al obtener datos de usuario")
            return response_error("Error de conexión con GitHub")
        except Exception as e:
            print(f"❌ Error al obtener datos de usuario: {e}")
            return response_error(f"Error al obtener datos: {str(e)}")
        
        # 4. BUSCAR SI EL USUARIO YA EXISTE EN LA BD
        usuario_existente = controlador_usuario_cliente.get_usuario_correo(email)
        
        if usuario_existente:
            # Usuario existente - LOGIN
            usuario_id = usuario_existente['id']
            msg = "Inicio de sesión exitoso con GitHub"
            es_nuevo_usuario = False
            
            data = {
                "id": usuario_existente['id'],
                "nombres": usuario_existente['nombres'],
                "apellidos": usuario_existente['apellidos'],
                "correo": usuario_existente['correo'],
                "doc_identidad": usuario_existente.get('doc_identidad', ''),
                "telefono": usuario_existente.get('telefono', ''),
                "genero": usuario_existente.get('genero', 1),
                "fecha_nacimiento": str(usuario_existente.get('fecha_nacimiento', '')),
                "img_usuario": usuario_existente.get('img_usuario') or avatar_url,
                "disponibilidad": usuario_existente.get('disponibilidad', 1),
                "tipo_usuarioid": usuario_existente.get('tipo_usuarioid', 3),
                "es_nuevo_usuario": es_nuevo_usuario
            }
        
        else:
            # Usuario nuevo - REGISTRO AUTOMÁTICO
            partes_nombre = name.split(' ', 1)
            nombres = partes_nombre[0] if len(partes_nombre) > 0 else login
            apellidos = partes_nombre[1] if len(partes_nombre) > 1 else "GitHub"
            
            doc_identidad = "00000000"
            genero = 1
            telefono = "999999999"
            
            import bd
            contrasenia_temporal = encstringsha256(secrets.token_urlsafe(32))
            
            sql = """
                INSERT INTO usuario 
                (nombres, apellidos, doc_identidad, genero, telefono, correo, contrasenia, img_usuario, disponibilidad, TIPO_USUARIOid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, 3)
            """
            
            try:
                usuario_id = bd.sql_execute_lastrowid(
                    sql,
                    (nombres, apellidos, doc_identidad, genero, telefono, email, contrasenia_temporal, avatar_url)
                )
                
                if usuario_id <= 0:
                    return response_error("Error al registrar usuario: ID inválido")
                
                msg = "Usuario registrado exitosamente con GitHub"
                es_nuevo_usuario = True
                
                data = {
                    "id": usuario_id,
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "correo": email,
                    "doc_identidad": doc_identidad,
                    "telefono": telefono,
                    "genero": genero,
                    "fecha_nacimiento": "",
                    "img_usuario": avatar_url,
                    "disponibilidad": 1,
                    "tipo_usuarioid": 3,
                    "es_nuevo_usuario": es_nuevo_usuario
                }
                
                print(f"✅ Usuario registrado con ID: {usuario_id}")
                
            except Exception as e_insert:
                print(f"❌ Error al insertar usuario: {e_insert}")
                import traceback
                traceback.print_exc()
                return response_error(f"Error al insertar usuario en BD: {str(e_insert)}")
        
        # ✅ GENERAR TOKEN JWT USANDO FLASK-JWT-EXTENDED
        access_token_jwt = create_access_token(
            identity=str(usuario_id),
            additional_claims={
                'nombres': data['nombres'],
                'correo': email,
                'tipo_usuario': data['tipo_usuarioid']
            }
        )
        
        print(f"✅ Token JWT generado para usuario {usuario_id}")
        
        # Registrar bitácora
        controlador_bitacora.registrar_bitacora(usuarioid=usuario_id)
        
        # ✅ RESPUESTA CON TOKEN
        return jsonify({
            "status": 1,
            "mensaje": msg,
            "data": data,
            "token": access_token_jwt  # ✅ TOKEN JWT
        }), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return response_error(f"Error en login con GitHub: {str(e)}")

#######

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)