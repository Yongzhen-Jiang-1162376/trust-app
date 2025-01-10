from flask import request, jsonify, current_app, send_file
from sqlalchemy import text
from app.blueprints.api import bp
from app.extensions import db
import os
import uuid
from pathlib import Path


def remove_document(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_employee(employee_id):
    remove_employee_document(employee_id)
    remove_employee_document_records(employee_id)
    remove_employee_profile(employee_id)


def remove_employee_documents(employee_id):
    sql = '''
        SELECT concat(file_uuid, '.', extension) AS file_name FROM hr_employee_document WHERE employee_id = :employee_id
    '''

    result = db.session.execute(text(sql), {'employee_id': employee_id}).fetchall()

    print(result)

    for file_path in result:
        remove_document(file_path)


def remove_employee_document_records(employee_id):
    sql = '''
        DELETE FROM hr_employee_document WHERE employee_id = :employee_id
    '''

    db.session.execute(text(sql), {'employee_id': employee_id})
    db.session.commit()


def remove_employee_profile(employee_id):
    sql = '''
        DELETE FROM hr_employee WHERE id = :employee_id
    '''

    db.session.execute(text(sql), {'employee_id': employee_id})
    db.session.commit()


def remove_employee_document_by_document_id(document_id):
    select_sql = '''
        SELECT concat(file_uuid, '.', extension) AS file_name FROM hr_employee_document WHERE id = :document_id
    '''

    result = db.session.execute(text(select_sql), {'document_id': document_id})
    # print(result)

    row = result.fetchone()
    if row:
        remove_path = os.path.join(current_app.config['UPLOAD_PATH'], row[0])
        if os.path.exists(remove_path):
            os.remove(remove_path)

    remove_sql = '''
        DELETE FROM hr_employee_document WHERE id = :document_id
    '''
    
    db.session.execute(text(remove_sql), {'document_id': document_id})
    db.session.commit()


@bp.route('/upload-employee-document', methods=('POST',))
def upload_employee_document():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    employee_id = request.form['employee_id']
    extension = Path(file.filename).suffix
    original_file_name = file.filename
    file_uuid = str(uuid.uuid4())
    
    new_file_name = file_uuid + extension
    
    params = {
        'employee_id': employee_id,
        'extension': extension[1:] if len(extension) > 1 else extension,
        'original_file_name': original_file_name,
        'file_uuid': file_uuid
    }
    
    # print(employee_id, extension, original_file_name, file_uuid, new_file_name)
    
    sql = '''
        INSERT INTO hr_employee_document
        (
            employee_id,
            original_file_name,
            extension,
            file_uuid,
            created_at
        )
        VALUES
        (
            :employee_id,
            :original_file_name,
            :extension,
            :file_uuid,
            now()
        )
    '''
    
    save_path = os.path.join(current_app.config['UPLOAD_PATH'], new_file_name)
    file.save(save_path)
    
    db.session.execute(text(sql), params)
    db.session.commit()

    return jsonify({'message': f'File {file.filename} uploaded successfully'})

@bp.route('/get-employee-documents', methods=('POST',))
def get_employee_documents():
    data = request.get_json()    
    employee_id = data['employee_id']

    # print(data)
    # print(employee_id)
    
    sql = '''
        SELECT
            id,
            employee_id,
            original_file_name,
            extension,
            file_uuid,
            date_format(created_at, '%Y-%m-%d %H:%i:%s') AS created_at
        FROM hr_employee_document
        WHERE employee_id = :employee_id
        ORDER BY original_file_name
    '''
    
    result = db.session.execute(text(sql), {'employee_id': employee_id})
    
    result_mappings = result.mappings()

    rows = [dict(row) for row in result_mappings]

    # print(rows)

    return rows

@bp.route('/remove-employee-document', methods=('POST',))
def remove_employee_document():
    data = request.get_json()    
    document_id = data['document_id']

    remove_employee_document_by_document_id(document_id)
    
    return jsonify({'status': 'success', 'message': 'Document removed successfully'}), 200


@bp.route('/remove-employee-list', methods=('POST',))
def remove_employee_list():
    data = request.get_json()
    ids = data['employee_ids']
    
    # [remove_employee(id) for id in ids]

    return jsonify({'status': 'success', 'message': 'Employee data deleted successfully'}), 200   


@bp.route('/download-employee-document', methods=('POST',))
def download_employee_document():
    data = request.get_json()    
    document_id = data['document_id']

    select_sql = '''
        SELECT concat(file_uuid, '.', extension) AS file_name FROM hr_employee_document WHERE id = :document_id
    '''

    result = db.session.execute(text(select_sql), {'document_id': document_id})
    print(result)

    row = result.fetchone()
    if row:
        file_path = os.path.join(current_app.config['UPLOAD_PATH'], row[0])
        if os.path.exists(file_path):
            
            return send_file(file_path, as_attachment=True)

    return jsonify({'status': 'error', 'message': 'Document not existing.'}), 400


@bp.route('/update-employee', methods=('POST',))
def update_employee():
    print('entering in api function')
    
    data = request.get_json()    
    # employee_id = data['employee_id']

    sql = '''
        UPDATE hr_employee
        SET full_name = :full_name,
            gender = :gender,
            position = :position,
            portfolio_assigned = :portfolio_assigned,
            manager_name = :manager_name,
            employee_type = :employee_type,
            mode_of_work = :mode_of_work,
            date_of_birth = :date_of_birth,
            nationality = :nationality,
            email = :email,
            contact_detail = :contact_detail,
            address = :address,
            start_date = :start_date,
            resignation_date = :resignation_date,
            last_working_date = :last_working_date,
            trial_period = :trial_period,
            trial_period_start_date = :trial_period_start_date,
            hours_per_week = :hours_per_week,
            volunteer_current_status = :volunteer_current_status,
            feedback_performance_review = :feedback_performance_review,
            leave_reason_id = :leave_reason_id,
            comments = :comments,
            updated_at = now()
        WHERE id = :employee_id
    '''
    
    db.session.execute(text(sql), data)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Profile data updated successfully'}), 200


@bp.route('/export-employee-data', methods=('GET',))
def export_employee_data():
    pass
