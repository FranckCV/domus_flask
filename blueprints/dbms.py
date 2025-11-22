from flask import Blueprint, render_template, request, redirect , flash , url_for,jsonify,current_app
from bd import (
    sql_execute ,
    sql_execute_lastrowid ,
    bd_insert_lastrowid ,
    sql_select_fetchall ,
    sql_select_fetchone,
    bd_delete ,
    bd_update ,
    bd_insert 
)

dbms_bp = Blueprint('dbms', __name__)

def obtener_tablas():
    """Obtiene todas las tablas de la base de datos"""
    sql = "SHOW TABLES"
    resultado = sql_select_fetchall(sql)
    tablas = [list(tabla.values())[0] for tabla in resultado]
    return tablas

def obtener_columnas(tabla):
    """Obtiene información de las columnas de una tabla"""
    sql = f"DESCRIBE {tabla}"
    return sql_select_fetchall(sql)

def obtener_datos_tabla(tabla):
    """Obtiene todos los registros de una tabla"""
    sql = f"SELECT * FROM {tabla}"
    return sql_select_fetchall(sql)

def obtener_primary_key(tabla):
    """Obtiene el nombre de la columna primary key"""
    columnas = obtener_columnas(tabla)
    for col in columnas:
        if col['Key'] == 'PRI':
            return col['Field']
    return 'id'  # fallback


@dbms_bp.route('/gestion')
def gestion():
    """Página principal con listado de tablas"""
    tablas = obtener_tablas()
    return render_template('DBMS/GESTION.html', tablas=tablas)


@dbms_bp.route('/tabla/<nombre_tabla>')
def ver_tabla(nombre_tabla):
    """Vista de una tabla específica con sus datos"""
    try:
        columnas = obtener_columnas(nombre_tabla)
        datos = obtener_datos_tabla(nombre_tabla)
        pk = obtener_primary_key(nombre_tabla)
        return render_template('DBMS/tabla.html', 
                             tabla=nombre_tabla, 
                             columnas=columnas, 
                             datos=datos,
                             pk=pk)
    except Exception as e:
        flash(f'Error al cargar tabla: {str(e)}', 'danger')
        return redirect(url_for('dbms.gestion'))

@dbms_bp.route('/tabla/<nombre_tabla>/nuevo', methods=['GET', 'POST'])
def nuevo_registro(nombre_tabla):
    """Crear nuevo registro"""
    columnas = obtener_columnas(nombre_tabla)
    
    if request.method == 'POST':
        try:
            campos = []
            valores = []
            
            for col in columnas:
                campo = col['Field']
                # Saltar auto_increment
                if col['Extra'] == 'auto_increment':
                    continue
                    
                valor = request.form.get(campo)
                campos.append(campo)
                valores.append(valor if valor != '' else None)
            
            bd_insert_lastrowid(nombre_tabla, campos, valores)
            flash('Registro creado exitosamente', 'success')
            return redirect(url_for('ver_tabla', nombre_tabla=nombre_tabla))
            
        except Exception as e:
            flash(f'Error al crear registro: {str(e)}', 'danger')
    
    return render_template('DBMS/formulario.html', 
                         tabla=nombre_tabla, 
                         columnas=columnas,
                         datos=None,
                         accion='Nuevo')

@dbms_bp.route('/tabla/<nombre_tabla>/editar/<int:id>', methods=['GET', 'POST'])
def editar_registro(nombre_tabla, id):
    """Editar registro existente"""
    pk = obtener_primary_key(nombre_tabla)
    columnas = obtener_columnas(nombre_tabla)
    
    if request.method == 'POST':
        try:
            campos = []
            valores = []
            
            for col in columnas:
                campo = col['Field']
                # Saltar primary key
                if col['Key'] == 'PRI':
                    continue
                    
                valor = request.form.get(campo)
                campos.append(campo)
                valores.append(valor if valor != '' else None)
            
            bd_update(nombre_tabla, campos, valores, f"{pk} = %s", [id])
            flash('Registro actualizado exitosamente', 'success')
            return redirect(url_for('ver_tabla', nombre_tabla=nombre_tabla))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    # Obtener datos actuales
    sql = f"SELECT * FROM {nombre_tabla} WHERE {pk} = %s"
    datos = sql_select_fetchall(sql, [id])
    datos = datos[0] if datos else None
    
    return render_template('DBMS/formulario.html', 
                         tabla=nombre_tabla, 
                         columnas=columnas,
                         datos=datos,
                         accion='Editar')

@dbms_bp.route('/tabla/<nombre_tabla>/eliminar/<int:id>', methods=['POST'])
def eliminar_registro(nombre_tabla, id):
    """Eliminar un registro"""
    try:
        pk = obtener_primary_key(nombre_tabla)
        bd_delete(nombre_tabla, f"{pk} = %s", [id])
        flash('Registro eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('ver_tabla', nombre_tabla=nombre_tabla))

@dbms_bp.route('/api_tabla/<nombre_tabla>/actualizar-celda', methods=['POST'])
def actualizar_celda(nombre_tabla):
    """API para actualizar una celda específica (doble click)"""
    try:
        data = request.get_json()
        pk = obtener_primary_key(nombre_tabla)
        
        id_registro = data.get('id')
        columna = data.get('columna')
        valor = data.get('valor')
        
        # Validar que la columna existe
        columnas = obtener_columnas(nombre_tabla)
        nombres_columnas = [col['Field'] for col in columnas]
        
        if columna not in nombres_columnas:
            return jsonify({'success': False, 'error': 'Columna no válida'}), 400
        
        if columna == pk:
            return jsonify({'success': False, 'error': 'No se puede editar la clave primaria'}), 400
        
        bd_update(nombre_tabla, [columna], [valor], f"{pk} = %s", [id_registro])
        
        return jsonify({'success': True, 'mensaje': 'Celda actualizada'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


import os
from werkzeug.utils import secure_filename

# Carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'img')
# current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@dbms_bp.route('/api_agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        # Datos del formulario
        nombre = request.form['nombre']
        price_regular = request.form.get('price_regular')
        precio_online = request.form['precio_online']
        precio_oferta = request.form.get('precio_oferta')
        info_adicional = request.form.get('info_adicional')
        stock = request.form['stock']
        disponibilidad = request.form['disponibilidad']
        marcaid = request.form['marcaid']
        subcategoriaid = request.form['subcategoriaid']

        # Imagen
        file = request.files.get('imagen')
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Formato de archivo no permitido'}), 400

        filename = secure_filename(file.filename)
        path_guardado = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path_guardado)

        # Guardar en base de datos
        import bd
        conn = bd.obtener_conexion()
        cursor = conn.cursor()

        # Insertar producto
        sql_producto = """INSERT INTO producto 
            (nombre, price_regular, precio_online, precio_oferta, info_adicional, stock, disponibilidad, marcaid, subcategoriaid)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values_producto = (nombre, price_regular, precio_online, precio_oferta, info_adicional, stock, disponibilidad, marcaid, subcategoriaid)
        cursor.execute(sql_producto, values_producto)
        conn.commit()
        productoid = cursor.lastrowid

        # Guardar imagen (solo ruta relativa)
        ruta_relativa = f"static/img/{filename}"
        sql_img = """INSERT INTO img_producto (img_nombre, imagen, imgprincipal, productoid)
                     VALUES (%s,%s,%s,%s)"""
        cursor.execute(sql_img, (filename, ruta_relativa, 1, productoid))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Producto agregado correctamente', 'producto_id': productoid}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

