from flask import Blueprint, render_template, redirect, url_for, session , flash , request , make_response
admin_marcas_bp = Blueprint('admin_marcas', __name__)