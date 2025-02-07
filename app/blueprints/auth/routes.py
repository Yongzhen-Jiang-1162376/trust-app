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

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            error = 'Incorrect email or password'
        elif user.is_blocked:
            error = 'Account is blocked. Please contact admin.'
        else:
            login_user(user, remember=remember)
            return redirect(url_for('main.index'))
    
    return render_template('auth/login.html', error=error)


@bp.route('/register', methods=('GET', 'POST'))
@superadmin_required()
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('auth.login'))
        
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

    return render_template('auth/user_manage.html', data=data)


@bp.route('/user-edit', methods=['GET', 'POST'])
@login_required
@superadmin_required()
def user_edit():
    if request.method == 'POST':
        id = request.form.get("id")
        full_name = request.form.get("full_name")
        is_superadmin = 1 if request.form.get("is_superadmin") else 0
        is_blocked = 1 if request.form.get("is_blocked") else 0
        portfolios = request.form.getlist("portfolios")

        # update user profile information
        sql = """
            UPDATE auth_user
            SET full_name = :full_name,
                is_superadmin = :is_superadmin,
                is_blocked = :is_blocked
            WHERE id = :id        
        """
        
        params = {
            'full_name': full_name,
            'is_superadmin': is_superadmin,
            'is_blocked': is_blocked,
            'id': id
        }
        
        db.session.execute(text(sql), params)
        db.session.commit()
        
        # delete user existing portfolios (fist delete then insert)
        sql = """
            DELETE FROM auth_user_portfolio WHERE user_id = :user_id
        """
        
        db.session.execute(text(sql), {'user_id': id})
        db.session.commit()
        
        # insert new portfolios for this users
        if len(portfolios) > 0:
            sql = """
                INSERT INTO auth_user_portfolio (user_id, portfolio_id) VALUES
            """
            #     SELECT
            #         user_id,
            #         portfolio_id
            #     FROM auth_user_portfolio
            #     WHERE user_id = :user_id AND portfolio_id NOT IN :portfolios
            # """
            
            values = ', '.join([f'({id}, {p})' for p in portfolios])
            sql = sql + values
            
            db.session.execute(text(sql))
            db.session.commit()
        
        return redirect(url_for('auth.user_manage'))
        
    
    userid = request.args.get('userid')
    
    sql = '''
        SELECT
            JSON_OBJECT(
                'id', u.id,
                'email', u.email,
                'full_name', u.full_name,
                'is_superadmin', u.is_superadmin,
                'is_blocked', u.is_blocked,
                'portfolios', (
                    SELECT JSON_ARRAYAGG(portfolio_id)
                    FROM auth_user_portfolio up
                    WHERE up.user_id = u.id
                )
            ) AS user
        FROM auth_user u
        WHERE u.id = :id
    '''
    result = db.session.execute(text(sql), {'id': userid}).fetchone()
    user_data = json.loads(result[0])
    
    if user_data.get('portfolios') is None:
        user_data.update({
            'portfolios': []
        })
    
    # user_data = User.query.filter_by(id=userid).one()
    
    # user_schema = AuthUserSchema()
    # data = user_schema.dumps(user)
    
    sql = '''
        SELECT
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'group_id', pg.id,
                    'group_name', pg.group_name,
                    'portfolios', (
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'portfolio_id', p.id,
                                'portfolio', p.portfolio
                            )
                            
                        )
                        FROM hr_employee_portfolio p
                        WHERE p.group_id = pg.id
                    )
                )
            ) AS portfolios
        FROM hr_employee_portfolio_group pg
    '''
    
    result = db.session.execute(text(sql)).fetchone()
    
    portfolio_data = json.loads(result[0])
    
    data = {
        'user': user_data,
        'portfolios': portfolio_data
    }
    
    return render_template('auth/user_edit.html', data=data)


@bp.route('/user-add', methods=['GET', 'POST'])
@login_required
@superadmin_required()
def user_add():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        is_superadmin = 1 if request.form.get('is_superadmin') else 0
        is_blocked = 1 if request.form.get('is_blocked') else 0
        password = request.form.get('password')
        portfolios = request.form.getlist('portfolios')
        
        print('------------------ form data -------------------------')
        print(email)
        print(full_name)
        print(is_superadmin)
        print(is_blocked)
        print(password)
        print(portfolios)

        user = User.query.filter_by(email=email).first()

        if not user:
            sql = '''
                INSERT INTO auth_user
                (
                    email,
                    password,
                    full_name,
                    is_superadmin,
                    is_blocked,
                    created_at
                )
                VALUES
                (
                    :email,
                    :password,
                    :full_name,
                    :is_superadmin,
                    :is_blocked,
                    now()
                )
            '''

            params = {
                'email': email,
                'password': generate_password_hash(password),
                'full_name': full_name,
                'is_superadmin': is_superadmin,
                'is_blocked': is_blocked
            }

            result = db.session.execute(text(sql), params)
            db.session.commit()
            
            # get the id for the last inserted auth_user
            user_id = result.lastrowid
            
            # insert into portfolios
            if len(portfolios) > 0:
                sql = """
                    INSERT INTO auth_user_portfolio (user_id, portfolio_id) VALUES
                """
                #     SELECT
                #         user_id,
                #         portfolio_id
                #     FROM auth_user_portfolio
                #     WHERE user_id = :user_id AND portfolio_id NOT IN :portfolios
                # """
                
                values = ', '.join([f'({user_id}, {p})' for p in portfolios])
                sql = sql + values
                
                db.session.execute(text(sql))
                db.session.commit()
            return redirect(url_for('auth.user_manage'))

        else:
            error = 'This email addres already existed'
    
    
    sql = '''
        SELECT
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'group_id', pg.id,
                    'group_name', pg.group_name,
                    'portfolios', (
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'portfolio_id', p.id,
                                'portfolio', p.portfolio
                            )
                            
                        )
                        FROM hr_employee_portfolio p
                        WHERE p.group_id = pg.id
                    )
                )
            ) AS portfolios
        FROM hr_employee_portfolio_group pg
    '''
    
    result = db.session.execute(text(sql)).fetchone()
    
    portfolio_data = json.loads(result[0])
    
    data = {
        'portfolios': portfolio_data
    }
    
    return render_template('auth/user_add.html', data=data, error=error)


@bp.route('/change-user-password', methods=('GET', 'POST'))
def change_user_password():
    error = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if password == password_confirm:
            user = User.query.filter_by(id=user_id).first()
            user.set_password(password)
            db.session.commit()
            
            return redirect(url_for('auth.user_manage'))
        else:  
            error = 'Password and confirm password are not the same'

    user_id = request.args.get("userid")
    
    sql = """
        SELECT
            id,
            email,
            full_name
        FROM auth_user
        WHERE id = :user_id
    """
    
    data = db.session.execute(text(sql), {'user_id': user_id}).mappings().one()
    
    return render_template('auth/user_change_password.html', data=data, error=error)