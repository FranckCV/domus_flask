
import hashlib
import inspect
from werkzeug.utils import secure_filename
import os
from datetime import datetime

def encstringsha256(cadena_legible):
    h = hashlib.new('sha256')
    h.update(bytes(cadena_legible, encoding='utf-8'))
    epassword = h.hexdigest()
    return epassword


def inspect_function(request , funcion):
    firma = inspect.signature(funcion)
    valores = []
    for nombre, parametro in firma.parameters.items():
        if nombre in request.files:
            archivo = request.files[nombre]
            if archivo.filename != "":
                nuevo_nombre = save_file_folder(archivo,'')
                valores.append(nuevo_nombre)
            else:
                valores.append(request.form.get(f"{nombre}_actual"))
        else:
            valor = request.form.get(nombre)
            valores.append(valor)
    return funcion( *valores )


def save_file_folder(archivo,folder='static'):
    if archivo and '.' in archivo.filename and archivo.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
        filename_seguro = secure_filename(archivo.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_final = f"{timestamp}_{filename_seguro}"
        ruta_completa = os.path.join(folder, nombre_final)
        archivo.save(ruta_completa)
        return ruta_completa
    return None

