from flask import Blueprint, render_template, request, redirect, session, make_response , flash , url_for
from controladores import (
    controlador_usuario_cliente ,
    controlador_lista_deseos ,
)
from utils import encstringsha256

perfil_bp = Blueprint('perfil', __name__)


@perfil_bp.route("/perfil=<int:user_id>")
def perfil(user_id):
    if 'id' in session and session['id'] == user_id:
        usuario=controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
        img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)
        return render_template('perfil.html', user_id=user_id,usuario=usuario,img=img )
    else:
        return redirect('/iniciar_sesion')


@perfil_bp.route("/lista_deseos=<int:user_id>")
def lista_deseos(user_id):
    usuario=controlador_usuario_cliente.obtener_usuario_cliente_por_id(user_id)
    img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(user_id)
    lista=controlador_lista_deseos.obtenerListaDeseosConImagen(user_id)
    return render_template("listaDeseos.html",user_id=user_id,usuario=usuario,img=img, lista=lista )


@perfil_bp.route('/agregar_a_lista_deseos', methods=['POST'])
def agregar_a_lista_deseos():
    usuario_id = session.get('id')

    if not usuario_id:
        return render_template('iniciar_sesion.html', mostrar_modal=True, mensaje_modal="Regístrese para agregar a la lista de deseos")

    producto_id = request.form.get('producto_id')

    if producto_id:
        controlador_lista_deseos.agregar_a_lista_deseos(usuario_id, producto_id)
        return '', 204  
    return '', 400 


    
@perfil_bp.route("/insertar_imagen_usuario", methods=['POST'])
def imagen_usuario():
    if 'imagen' not in request.files:
        flash('No se seleccionó ninguna imagen.', 'error')
        return redirect(url_for('perfil', user_id=session.get('id')))

    imagen = request.files["imagen"]
    if imagen.filename == '':
        flash('No se seleccionó ninguna imagen.', 'error')
        return redirect(url_for('perfil', user_id=session.get('id')))

    try:
        imagen_bin = imagen.read()
        id = session.get('id')
        controlador_usuario_cliente.insertar_imagen(id,imagen_bin)
        img=controlador_usuario_cliente.obtener_imagen_usuario_cliente_id(id)
        flash('Imagen actualizada correctamente.', 'success')
    except Exception as e:
        flash(f'Error al guardar la imagen: {e}', 'error')

    return redirect(url_for('perfil', user_id=session.get('id') ))


