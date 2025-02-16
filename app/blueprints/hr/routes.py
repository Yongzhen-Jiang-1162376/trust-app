from flask import render_template, request, jsonify, current_app, redirect, url_for
from app.blueprints.hr import bp
from app.models.hr import Employee
from app.schemas.hr import EmployeeSchema, PortfolioGroupSchema, PortfolioSchema
from sqlalchemy import select, text
from app.extensions import db
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from pprint import pprint
from flask_login import login_required, current_user
import os
import pyexcel as pe


@bp.route('/employees', methods=('GET',))
@login_required
def employee_list():
    
    id = current_user.id
    
    columns = [
        {
            'id': 'id',
            'name': 'Internal Id'
        },
        {
            'id': 'full_name',
            'name': 'Full Name'
        },
        {
            'id': 'gender',
            'name': 'Gender'
        },
        {
            'id': 'position',
            'name': 'Position'
        },
        {
            'id': 'portfolio_assigned_names',
            'name': 'Portfolio Assigned'
        },
        {
            'id': 'portfolio_assigned',
            'name': 'Portfolio Assigned'
        },
        {
            'id': 'manager_name',
            'name': 'Manager Name'
        },
        {
            'id': 'employee_type',
            'name': 'Employee Type'
        },
        {
            'id': 'mode_of_work',
            'name': 'Mode of Work'
        },
        {
            'id': 'date_of_birth',
            'name': 'Date of Birth'
        },
        {
            'id': 'nationality',
            'name': 'Nationality'
        },
        {
            'id': 'email',
            'name': 'Email'
        },
        {
            'id': 'contact_detail',
            'name': 'Contact Detail'
        },
        {
            'id': 'address',
            'name': 'Address'
        },
        {
            'id': 'start_date',
            'name': 'Start Date'
        },
        {
            'id': 'resignation_date',
            'name': 'Resignation Date'
        },
        {
            'id': 'last_working_date',
            'name': 'Last Working Day'
        },
        {
            'id': 'trial_period',
            'name': 'Trial Period'
        },
        {
            'id': 'trial_period_start_date',
            'name': 'Trial Period Start Date'
        },
        {
            'id': 'hours_per_week',
            'name': 'Hours Per Week'
        },
        {
            'id': 'volunteer_current_status',
            'name': 'Volunteer Current Status'
        },
        {
            'id': 'feedback_performance_review',
            'name': 'Feedback & Performance Review'
        },
        # {
        #     'id': 'leave_reason_id',
        #     'name': 'Leave Reason Id'
        # },
        {
            'id': 'leave_reason',
            'name': 'Leave Reason'
        },
        {
            'id': 'comments',
            'name': 'Comments'
        }
    ]
    
    
    sql = None
    result = None
    
    if current_user.is_superadmin:
        sql = '''
            SELECT
                e.id,
                e.full_name,
                e.gender,
                e.position,
                GROUP_CONCAT(ep.portfolio ORDER BY ep.id SEPARATOR ', ') AS portfolio_assigned_names,
                GROUP_CONCAT(ep.id ORDER BY ep.id SEPARATOR ', ') AS portfolio_assigned,
                e.manager_name,
                e.employee_type,
                e.mode_of_work,
                e.date_of_birth,
                e.nationality,
                e.email,
                e.contact_detail,
                e.address,
                e.start_date,
                e.resignation_date,
                e.last_working_date,
                e.trial_period,
                e.trial_period_start_date,
                e.hours_per_week,
                e.volunteer_current_status,
                REPLACE(e.feedback_performance_review, '\\n', '\\\\n') AS feedback_performance_review,
                e.leave_reason,
                e.comments
            FROM hr_employee e
            LEFT JOIN hr_employee_portfolio_assigned epa ON e.id = epa.employee_id
            LEFT JOIN hr_employee_portfolio ep ON epa.portfolio_id = ep.id
            GROUP BY e.id
            ORDER BY e.id
        '''
        result = db.session.execute(text(sql)).fetchall()
    else:
        sql = """
            SELECT
                e.id,
                e.full_name,
                e.gender,
                e.position,
                GROUP_CONCAT(ep.portfolio ORDER BY ep.id SEPARATOR ', ') AS portfolio_assigned_names,
                GROUP_CONCAT(ep.id ORDER BY ep.id SEPARATOR ', ') AS portfolio_assigned,
                e.manager_name,
                e.employee_type,
                e.mode_of_work,
                e.date_of_birth,
                e.nationality,
                e.email,
                e.contact_detail,
                e.address,
                e.start_date,
                e.resignation_date,
                e.last_working_date,
                e.trial_period,
                e.trial_period_start_date,
                e.hours_per_week,
                e.volunteer_current_status,
                REPLACE(e.feedback_performance_review, '\\n', '\\\\n') AS feedback_performance_review,
                e.leave_reason,
                e.comments
            FROM hr_employee e
            LEFT JOIN hr_employee_portfolio_assigned epa ON e.id = epa.employee_id
            LEFT JOIN hr_employee_portfolio ep ON epa.portfolio_id = ep.id
            WHERE e.id IN (
                SELECT
                    DISTINCT employee_id
                FROM hr_employee_portfolio_assigned
                WHERE portfolio_id IN (
                    SELECT
                        up.portfolio_id
                    FROM auth_user u
                    INNER JOIN auth_user_portfolio up ON u.id = up.user_id
                    WHERE id = :id	
                )
            )
            GROUP BY e.id
            ORDER BY e.id
            ;
        """
        result = db.session.execute(text(sql), {'id': id}).fetchall()
    
    employee_schema = EmployeeSchema(many=True)

    # serialize to json string
    table_data = employee_schema.dumps(result)
    
    sql = """
        SELECT
            p.id,
            p.portfolio
        FROM hr_employee_portfolio p
        ORDER BY p.id
    """
    portfolio_list = db.session.execute(text(sql)).fetchall()
    
    return render_template('hr/employee_list.html', portfolio_list =portfolio_list, columns=columns, table_data=table_data)


@bp.route('/employees/create')
@login_required
def employee_create():
    
    sql = """
        SELECT
            p.id,
            p.portfolio
        FROM hr_employee_portfolio p
        ORDER BY p.id
    """
    portfolio_list = db.session.execute(text(sql)).fetchall()
    
    return render_template('hr/employee_create.html', portfolio_list=portfolio_list)


@bp.route('/portfolios')
@login_required
def portfolio_list():

    sql = """
        SELECT
            id,
            group_name
        FROM hr_employee_portfolio_group;
    """
    result = db.session.execute(text(sql)).fetchall()

    group_schema = PortfolioGroupSchema(many=True)
    group_list = group_schema.dumps(result)

    sql = """
        SELECT 
            p.id,
            pg.group_name,
            p.portfolio
        FROM hr_employee_portfolio p
        INNER JOIN hr_employee_portfolio_group pg ON p.group_id = pg.id
    """


    result = db.session.execute(text(sql)).fetchall()
    portfolio_schema = PortfolioSchema(many=True)
    portfolio_list = portfolio_schema.dumps(result)

    print(group_list)
    print(portfolio_list)

    return render_template('hr/portfolio_list.html', group_list=group_list, portfolio_list=portfolio_list)


@bp.route('/portfolio/create', methods=('GET', 'POST'))
@login_required
def portfolio_create():
    error = None

    sql = """
        SELECT
            id,
            group_name
        FROM hr_employee_portfolio_group
        ORDER BY id
    """
    result = db.session.execute(text(sql)).fetchall()

    group_schema = PortfolioGroupSchema(many=True)
    group_list = group_schema.dump(result)

    if request.method == 'POST':
        group_id = request.form.get('group_id')
        portfolio = request.form.get('portfolio')

        if not portfolio:
            error = 'portfolio is empty'
            return render_template('hr/portfolio_create.html', group_list=group_list, error=error)
        
        sql = """
            SELECT
                id
            FROM hr_employee_portfolio
            WHERE group_id = :group_id AND portfolio = :portfolio
        """

        params = {
            'group_id': group_id,
            'portfolio': portfolio
        }

        result = db.session.execute(text(sql), params).fetchall()

        if len(result) > 0:
            error = 'Portfolio already existed'
            return render_template('hr/portfolio_create.html', group_list=group_list, error=error)

        sql = """
            INSERT INTO hr_employee_portfolio (group_id, portfolio) VALUES (:group_id, :portfolio);
        """
        db.session.execute(text(sql), params)
        db.session.commit()

        return redirect(url_for('hr.portfolio_list'))
    
    return render_template('hr/portfolio_create.html', group_list=group_list, error=error)



@bp.route('/portfoliogroup/create', methods=('GET', 'POST'))
@login_required
def portfolio_group_create():
    error = None

    if request.method == 'POST':
        group_name = request.form.get('group_name')

        if not group_name:
            error = 'portfolio group is empty'
            return render_template('hr/portfolio_group_create.html', error=error)
        
        sql = """
            SELECT
                id
            FROM hr_employee_portfolio_group
            WHERE group_name = :group_name
        """

        params = {
            'group_name': group_name
        }

        result = db.session.execute(text(sql), params).fetchall()

        if len(result) > 0:
            error = 'Portfolio group already existed'
            return render_template('hr/portfolio_group_create.html', error=error)

        sql = """
            INSERT INTO hr_employee_portfolio_group (group_name) VALUES (:group_name);
        """
        db.session.execute(text(sql), params)
        db.session.commit()

        return redirect(url_for('hr.portfolio_list'))
    
    return render_template('hr/portfolio_group_create.html', error=error)
