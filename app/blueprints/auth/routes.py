from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import bp
from app.extensions import db
from app.models.auth.models import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash


# @bp.route('/')
# def index():
#     return 'auth.index'


@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        print(email, password, remember)

        user = User.query.filter_by(email=email).first()

        print('--------- user ---------')
        print(user)
        print(check_password_hash(user.password, password) if user else False)

        if not user or not check_password_hash(user.password, password):
            error = 'Incorrect email or password'
        else:
            login_user(user, remember=remember)
            return redirect(url_for('main.index'))
    
    return render_template('auth/login.html', error=error)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        print('---------- user -----------')
        print(user)

        if user:
            return redirect(url_for('auth.login'))
        
        print('-------- registering ----------')
        print(name, email, password)

        sql = '''
            INSERT INTO auth_user
            (
                email,
                password,
                full_name,
                created_at
            )
            VALUES
            (
                :email,
                :password,
                :full_name,
                now()
            )
        '''

        params = {
            'email': email,
            'password': generate_password_hash(password),
            'full_name': name
        }

        db.session.execute(text(sql), params)
        db.session.commit()

        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/profile')
@login_required
def profile():

    print(current_user)

    return render_template('auth/profile.html', current_user=current_user)
