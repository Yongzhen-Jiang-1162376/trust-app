from flask import render_template, request, jsonify
from app.blueprints.hr import bp
from app.models.hr import Employee, LeaveReason
from app.schemas.hr import EmployeeSchema
from sqlalchemy import select, text
from app.extensions import db
from marshmallow import EXCLUDE
from marshmallow.exceptions import ValidationError
from pprint import pprint


@bp.route('/employees', methods=('GET',))
def employee_list():
    
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
        {
            'id': 'leave_reason_id',
            'name': 'Leave Reason Id'
        },
        {
            'id': 'leave_reason',
            'name': 'Leave Reason'
        },
        {
            'id': 'comments',
            'name': 'Comments'
        }
    ]

    sql = '''
        SELECT
            e.id,
            e.full_name,
            e.gender,
            e.position,
            e.portfolio_assigned,
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
            e.leave_reason_id,
            l.reason as leave_reason,
            e.comments
        FROM hr_employee e
        LEFT JOIN hr_leave_reason l ON e.leave_reason_id = l.id
        -- WHERE e.id = 57
        ORDER BY e.id
    '''
    
    result = db.session.execute(text(sql)).fetchall()

    employee_schema = EmployeeSchema(many=True)

    # serialize to json string
    json_str = employee_schema.dumps(result)
    
    # print(json_str)
    
    return render_template('hr/employee_list.html', columns=columns, data=json_str)


@bp.route('/employees/create', methods=('GET', 'POST'))
def employee_create():
    error = None
    
    print('entering....')
    print(request.method)
    
    allow_none_fields = [
        'date_of_birth', 
        'start_date', 
        'resignation_date', 
        'last_working_date', 
        'trial_period_start_date',
        'hours_per_week',
        'trial_period'
    ]
    
    if (request.method == 'POST'):
        emp_schema = EmployeeSchema(unknown=EXCLUDE)
        
        formData = request.form.to_dict()
        
        
        
        for key in formData.keys():
            if key in allow_none_fields and formData[key] == '':
                formData[key] = None
                
        files = request.files
        
        pprint(formData)
        pprint(files)
        
        try:
            emp_data = emp_schema.load(formData)
        
        except ValidationError as err:
            error = err.messages
    
    return render_template('hr/employee_create.html', error=error)
