# Estructura de Blueprints para Organizar main.py

## Estructura de directorios recomendada:

```
proyecto/
├── main.py                          # Solo configuración de la app
├── blueprints/
│   ├── __init__.py
│   ├── auth.py                      # Login, registro, logout
│   ├── general.py                   # Rutas públicas principales
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── dashboard.py             # Dashboard admin
│   │   ├── categorias.py            # Crud categorías
│   │   ├── subcategorias.py         # Crud subcategorías
│   │   ├── productos.py             # Crud productos
│   │   ├── marcas.py                # Crud marcas
│   │   ├── caracteristicas.py       # Crud características
│   │   ├── empleados.py             # Crud empleados
│   │   ├── usuarios_clientes.py     # Crud clientes
│   │   ├── novedades.py             # Crud novedades
│   │   ├── configuracion.py         # Metodos pago, estados, etc
│   │   └── contenido.py             # Contenido informativo
│   ├── carrito.py                   # Carrito de compras
│   ├── pedidos.py                   # Órdenes de pedido
│   ├── perfil.py                    # Perfil de usuario
│   ├── comentarios.py               # Comentarios
│   └── api/
│       ├── __init__.py
│       ├── v1.py                    # APIs versión 1
│       └── utils.py                 # Funciones compartidas API
├── controladores/
├── clases/
└── static/
```

## Contenido de cada blueprint:

### 1. main.py (simplificado)

```python
from flask import Flask
from flask_jwt import JWT
import hashlib

# Importar blueprints
from blueprints.auth import auth_bp
from blueprints.general import general_bp
from blueprints.carrito import carrito_bp
from blueprints.pedidos import pedidos_bp
from blueprints.perfil import perfil_bp
from blueprints.comentarios import comentarios_bp
from blueprints.admin.dashboard import admin_dashboard_bp
from blueprints.admin.categorias import admin_categorias_bp
from blueprints.admin.productos import admin_productos_bp
# ... importar otros blueprints admin
from blueprints.api.v1 import api_v1_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.debug = True

# Configurar JWT
from controladores import controlador_usuario_cliente

def authenticate(username, password):
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_email(username)
    if not data:
        return None
    # ... lógica de autenticación
    return user

def identity(payload):
    user_id = payload['identity']
    # ... lógica de identidad
    return user

jwt = JWT(app, authenticate, identity)

# Context processor global
@app.context_processor
def inject_globals():
    # ... tu código actual de inject_globals
    return dict(...)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(general_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(comentarios_bp)

# Blueprints admin con prefijo
app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
app.register_blueprint(admin_categorias_bp, url_prefix='/admin')
app.register_blueprint(admin_productos_bp, url_prefix='/admin')
# ... registrar otros blueprints admin

# APIs
app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
```

### 2. blueprints/auth.py

```python
from flask import Blueprint, render_template, request, redirect, session, make_response
import hashlib
from controladores import controlador_usuario_cliente

auth_bp = Blueprint('auth', __name__)

def encstringsha256(cadena_legible):
    h = hashlib.new('sha256')
    h.update(bytes(cadena_legible, encoding='utf-8'))
    return h.hexdigest()

@auth_bp.route("/iniciar_sesion")
def iniciar_sesion():
    return render_template("iniciar_sesion.html")

@auth_bp.route("/registrate")
def registrate():
    return render_template("registrate.html")

@auth_bp.route("/registrar_cliente", methods=["POST"])
def registrar_cliente():
    # ... tu código actual
    pass

@auth_bp.route("/login", methods=['POST'])
def login():
    # ... tu código actual
    pass

@auth_bp.route("/logout")
def logout():
    session.clear()
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')
    return resp

@auth_bp.route("/cambiar_contrasenia_cliente", methods=['GET', 'POST'])
def cambiar_contrasenia_cliente():
    # ... tu código actual
    pass
```

### 3. blueprints/general.py

```python
from flask import Blueprint, render_template, request
from controladores import (
    controlador_categorias,
    controlador_marcas,
    controlador_productos,
    controlador_novedades
)

general_bp = Blueprint('general', __name__)

@general_bp.route("/")
def index():
    marcasBloque = controlador_marcas.obtener_marcas_index(10)
    productosRecientes = controlador_productos.obtenerEnTarjetasMasRecientes()
    productosPopulares = controlador_productos.obtenerEnTarjetasMasPopulares()
    novedadesBanner = controlador_novedades.obtenerBannersNovedadesRecientes()
    novedadesRecientes = controlador_novedades.obtenerNovedadesRecientes()
    return render_template("index.html", ...)

@general_bp.route("/nuestras_marcas")
def nuestras_marcas():
    # ... tu código actual
    pass

@general_bp.route("/catalogo")
def catalogo():
    # ... tu código actual
    pass

# ... otras rutas generales
```

### 4. blueprints/admin/dashboard.py

```python
from flask import Blueprint, render_template, redirect, url_for, session
from functools import wraps

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

def login_requerido(func):
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('admin_auth.login_admin'))
        return func(*args, **kwargs)
    return envoltura

@admin_dashboard_bp.route("/login_admin", methods=['GET', 'POST'])
def login_admin():
    # ... tu código actual
    pass

@admin_dashboard_bp.route("/dashboard")
@login_requerido
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('admin_auth.login_admin'))
    return render_template("dashboard.html")
```

### 5. blueprints/admin/productos.py

```python
from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from controladores import controlador_productos, controlador_marcas, etc

admin_productos_bp = Blueprint('admin_productos', __name__)

def login_requerido(func):
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('admin_dashboard.login_admin'))
        return func(*args, **kwargs)
    return envoltura

@admin_productos_bp.route("/agregar_producto")
@login_requerido
def formulario_agregar_producto():
    # ... tu código actual
    pass

@admin_productos_bp.route("/guardar_producto", methods=["POST"])
@login_requerido
def guardar_producto():
    # ... tu código actual
    pass

@admin_productos_bp.route("/listado_productos")
@login_requerido
def productos():
    # ... tu código actual
    pass

# ... otras rutas de productos
```

### 6. blueprints/api/v1.py

```python
from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from controladores import controlador_marcas, controlador_productos, etc

api_v1_bp = Blueprint('api_v1', __name__)

# Agrupar APIs por recurso

@api_v1_bp.route("/marcas", methods=["GET"])
@jwt_required()
def api_listado_marcas():
    # ... tu código actual
    pass

@api_v1_bp.route("/marcas", methods=["POST"])
@jwt_required()
def api_guardar_marca():
    # ... tu código actual
    pass

# ... organizar todas las APIs por recursos (marcas, productos, etc)
```

## Ventajas de esta estructura:

1. **Modularidad**: Cada blueprint maneja un área específica
2. **Mantenibilidad**: Fácil encontrar y modificar rutas
3. **Escalabilidad**: Agregar nuevas funcionalidades es más limpio
4. **Reutilización**: Decoradores como `login_requerido` compartidos
5. **Testing**: Más fácil de testear cada módulo
6. **Performance**: Carga de código más eficiente
7. **Equipo**: Múltiples desarrolladores pueden trabajar en paralelo

## Migrando gradualmente:

Si no quieres refactorizar todo de una vez:

1. Crea los blueprints gradualmente
2. Mueve las rutas existentes
3. Importa en main.py
4. Prueba antes de eliminar del main
5. Una vez migrado todo, simplifica main.py






# Archivos __init__.py en Estructura de Blueprints

## 1. blueprints/__init__.py (raíz de blueprints)

```python
"""
Blueprints del proyecto
Importar aquí todos los blueprints para facilitar el acceso
"""

from blueprints.auth import auth_bp
from blueprints.general import general_bp
from blueprints.carrito import carrito_bp
from blueprints.pedidos import pedidos_bp
from blueprints.perfil import perfil_bp
from blueprints.comentarios import comentarios_bp

# Blueprints Admin
from blueprints.admin import (
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
)

# APIs
from blueprints.api import api_v1_bp

__all__ = [
    'auth_bp',
    'general_bp',
    'carrito_bp',
    'pedidos_bp',
    'perfil_bp',
    'comentarios_bp',
    'admin_dashboard_bp',
    'admin_categorias_bp',
    'admin_subcategorias_bp',
    'admin_productos_bp',
    'admin_marcas_bp',
    'admin_caracteristicas_bp',
    'admin_empleados_bp',
    'admin_usuarios_clientes_bp',
    'admin_novedades_bp',
    'admin_configuracion_bp',
    'admin_contenido_bp',
    'api_v1_bp',
]
```

## 2. blueprints/admin/__init__.py

```python
"""
Blueprints de administración
"""

from blueprints.admin.dashboard import admin_dashboard_bp
from blueprints.admin.categorias import admin_categorias_bp
from blueprints.admin.subcategorias import admin_subcategorias_bp
from blueprints.admin.productos import admin_productos_bp
from blueprints.admin.marcas import admin_marcas_bp
from blueprints.admin.caracteristicas import admin_caracteristicas_bp
from blueprints.admin.empleados import admin_empleados_bp
from blueprints.admin.usuarios_clientes import admin_usuarios_clientes_bp
from blueprints.admin.novedades import admin_novedades_bp
from blueprints.admin.configuracion import admin_configuracion_bp
from blueprints.admin.contenido import admin_contenido_bp

__all__ = [
    'admin_dashboard_bp',
    'admin_categorias_bp',
    'admin_subcategorias_bp',
    'admin_productos_bp',
    'admin_marcas_bp',
    'admin_caracteristicas_bp',
    'admin_empleados_bp',
    'admin_usuarios_clientes_bp',
    'admin_novedades_bp',
    'admin_configuracion_bp',
    'admin_contenido_bp',
]
```

## 3. blueprints/api/__init__.py

```python
"""
APIs del proyecto
"""

from blueprints.api.v1 import api_v1_bp

__all__ = ['api_v1_bp']
```

## 4. main.py SIMPLIFICADO

```python
from flask import Flask
from flask_jwt import JWT
import hashlib

# Importación centralizada desde blueprints
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
    api_v1_bp,
)

from controladores import controlador_usuario_cliente

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.debug = True

# JWT
def authenticate(username, password):
    data = controlador_usuario_cliente.obtener_usuario_cliente_por_email(username)
    if not data:
        return None
    # ... lógica
    return user

def identity(payload):
    user_id = payload['identity']
    # ... lógica
    return user

jwt = JWT(app, authenticate, identity)

# Context processor
@app.context_processor
def inject_globals():
    # ... tu código actual
    return dict(...)

# Registrar blueprints públicos
app.register_blueprint(auth_bp)
app.register_blueprint(general_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(comentarios_bp)

# Registrar blueprints admin con prefijo
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

# Registrar APIs
app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
```

## 5. Ejemplo completo: blueprints/admin/productos.py

```python
from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
from controladores import (
    controlador_productos,
    controlador_marcas,
    controlador_categorias,
    controlador_subcategorias,
    controlador_imagenes_productos,
    controlador_usuario_admin,
)
from clases.clsProducto import Producto as clsProducto
from clases.clsImgProducto import ImgProducto as clsImgProducto

# Crear blueprint
admin_productos_bp = Blueprint(
    'admin_productos',
    __name__,
    template_folder='../../templates',
    static_folder='../../static'
)

def login_requerido(func):
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('admin_dashboard.login_admin'))
        return func(*args, **kwargs)
    return envoltura

def verificar_permisos_admin(func):
    """Verifica si el usuario es admin (tipo 1)"""
    @wraps(func)
    def envoltura(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('admin_dashboard.login_admin'))
        
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)
        
        # Si es empleado regular (tipo 2), redirigir al dashboard
        if tipo_id == 2:
            return redirect(url_for('admin_dashboard.dashboard'))
        
        return func(*args, **kwargs)
    return envoltura

# Rutas
@admin_productos_bp.route("/agregar_producto")
@login_requerido
@verificar_permisos_admin
def formulario_agregar_producto():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    return render_template("agregar_producto.html", 
                         marcas=marcas, 
                         subcategorias=subcategorias, 
                         categorias=categorias)

@admin_productos_bp.route("/guardar_producto", methods=["POST"])
@login_requerido
@verificar_permisos_admin
def guardar_producto():
    # ... tu código actual
    pass

@admin_productos_bp.route("/listado_productos")
@login_requerido
def productos():
    # ... tu código actual
    pass

@admin_productos_bp.route("/listado_productos_buscar")
@login_requerido
def productos_buscar():
    # ... tu código actual
    pass

# ... más rutas
```

## 6. blueprints/api/v1.py

```python
"""
API v1
Todas las rutas de API van aquí
"""

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from controladores import (
    controlador_marcas,
    controlador_productos,
    controlador_usuario_cliente,
    # ... otros controladores
)
from blueprints.api.utils import response_success, response_error

api_v1_bp = Blueprint('api_v1', __name__)

# ========== MARCAS ==========
@api_v1_bp.route("/marcas", methods=["GET"])
@jwt_required()
def obtener_marcas():
    try:
        marcas = controlador_marcas.obtener_listado_marcas()
        return response_success("Marcas obtenidas", marcas)
    except Exception as e:
        return response_error(str(e))

@api_v1_bp.route("/marcas", methods=["POST"])
@jwt_required()
def crear_marca():
    # ... tu código actual
    pass

# ========== PRODUCTOS ==========
@api_v1_bp.route("/productos", methods=["GET"])
@jwt_required()
def obtener_productos():
    # ... tu código actual
    pass

# ========== USUARIOS ==========
@api_v1_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    # ... tu código actual
    pass

# ... más rutas organizadas por recurso
```

## 7. blueprints/api/utils.py

```python
"""
Utilidades compartidas para APIs
"""

from flask import jsonify

def response_success(message, data=None, status_code=200):
    """Respuesta exitosa estándar"""
    response = {
        "status": 1,
        "mensaje": message,
        "data": data or {}
    }
    return jsonify(response), status_code

def response_error(message, data=None, status_code=400):
    """Respuesta de error estándar"""
    response = {
        "status": -1,
        "mensaje": message,
        "data": data or {}
    }
    return jsonify(response), status_code

def response_not_found(message="Recurso no encontrado"):
    """Respuesta 404 estándar"""
    return response_error(message, status_code=404)

def response_unauthorized(message="No autorizado"):
    """Respuesta 401 estándar"""
    return response_error(message, status_code=401)
```

## Resumen de lo que va en cada __init__.py:

| Archivo | Contenido |
|---------|-----------|
| `blueprints/__init__.py` | Importa TODOS los blueprints para acceso rápido |
| `blueprints/admin/__init__.py` | Importa solo blueprints admin |
| `blueprints/api/__init__.py` | Importa solo blueprints API |
| `blueprints/auth.py` | Rutas de autenticación (sin __init__) |
| `blueprints/general.py` | Rutas públicas (sin __init__) |

## Ventajas:

✅ Importaciones limpias en main.py  
✅ Organización clara y jerárquica  
✅ Fácil de encontrar blueprints  
✅ Escalable para nuevos módulos  
✅ Reutilizable en equipos grandes