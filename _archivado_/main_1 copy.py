



@app.route('/api/session-data', methods=['GET'])
def get_session_data():
    if 'usuario' in session:
        return jsonify({
            'usuario': session.get('usuario', ''),
            'tipoid': session.get('tipo_usuarioid', ''),
            'nombres': session.get('nombre_c', ''),
            'doc_identidad': session.get('doc_identidad', ''),
            'genero': session.get('genero', ''),
            'fecha_nacimiento': session.get('fecha_nacimiento', ''),
            'telefono': session.get('telefono', ''),
            'correo': session.get('username', '')
        })
    return jsonify({'error': 'No session data'}), 401


@app.route('/logout_admin')
def logout_admin():
    session.pop('usuario', None)  # Eliminar la sesión
    return redirect(url_for('login_admin'))  # Redirigir al login


@app.route("/error_adm")
def error_adm():
    return render_template("error_admin.html")


@app.route('/cuenta_administrativa')
@login_requerido # Decorador
def cuenta_administrativa():
    return render_template('cuenta_administrativa.html')


@app.route("/dashboard")
@login_requerido #Decorador
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login_admin'))
    return render_template("dashboard.html")






@app.route("/agregar_marca")
@login_requerido
def formulario_agregar_marca():
    return render_template("agregar_marca.html")


@app.route("/guardar_marca", methods=["POST"])
@login_requerido
def guardar_marca():
    marca = request.form["marca"]

    logo= request.files["logo"]
    logo_binario = logo.read()

    banner = request.files["banner"]

    if banner.filename == '':
        banner_binario = ''
    else:
        banner_binario = banner.read()

    objMarca = clsMarca(
        p_id = None,
        p_marca = marca,
        p_img_logo = logo_binario,
        p_img_banner = banner_binario,
        p_fecha_registro = None,
        p_disponibilidad = None
    )
    controlador_marcas.insertar_marca(objMarca.marca,objMarca.img_logo,objMarca.img_banner)
    return redirect("/listado_marcas")


@app.route("/listado_marcas")
@login_requerido
def marcas():
    marcas = controlador_marcas.obtener_listado_marcas()
    return render_template("listado_marcas.html", marcas=marcas, active='marcas')


@app.route("/listado_marcas_buscar")
@login_requerido
def marcas_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    marcas = controlador_marcas.buscar_listado_marcas_nombre(nombreBusqueda)

    return render_template("listado_marcas.html", marcas=marcas, active='marcas' , nombreBusqueda = nombreBusqueda)


@app.route("/eliminar_marca", methods=["POST"])
@login_requerido
def eliminar_marca():
    controlador_marcas.eliminar_marca(request.form["id"])
    return redirect("/listado_marcas")


@app.route("/formulario_editar_marca=<int:id>")
@login_requerido
def editar_marca(id):
    marca = controlador_marcas.obtener_listado_marca_por_id(id)
    return render_template("editar_marca.html", marca=marca)


@app.route("/actualizar_marca", methods=["POST"])
@login_requerido
def actualizar_marca():
    id = request.form["id"]

    marca_element = controlador_marcas.obtener_imgs_marca_disponible_por_id(id)

    marca = request.form["marca"]
    disponibilidad = request.form["disponibilidad"]
    logo= request.files["logo"]
    banner = request.files["banner"]

    if logo.filename == '':
        logo_binario = marca_element[1]
    else:
        logo_binario = logo.read()

    if banner.filename == '':
        banner_binario = marca_element[2]
    else:
        banner_binario = banner.read()

    objMarca = clsMarca(
        p_id = id,
        p_marca = marca,
        p_img_logo = logo_binario,
        p_img_banner = banner_binario,
        p_fecha_registro = None,
        p_disponibilidad = disponibilidad
    )

    controlador_marcas.actualizar_marca(objMarca.marca,objMarca.img_logo,objMarca.img_banner,objMarca.disponibilidad,objMarca.id)
    return redirect("/listado_marcas")



    # CARACTERISTICAS









@app.route("/listado_caracteristicas_buscar")
@login_requerido
def caracteristicas_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
        categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
        caracteristicas = controlador_caracteristicas.buscar_listado_Caracteristicas_nombre(nombreBusqueda)
        categorias = controlador_categorias.obtener_categorias()
        subcategorias =controlador_subcategorias.obtener_subcategorias()
        return render_template("listado_caracteristicas.html", caracteristicas = caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro , subcategorias=subcategorias , categorias = categorias , nombreBusqueda = nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_caracteristicas")
@login_requerido
def caracteristicas():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        subcategoriasFiltro = controlador_subcategorias.obtener_subcategoriasXnombre()
        categoriasFiltro = controlador_categorias.obtener_categoriasXnombre()
        caracteristicas = controlador_caracteristicas.obtener_listado_Caracteristicas()
        categorias = controlador_categorias.obtener_categorias()
        subcategorias = controlador_subcategorias.obtener_subcategorias()
        return render_template("listado_caracteristicas.html", caracteristicas=caracteristicas, categoriasFiltro=categoriasFiltro, subcategoriasFiltro=subcategoriasFiltro, subcategorias=subcategorias, categorias=categorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_caracteristica")
@login_requerido
def formulario_agregar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        categorias = controlador_categorias.obtener_categoriasXnombre()
        subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
        return render_template("agregar_caracteristica.html", subcategorias=subcategorias, categorias=categorias)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_caracteristica", methods=["POST"])
@login_requerido
def guardar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        campo = request.form["campo"]
        subcategoria_id = request.form["subcategorySelect"]

        objCar = clsCaracteristica(
            p_id = None,
            p_campo = campo,
            p_disponibilidad = None
        )

        id_carac = controlador_caracteristicas.insertar_caracteristica(objCar.campo)

        objCarSub = clsCaracteristicasSubcategoria(
            p_CARACTERISTICAid = id_carac,
            p_subcategoriaid = subcategoria_id
        )

        controlador_caracteristicas.insertar_caracteristica_subcategoria(objCarSub.CARACTERISTICAid, objCarSub.subcategoriaid)
        return redirect("/listado_caracteristicas")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_caracteristica", methods=["POST"])
@login_requerido
def eliminar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_caracteristicas.eliminar_caracteristica(request.form["id"])
        return redirect("/listado_caracteristicas")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_caracteristica=<int:id>")
@login_requerido
def editar_caracteristica(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        carac = controlador_caracteristicas.obtener_caracteristica_por_id(id)
        sub_id = controlador_caracteristicas.obtener_carac_subcat_por_carac_id(id)
        categorias = controlador_categorias.obtener_categoriasXnombre()
        subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
        return render_template("editar_caracteristica.html", caracteristica=carac, categorias=categorias, subcategorias=subcategorias, sub_id=sub_id)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_caracteristica", methods=["POST"])
@login_requerido
def actualizar_caracteristica():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        sub_id = request.form["sub_id"]
        campo = request.form["campo"]
        disp = request.form["disponibilidad"]
        subcategoria_id = request.form["subcategorySelect"]

        objCar = clsCaracteristica(
            p_id = id,
            p_campo = campo,
            p_disponibilidad = disp
        )

        objCarSub1 = clsCaracteristicasSubcategoria(
            p_CARACTERISTICAid = id,
            p_subcategoriaid = sub_id
        )

        objCarSub2 = clsCaracteristicasSubcategoria(
            p_CARACTERISTICAid = id,
            p_subcategoriaid = subcategoria_id
        )

        controlador_caracteristicas.actualizar_caracteristica(objCar.campo, objCar.disponibilidad, objCarSub2.subcategoriaid, objCarSub1.subcategoriaid, objCar.id)
        return redirect("/listado_caracteristicas")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


















@app.route("/cambiar_contrasenia=<int:id>")
@login_requerido
def cambiar_contrasenia(id):
    usuario = controlador_empleados.obtener_usuario_por_id(id)
    clave_default = controlador_empleados.clave_default_empleado()
    clave_actual = None
    if usuario[9] == controlador_empleados.clave_default_empleado():
        clave_actual = clave_default
    return render_template("nueva_contrasenia_admin.html", usuario=usuario , clave_actual = clave_actual)


@app.route("/guardar_contrasenia_empleado", methods=["POST"])
@login_requerido
def guardar_contrasenia_empleado():
    id = request.form["id"]
    contrasenia = request.form["contrasenia"]
    confcontrasenia = request.form["confcontrasenia"]
    password = encstringsha256(contrasenia)
    if contrasenia == confcontrasenia:
        controlador_empleados.cambiar_contrasenia_usuario(password,id)
        return redirect("/dashboard")
    else:
        return redirect("/cambiar_contrasenia="+id)


@app.route("/empleados_listado")
@login_requerido
def empleados_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuarios = controlador_empleados.obtener_listado_usuarios_empleados()
        tipos_usuarios = controlador_tipos_usuario.obtener_tipos_usuario()
        imagenes = controlador_empleados.obtener_listado_imagenes_usuario_empleado()
        return render_template("listado_empleados.html", usuarios=usuarios, tipos_usuarios=tipos_usuarios, imagenes=imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/empleados_listado_buscar")
@login_requerido
def empleados_listado_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        usuarios = controlador_empleados.buscar_listado_usuarios_empleados_nombre(nombreBusqueda)
        tipos_usuarios = controlador_tipos_usuario.obtener_tipos_usuario()
        imagenes = controlador_empleados.obtener_listado_imagenes_usuario_empleado()
        return render_template("listado_empleados.html", usuarios=usuarios, tipos_usuarios=tipos_usuarios, nombreBusqueda=nombreBusqueda, imagenes=imagenes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/ver_empleado=<int:id>")
@login_requerido
def ver_empleado(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_empleados.ver_info_usuario_empleado(id)
        imagen = controlador_empleados.obtener_imagen_usuario_empleado_id(id)
        return render_template("ver_usuario_empleado.html", usuario=usuario, imagen=imagen)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_empleado")
@login_requerido
def formulario_agregar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_empleado.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_empleado", methods=["POST"])
@login_requerido
def guardar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        doc_identidad = request.form["doc_identidad"]

        # Verificar si se subió una imagen
        img_usuario = request.files["img_usuario"].read() if "img_usuario" in request.files and request.files["img_usuario"].filename != '' else None

        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        # contraseña = request.form["contraseña"]  # Aquí se mantiene la contraseña sin cifrado

        objEmp = clsUsuario(
            p_id = None,
            p_nombres=nombres,
            p_apellidos=apellidos,
            p_doc_identidad=doc_identidad,
            p_img_usuario=img_usuario,
            p_genero=genero,
            p_fecha_nacimiento=fecha_nacimiento,
            p_telefono=telefono,
            p_correo=correo,
            p_contrasenia = controlador_empleados.clave_default_empleado() ,
            p_disponibilidad=1,
            p_fecha_registro=None,
            p_TIPO_USUARIOid=2
        )

    # Verificar si el correo ya existe
        if controlador_empleados.verificar_correo_existente(objEmp.correo):
            error = "El correo se encuentra registrado. Intente con otro correo."
            return render_template("agregar_empleado.html", error=error, nombres=nombres, apellidos=apellidos, doc_identidad=doc_identidad, genero=genero, fecha_nacimiento=fecha_nacimiento, telefono=telefono, correo=correo)

        controlador_empleados.insertar_usuario(
            objEmp.nombres, objEmp.apellidos, objEmp.doc_identidad, objEmp.img_usuario, objEmp.genero, 
            objEmp.fecha_nacimiento, objEmp.telefono, objEmp.correo, objEmp.contrasenia, objEmp.disponibilidad
        )
        return redirect("/empleados_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_empleado", methods=["POST"])
@login_requerido
def actualizar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        doc_identidad = request.form["doc_identidad"]

        img_usuario = request.files["img_usuario"].read() if "img_usuario" in request.files and request.files["img_usuario"].filename != '' else None

        genero = request.form["genero"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        # contraseña = request.form["contraseña"]  # Aquí también se mantiene la contraseña sin cifrado
        disponibilidad = request.form["disponibilidad"]

        # epassword = encstringsha256(contraseña)
        objUsuario = clsUsuario(
            p_id=id,
            p_nombres=nombres,
            p_apellidos=apellidos,
            p_doc_identidad=doc_identidad,
            p_img_usuario=img_usuario,
            p_genero=genero,
            p_fecha_nacimiento=fecha_nacimiento,
            p_telefono=telefono,
            p_correo=correo,
            p_contrasenia = controlador_empleados.clave_default_empleado() ,
            p_disponibilidad=disponibilidad,
            p_fecha_registro=None,
            p_TIPO_USUARIOid=2
        )

        controlador_empleados.actualizar_usuario_empleado(
            objUsuario.nombres, objUsuario.apellidos, objUsuario.doc_identidad, objUsuario.img_usuario, objUsuario.genero,
            objUsuario.fecha_nacimiento, objUsuario.telefono, objUsuario.correo, objUsuario.disponibilidad, objUsuario.id
        )
        return redirect("/empleados_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_empleado=<int:id>")
@login_requerido
def editar_empleado(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        usuario = controlador_empleados.obtener_usuario_por_id(id)
        imagen = controlador_empleados.obtener_imagen_usuario_empleado_id(id)
        return render_template("editar_empleado.html", usuario=usuario, imagen=imagen)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_empleado", methods=["POST"])
@login_requerido
def eliminar_empleado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_empleados.eliminar_usuario(request.form["id"])
        return redirect("/empleados_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa












@app.route("/listado_tipos_novedad")
@login_requerido
def listado_tipos_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_novedad = controlador_tipos_novedad.obtener_listado_tipos_novedad()
        return render_template("listado_tipos_novedad.html", tipos_novedad=tipos_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_novedad")
@login_requerido
def formulario_agregar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_novedad.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_novedad", methods=["POST"])
@login_requerido
def guardar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre_tipo = request.form["nombre_tipo"]
        controlador_tipos_novedad.insertar_tipo_novedad(nombre_tipo)
        return redirect("/listado_tipos_novedad")  # Aquí se muestra el listado de tipos de novedades
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_novedad", methods=["POST"])
@login_requerido
def eliminar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_tipos_novedad.eliminar_tipo_novedad(request.form["id"])
        return redirect("/listado_tipos_novedad")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_novedad=<int:id>")
@login_requerido
def editar_tipo_novedad(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo_novedad = controlador_tipos_novedad.obtener_tipo_novedad_por_id(id)
        id_tipo = id
        return render_template("editar_tipo_novedad.html", tipo_novedad=tipo_novedad, id_tipo=id_tipo)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_novedad", methods=["POST"])
@login_requerido
def actualizar_tipo_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre_tipo = request.form["nombre_tipo"]
        disponibilidad = request.form["disponibilidad"]
        controlador_tipos_novedad.actualizar_tipo_novedad(nombre_tipo, disponibilidad, id)
        return redirect("/listado_tipos_novedad")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_novedad")
@login_requerido
def formulario_agregar_novedad():
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
    return render_template("agregar_novedad.html", marcas=marcas, subcategorias=subcategorias, categorias = categorias, tipos_novedad=tipos_novedad, tipos_img_novedad = tipos_img_novedad)


@app.route("/guardar_novedad", methods=["POST"])
@login_requerido
def guardar_novedad():
    tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()

    nombre = request.form["nombre"]
    titulo = request.form["titulo"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    terminos = request.form["terminos"]
    marca_id = request.form["marca"]
    subcategoria_id = request.form["subcategorySelect"]
    tipo_novedad_id = request.form["tipo_novedad"]

    idNovedad = controlador_novedades.insertarNovedad(
        nombre,
        titulo,
        fecha_inicio,
        fecha_vencimiento,
        terminos,
        marca_id,
        subcategoria_id,
        tipo_novedad_id
    )

    files = request.files.getlist('imgNovedad')
    for file in files:
        nom_file = nombre+'_'+file.filename
        data = file.read()
        controlador_imagenes_novedades.insertar_imagen_novedad(nom_file, data, 2, idNovedad)

    # return render_template('agregar_img_novedad.html', novedad_id=idNovedad, tipos_img_novedad = tipos_img_novedad)
    return redirect("/listado_novedades")


@app.route("/listado_novedades")
@login_requerido
def novedades_listado():
    novedades = controlador_novedades.obtener_listado_novedades()
    imgs_nov = controlador_imagenes_novedades.obtener_todas_imagenes_novedad()
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_marcasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategoriasXnombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias , categorias=categorias , imgs_nov = imgs_nov)


@app.route("/listado_novedades_buscar")
@login_requerido
def novedades_listado_buscar():
    nombreBusqueda = request.args.get("buscarElemento")
    novedades = controlador_novedades.buscar_listado_novedades_nombre_titulo(nombreBusqueda)
    tipos_novedad = controlador_tipos_novedad.obtener_tipos_novedad()
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    return render_template("listado_novedades.html", novedades=novedades, tipos_novedad=tipos_novedad, marcas=marcas, subcategorias=subcategorias , nombreBusqueda = nombreBusqueda)


@app.route("/ver_novedad=<int:id>")
@login_requerido
def ver_novedad(id):
    novedad = controlador_novedades.obtener_novedad_id(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    imagenes = controlador_imagenes_novedades.obtener_imagenes_novedad_id(id)
    return render_template("ver_novedad.html", novedad=novedad, marcas=marcas , subcategorias = subcategorias, id = id ,tiposNovedad = tiposNovedad , imagenes = imagenes , categorias = categorias)


@app.route("/eliminar_novedad", methods=["POST"])
@login_requerido
def eliminar_novedad():
    controlador_novedades.eliminarNovedad(request.form["id"])
    return redirect("/listado_novedades")


@app.route("/formulario_editar_novedad=<int:id>")
@login_requerido
def editar_novedad(id):
    novedad = controlador_novedades.obtenerNovedadPorId(id)
    marcas = controlador_marcas.obtener_listado_marcas_nombre()
    categorias = controlador_categorias.obtener_categoriasXnombre()
    subcategorias = controlador_subcategorias.obtener_subcategorias()
    tiposNovedad = controlador_tipos_novedad.obtener_tipos_novedad()
    return render_template("editar_novedad.html", novedad=novedad, marcas=marcas, subcategorias=subcategorias, tipos_novedad=tiposNovedad, novedad_id = id , categorias = categorias)


@app.route("/actualizar_novedad", methods=["POST"])
@login_requerido
def actualizar_novedad():
    id = request.form["id"]
    nombre = request.form["nombre"]
    titulo = request.form["titulo"]
    fecha_inicio = request.form["fecha_inicio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    terminos = request.form["terminos"]
    disponibilidad = request.form["disponibilidad"]
    marca_id = request.form["marca_id"]
    subcategoria_id = request.form["subcategorySelect"]
    if (subcategoria_id == "null" or subcategoria_id == None or subcategoria_id == 0):
        subcategoria_id = None
    tipo_novedad_id = request.form["tipo_novedad_id"]

    imagen = request.files["imagen"].read() if "imagen" in request.files else None

    controlador_novedades.actualizarNovedad(nombre, titulo, fecha_inicio, fecha_vencimiento, terminos, disponibilidad, marca_id, subcategoria_id, tipo_novedad_id, imagen, id)
    return redirect("/listado_novedades")


@app.route("/guardar_img_novedad", methods=["POST"])
@login_requerido
def guardar_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        novedad_id = request.form["novedad_id"]
        nomImagen = request.form["nomImagen"]
        tipo_img_novedad_id = request.form["tipo_img_novedad"]
        img = request.files["imagen"]

        if img:
            imagen = img.read()
            controlador_imagenes_novedades.insertar_imagen_novedad(nomImagen, imagen, tipo_img_novedad_id, novedad_id)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_img_novedad=<int:novedad_id>")
@login_requerido
def formulario_agregar_img_novedad(novedad_id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
        return render_template("agregar_img_novedad.html", novedad_id=novedad_id, tipos_img_novedad=tipos_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/img_novedades_listado=<int:novedad_id>")
@login_requerido
def img_novedades_listado(novedad_id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        novedad = controlador_novedades.obtenerNovedadPorId(novedad_id)
        img_novedades = controlador_imagenes_novedades.obtener_imagenes_novedad_por_id(novedad_id=novedad_id)
        tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
        return render_template("listado_img_novedades.html", img_novedades=img_novedades, novedad_id=novedad_id, novedad = novedad , tipos_img_novedad = tipos_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_img_novedad", methods=["POST"])
@login_requerido
def eliminar_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_imagenes_novedades.eliminar_imagen_novedad(request.form["id"])
        novedad_id = request.form["novedad_id"]
        return redirect(f"/img_novedades_listado={novedad_id}")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_img_novedad=<int:id>")
@login_requerido
def editar_img_novedad(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        img_nov = controlador_imagenes_novedades.obtener_imagen_novedad_por_img_id(id)
        img_novedad = controlador_imagenes_novedades.obtener_imagenes_novedad_por_id(id)
        novedad_id = controlador_imagenes_novedades.obtener_novedad_id_por_imagen_id(id)
        tipos_img_novedad = controlador_tipos_img_novedad.obtener_tipos_img_novedad_disponibles()
        return render_template("editar_img_novedad.html", img_novedad=img_novedad, tipos_img_novedad=tipos_img_novedad, novedad_id = novedad_id,id = id , img_nov = img_nov)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_img_novedad", methods=["POST"])
@login_requerido
def actualizar_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2


        id = request.form["id"]
        nom_imagen = request.form["nomImagen"]
        tipo_img_novedad_id = request.form["tipo_img_novedad"]
        novedad_id = request.form["novedad_id"]
        controlador_imagenes_novedades.actualizar_imagen_novedad(id, nom_imagen, tipo_img_novedad_id, novedad_id)
        return redirect(f"/img_novedades_listado={novedad_id}")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa






@app.route("/tipos_img_novedad_listado")
@login_requerido
def tipos_img_novedad_listado():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos_img_novedad = controlador_tipos_img_novedad.obtener_listado_tipos_img_novedad()
        return render_template("listado_tipos_img_novedad.html", tipos_img_novedad=tipos_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_img_novedad")
@login_requerido
def formulario_agregar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_img_novedad.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_img_novedad", methods=["POST"])
@login_requerido
def guardar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo = request.form["tipo"]
        controlador_tipos_img_novedad.insertar_tipo_img_novedad(tipo, 1)
        return redirect("/tipos_img_novedad_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_img_novedad=<int:id>")
@login_requerido
def editar_tipo_img_novedad(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo_img_novedad = controlador_tipos_img_novedad.obtener_tipo_img_novedad_por_id(id)
        return render_template("editar_tipo_img_novedad.html", tipo_img_novedad=tipo_img_novedad)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_img_novedad", methods=["POST"])
@login_requerido
def actualizar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        tipo = request.form["tipo"]
        disponibilidad = request.form["disponibilidad"]
        controlador_tipos_img_novedad.actualizar_tipo_img_novedad(id, tipo, disponibilidad)
        return redirect("/tipos_img_novedad_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_img_novedad", methods=["POST"])
@login_requerido
def eliminar_tipo_img_novedad():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        controlador_tipos_img_novedad.eliminar_tipo_img_novedad(id)
        return redirect("/tipos_img_novedad_listado")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa







@app.route("/ver_tipo_contenido_info=<int:id>")
@login_requerido
def ver_tipo_contenido_info(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        contenido = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
        articulos = controlador_contenido_info.obtener_datos_contenido_por_tipo(id)
        return render_template("ver_contenido_info.html", articulos=articulos, contenido=contenido)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_tipo_contenido_info")
@login_requerido
def listado_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipos = controlador_contenido_info.obtener_listado_tipos_contenido()
        return render_template("listado_tipo_contenido_info.html", tipos=tipos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_tipo_contenido_info_buscar")
@login_requerido
def listado_tipo_contenido_info_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        tipos = controlador_contenido_info.buscar_listado_tipos_contenido_nombre(nombreBusqueda)
        return render_template("listado_tipo_contenido_info.html", tipos=tipos, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_tipo_contenido_info")
@login_requerido
def formulario_agregar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_tipo_contenido_info.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_tipo_contenido_info", methods=["POST"])
@login_requerido
def guardar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        faicon_cont = request.form["icono"]
        controlador_contenido_info.insertar_tipo_contenido_info(nombre, descripcion, faicon_cont)
        return redirect("/listado_tipo_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_tipo_contenido_info", methods=["POST"])
@login_requerido
def actualizar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        faicon_cont = request.form["icono"]
        descripcion = request.form["descripcion"]
        disponibilidad = request.form["disponibilidad"]
        controlador_contenido_info.actualizar_tipo_contenido_info_por_id(nombre, descripcion, faicon_cont, disponibilidad, id)
        return redirect("/listado_tipo_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_tipo_contenido_info=<int:id>")
@login_requerido
def editar_tipo_contenido_info(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        tipo = controlador_contenido_info.obtener_tipo_contenido_info_por_id(id)
        return render_template("editar_tipo_contenido_info.html", tipo=tipo)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_tipo_contenido_info", methods=["POST"])
@login_requerido
def eliminar_tipo_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_contenido_info.eliminar_tipo_contenido_info(request.form["id"])
        return redirect("/listado_tipo_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa







@app.route("/listado_contenido_info")
@login_requerido
def listado_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        datos = controlador_contenido_info.obtener_datos_contenido()
        secciones = controlador_contenido_info.obtener_listado_tipos_contenido()
        return render_template("listado_contenido_info.html", datos=datos, secciones=secciones)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/listado_contenido_info_buscar")
@login_requerido
def listado_contenido_info_buscar():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombreBusqueda = request.args.get("buscarElemento")
        datos = controlador_contenido_info.buscar_datos_contenido_info_titulo(nombreBusqueda)
        secciones = controlador_contenido_info.obtener_listado_tipos_contenido()
        return render_template("listado_contenido_info.html", datos=datos, secciones=secciones, nombreBusqueda=nombreBusqueda)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/agregar_contenido_info")
@login_requerido
def formulario_agregar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        secciones = controlador_contenido_info.obtener_tipos_contenido()
        return render_template("agregar_contenido_info.html", secciones=secciones)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_contenido_info", methods=["POST"])
@login_requerido
def guardar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        titulo = request.form["titulo"]
        cuerpo = request.form["cuerpo"]
        tipo = request.form["tipo"]
        controlador_contenido_info.insertar_contenido_info(titulo, cuerpo, tipo)
        return redirect("/listado_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_contenido_info", methods=["POST"])
@login_requerido
def actualizar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        cuerpo = request.form["cuerpo"]
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        controlador_contenido_info.actualizar_contenido_info_por_id(titulo, cuerpo, tipo, id)
        return redirect("/listado_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_contenido_info=<int:id>")
@login_requerido
def editar_contenido_info(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        secciones = controlador_contenido_info.obtener_tipos_contenido()
        tipo = controlador_contenido_info.obtener_contenido_info_por_id(id)
        return render_template("editar_contenido_info.html", tipo=tipo, secciones=secciones)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_contenido_info", methods=["POST"])
@login_requerido
def eliminar_contenido_info():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_contenido_info.eliminar_contenido_info(request.form["id"])
        return redirect("/listado_contenido_info")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa






@app.route("/listado_estado_pedido")
@login_requerido
def listado_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        estados = controlador_estado_pedido.obtener_listado_estados_pedido()
        return render_template("listado_estados_pedidos.html", estados=estados)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_agregar_estado_pedido")
@login_requerido
def formulario_agregar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_estado_pedido.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_estado_pedido", methods=["POST"])
@login_requerido
def guardar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        controlador_estado_pedido.insertar_estado_pedido(nombre)
        return redirect("/listado_estado_pedido")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_estado_pedido", methods=["POST"])
@login_requerido
def actualizar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        controlador_estado_pedido.actualizar_estado_pedido_por_id(nombre, id)
        return redirect("/listado_estado_pedido")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_estado_pedido=<int:id>")
@login_requerido
def editar_estado_pedido(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        estado = controlador_estado_pedido.obtener_estado_pedido_por_id(id)
        return render_template("editar_estado_pedido.html", estado=estado)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_estado_pedido", methods=["POST"])
@login_requerido
def eliminar_estado_pedido():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_estado_pedido.eliminar_estado_pedido(request.form["id"])
        return redirect("/listado_estado_pedido")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa






@app.route("/listado_metodo_pago")
@login_requerido
def listado_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        metodos = controlador_metodo_pago.obtener_listado_metodo_pago()
        return render_template("listado_metodo_pago.html", metodos=metodos)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_agregar_metodo_pago")
@login_requerido
def formulario_agregar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_metodo_pago.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_metodo_pago", methods=["POST"])
@login_requerido
def guardar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        controlador_metodo_pago.insertar_metodo_pago(nombre)
        return redirect("/listado_metodo_pago")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_metodo_pago", methods=["POST"])
@login_requerido
def actualizar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        disponibilidad = request.form["disponibilidad"]
        controlador_metodo_pago.actualizar_metodo_pago_por_id(nombre, disponibilidad, id)
        return redirect("/listado_metodo_pago")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_metodo_pago=<int:id>")
@login_requerido
def editar_metodo_pago(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        metodo = controlador_metodo_pago.obtener_metodo_pago_por_id(id)
        return render_template("editar_metodo_pago.html", metodo=metodo)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_metodo_pago", methods=["POST"])
@login_requerido
def eliminar_metodo_pago():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_metodo_pago.eliminar_metodo_pago(request.form["id"])
        return redirect("/listado_metodo_pago")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa








@app.route("/listado_redes_sociales")
@login_requerido
def listado_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        redes = controlador_redes_sociales.obtener_redes_sociales()
        return render_template("listado_redes_sociales.html", redes=redes)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_agregar_redes_sociales")
@login_requerido  # Decorador
def formulario_agregar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        return render_template("agregar_redes_sociales.html")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/guardar_redes_sociales", methods=["POST"])
@login_requerido  # Decorador
def guardar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        nombre = request.form["nombre"]
        enlace = request.form["enlace"]
        icono = request.form["icono"]
        controlador_redes_sociales.insertar_redes_sociales(nombre, icono, enlace)
        return redirect("/listado_redes_sociales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_redes_sociales", methods=["POST"])
@login_requerido  # Decorador
def actualizar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        nombre = request.form["nombre"]
        enlace = request.form["enlace"]
        icono = request.form["icono"]
        controlador_redes_sociales.actualizar_redes_sociales_por_id(nombre, icono, enlace, id)
        return redirect("/listado_redes_sociales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_redes_sociales=<int:id>")
@login_requerido  # Decorador
def editar_redes_sociales(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        red = controlador_redes_sociales.obtener_redes_sociales_por_id(id)
        return render_template("editar_redes_sociales.html", red=red)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/eliminar_redes_sociales", methods=["POST"])
@login_requerido  # Decorador
def eliminar_redes_sociales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        controlador_redes_sociales.eliminar_redes_sociales(request.form["id"])
        return redirect("/listado_redes_sociales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa








@app.route("/listado_cupones")
@login_requerido
def listado_cupones():
    cupones = controlador_cupon.obtener_cupones()
    return render_template("listado_cupones.html", cupones = cupones)


@app.route("/formulario_agregar_cupones")
@login_requerido
def formulario_agregar_cupones():
    return render_template("agregar_cupon.html")


@app.route("/eliminar_cupones", methods=["POST"])
@login_requerido
def eliminar_cupones():
    controlador_cupon.eliminar_cupon(request.form["id"])
    return redirect("/listado_cupones")


@app.route("/guardar_cupones", methods=["POST"])
@login_requerido
def guardar_cupones():
    codigo = request.form["codigo"]
    fecha_ini = request.form["fecha_inicio"]
    fecha_ven = request.form["fecha_vencimiento"]
    cant_dcto = request.form["cant_dcto"]
    controlador_cupon.insertar_cupon(codigo,fecha_ini,fecha_ven,cant_dcto)
    return redirect("/listado_cupones")


@app.route("/formulario_editar_cupones=<int:id>")
@login_requerido
def editar_cupones(id):
    cupon = controlador_cupon.obtener_cupon_por_id(id)
    return render_template("editar_cupones.html", cupon=cupon)


@app.route("/actualizar_cupones", methods=["POST"])
@login_requerido
def actualizar_cupones():
    id = request.form["id"]
    codigo = request.form["codigo"]
    fecha_ini = request.form["fecha_inicio"]
    fecha_ven = request.form["fecha_vencimiento"]
    cant_dcto = request.form["cant_dcto"]
    disponibilidad = request.form["disponibilidad"]
    controlador_cupon.actualizar_cupon_por_id(codigo,fecha_ini,fecha_ven,cant_dcto,disponibilidad,id)
    return redirect("/listado_cupones")









@app.route("/listado_datos_principales")
def listado_datos_principales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        info = controlador_informacion_domus.obtener_informacion_domus()
        return render_template("ver_datos_principales.html", info=info)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/formulario_editar_datos_principales=<int:id>")
def editar_datos_principales(id):
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        info = controlador_informacion_domus.obtener_informacion_domus_por_id(id)
        return render_template("editar_datos_principales.html", info=info)
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa


@app.route("/actualizar_datos_principales", methods=["POST"])
def actualizar_datos_principales():
    if 'usuario' in session:
        username = session['usuario']
        tipo_id = controlador_usuario_admin.obtenerTipoU(username)  # Obtener tipo de usuario

        # Verificar si el tipo de usuario es 2
        if tipo_id == 2:
            return redirect(url_for('dashboard'))  # Redirigir al dashboard si el tipo de usuario es 2

        id = request.form["id"]
        info = controlador_informacion_domus.obtener_imgs_informacion_domus_por_id(id)

        correo = request.form["correo"]
        numero = request.form["numero"]
        descripcion = request.form["descripcion"]
        historia = request.form["historia"]
        vision = request.form["vision"]
        valores = request.form["valores"]
        mision = request.form["mision"]

        imgLogo = request.files["imglogo"]
        imgIcon = request.files["imgicon"]

        if imgLogo.filename == '':
            logo = info[1]
        else:
            logo = imgLogo.read()

        if imgIcon.filename == '':
            icon = info[2]
        else:
            icon = imgIcon.read()

        controlador_informacion_domus.actualizar_informacion_domus_por_id(correo, numero, logo, icon, descripcion, historia, vision, valores, mision, id)
        return redirect("/listado_datos_principales")
    else:
        return redirect(url_for('login_admin'))  # Redirigir al login si no hay sesión activa

















### Para admin






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)