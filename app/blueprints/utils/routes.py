from flask import request, current_app, send_file
from faker import Faker
from app.extensions import db
from app.blueprints.utils import bp
from sqlalchemy import text
import random
import os


def generate_fake_emp():
    fake = Faker()
    
    emp = {
        'full_name': fake.name(),
        'gender': random.choice(['Male', 'Female']),
        'position': random.choice(['Engineer', 'Manager', 'Supervisor', 'Administrator', 'Director']),
        'portfolio_assigned': fake.job(),
        'manager_name': fake.name(),
        'employee_type': random.choice(['Employee', 'Volunteer']),
        'mode_of_work': random.choice(['Onsite', 'Remote', 'Hybrid']),
        'date_of_birth': fake.date(),
        'nationality': fake.country(),
        'email': fake.email(),
        'contact_detail': fake.phone_number(),
        'address': fake.address().replace('\n', ' '),
        'start_date': fake.date(),
        'resignation_date': fake.date(),
        'last_working_date': fake.date(),
        'trial_period': random.randint(1, 6),
        'trial_period_start_date': fake.date(),
        'hours_per_week': random.uniform(4, 40),
        'volunteer_current_status': random.choice(['working', 'not working', 'postponed', 'stopped']),
        'feedback_performance_review':fake.text(max_nb_chars=160),
        'leave_reason': fake.sentence(nb_words=6),
        'comments': ' '.join(fake.words(5))
    }
    
    return emp
    

@bp.route('/create-fake-employees', methods=('GET',))
def create_fake_employees():
    
    employees = []
    
    for i in range(50):
        employees.append(generate_fake_emp())
    
    sql = '''
        INSERT INTO hr_employee 
        (
            full_name, 
            gender,
            position,
            portfolio_assigned,
            manager_name,
            employee_type,
            mode_of_work,
            date_of_birth,
            nationality,
            email,
            contact_detail,
            address,
            start_date,
            resignation_date,
            last_working_date,
            trial_period,
            trial_period_start_date,
            hours_per_week,
            volunteer_current_status,
            feedback_performance_review,
            leave_reason,
            comments
        ) VALUES (
            :full_name,
            :gender,
            :position,
            :portfolio_assigned,
            :manager_name,
            :employee_type,
            :mode_of_work,
            :date_of_birth,
            :nationality,
            :email,
            :contact_detail,
            :address,
            :start_date,
            :resignation_date,
            :last_working_date,
            :trial_period,
            :trial_period_start_date,
            :hours_per_week,
            :volunteer_current_status,
            :feedback_performance_review,
            :leave_reason,
            :comments
        )
    '''

    db.session.execute(text(sql), employees)
    db.session.commit()

    return '<h2>data inserted successfully</h2>'


@bp.route('/download/<path:name>')
def download_file(name):
    filepath = os.path.join(current_app.config['DOWNLOAD_PATH'], name)
    return send_file(filepath, as_attachment=True)
