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
from blueprints.admin.comentario import admin_comentario_bp

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
    'admin_comentario_bp',
]