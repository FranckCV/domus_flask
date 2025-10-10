


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
    admin_comentario_bp
)

# APIs
from blueprints.api import api_v1_bp
from blueprints.api import api_bp

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
    'admin_comentario_bp',
    'api_v1_bp',
    'api_bp',
]