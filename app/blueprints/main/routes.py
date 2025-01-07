from flask import render_template, request
from app.blueprints.main import bp

@bp.route('/')
def index():
    return render_template('main/home.html')
