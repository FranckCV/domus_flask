from flask import Blueprint, render_template, redirect, url_for, session , flash , request , make_response
admin_empleados_bp = Blueprint('admin_empleados', __name__)