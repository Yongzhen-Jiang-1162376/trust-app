from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import bp
from app.extensions import db
from app.models.auth import User
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from app.decorators import superadmin_required
from app.schemas.auth.schema import AuthUserSchema
import json


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

        # print('--------- user ---------')
        # print(user)
        # print(check_password_hash(user.password, password) if user else False)

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

        # print('---------- user -----------')
        # print(user)

        if user:
            return redirect(url_for('auth.login'))
        
        # print('-------- registering ----------')
        # print(name, email, password)

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

    # print(current_user)

    return render_template('auth/profile.html', current_user=current_user)


@bp.route('/user-manage')
@login_required
@superadmin_required()
def user_manage():

    # sql = """
    #     SELECT
    #         u.id,
    #         u.email,
    #         u.full_name,
    #         u.is_blocked,
    #         u.is_superadmin,
    #         u.title,
    #         p.id AS portfolio_id,
    #         p.group_id,
    #         p.portfolio
    #     FROM 
    #     auth_user u
    #     LEFT JOIN auth_user_portfolio up ON u.id = up.user_id
    #     LEFT JOIN hr_employee_portfolio p ON p.id = up.portfolio_id
    #     ORDER BY u.id
    # """
    
    # result = db.session.execute(text(sql)).fetchall()
    users = User.query.all()

    user_schema = AuthUserSchema(many=True)
    data = user_schema.dumps(users)

    print(data)

    return render_template('auth/user_manage.html', data=data)


@bp.route('/user-edit', methods=['GET', 'POST'])
@login_required
@superadmin_required()
def user_edit():
    if request.method == 'POST':
        pass
    
    userid = request.args.get('userid')
    
    
    data = User.query.filter_by(id=userid).one()
    
    print('-----------------user--------------------')
    # print(user)
    print(data.is_superadmin)
    print(data.is_blocked)
    
    # user_schema = AuthUserSchema()
    # data = user_schema.dumps(user)
    
    print(data)
    
    return render_template('auth/user_edit.html', data=data)
