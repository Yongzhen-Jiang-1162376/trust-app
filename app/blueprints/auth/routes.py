from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.blueprints.auth import bp
from app.extensions import db
from app.models.auth.models import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route('/')
def index():
    return 'auth.index'

@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()


    
    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('auth.login'))
        
        print('-------- registering ----------')
        print(name, email, password)

        sql = '''
            INSERT INTO auth_user
            (
                email,
                password,
                full_name
            )
            VALUES
            (
                :email,
                :password,
                :full_name
            )
        '''

        params = {
            'email': email,
            'password': generate_password_hash(password),
            'full_name': name
        }

        db.session.execute(text(sql), params)
        db.session.commit()

        return redirect('auth.login')
    
    return render_template('auth/register.html')

