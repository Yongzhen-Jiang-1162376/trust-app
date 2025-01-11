from flask import render_template, request
from app.blueprints.main import bp
from flask_login import login_required

@bp.route('/')
@login_required
def index():
    return render_template('main/home.html')
