from flask import render_template, Blueprint, request, redirect, flash, url_for, jsonify, send_file, make_response
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ubicacion_templates = os.path.join(BASE_DIR, 'templates')
listado_bp = Blueprint(
    'ventas', 
    __name__, 
    template_folder = ubicacion_templates, 
    url_prefix = '/listado'
    )




