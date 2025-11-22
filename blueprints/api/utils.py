from flask import jsonify


def create_api(msg,data):
    try:
        return response_success(msg,data)
    except Exception as e:
        return response_error(str(e))


def response_success(message, data=None, status_code=200):
    """Respuesta exitosa estándar"""
    response = {
        "status": 1,
        "mensaje": message,
        "data": data or {}
    }
    return jsonify(response), status_code

def response_error(error, status_code=400):
    """Respuesta de error estándar"""
    response = {
        "status": -1,
        "mensaje": str(error),
        "data": error or {}
    }
    return jsonify(response), status_code

def response_error_msg(message, data=None, status_code=400):
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