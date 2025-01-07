from flask import render_template, request
from flask_login import login_required
from app.blueprints.auth import bp
from app.extensions import db


@bp.route('/')
def index():
    return 'auth.index'

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        pass
    
    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        pass
    
    return render_template('auth/register.html')

