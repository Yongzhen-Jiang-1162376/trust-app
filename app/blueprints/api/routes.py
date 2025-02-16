from flask import request, jsonify, current_app, send_file
from flask_login import current_user
from sqlalchemy import text
from app.blueprints.api import bp
from app.extensions import db
import os
import uuid
from pathlib import Path
import pyexcel as pe


def remove_document(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_employee(employee_id):
    remove_employee_documents(employee_id)
    remove_employee_document_records(employee_id)
    remove_employee_profile(employee_id)


def remove_employee_documents(employee_id):
    sql = '''
        SELECT file_name FROM hr_employee_document WHERE employee_id = :employee_id
    '''

    result = db.session.execute(text(sql), {'employee_id': employee_id}).fetchall()

    for file_name in result:
        file_path = os.path.join(current_app.config['DOCUMENT_ROOT_PATH'], file_name[0])
        remove_document(file_path)   # result is list of tuple


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
        SELECT file_name FROM hr_employee_document WHERE id = :document_id
    '''

    result = db.session.execute(text(select_sql), {'document_id': document_id})

    row = result.fetchone()
    if row:
        remove_path = os.path.join(current_app.config['DOCUMENT_ROOT_PATH'], row[0])
        if os.path.exists(remove_path):
            os.remove(remove_path)

    remove_sql = '''
        DELETE FROM hr_employee_document WHERE id = :document_id
    '''
    
    db.session.execute(text(remove_sql), {'document_id': document_id})
    db.session.commit()


def import_employee_data(data):
    insert_sql = '''
        INSERT INTO hr_employee
        (
            start_date,
            full_name,
            gender,
            trial_period_start_date,
            employee_type,
            position,
            mode_of_work,
            volunteer_current_status,
            hours_per_week,
            portfolio_assigned,
            manager_name,
            address,
            date_of_birth,
            nationality,
            contact_detail,
            email,
            comments,
            trial_period,
            resignation_date,
            last_working_date,
            feedback_performance_review,
            leave_reason
        )
        VALUES
    '''

    values = []
    for row in data:
        r1 = f"'{row[1]}'"
        r4 = f"'{row[4]}'"
        r13 = f"'{row[13]}'"
        r20 = f"'{row[20]}'"
        r21 = f"'{row[21]}'"

        row1 = f"{'Null' if row[1] == '' else r1}"
        row4 = f"{'Null' if row[4] == '' else r4}"
        row13 = f"{'Null' if row[13] == '' else r13}"
        row20 = f"{'Null' if row[20] == '' else r20}"
        row21 = f"{'Null' if row[21] == '' else r21}"

        value = f"({row1}, '{row[2]}', '{row[3]}', {row4}, '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}', '{row[11]}', '{row[12]}', {row13}, '{row[14]}', '{row[15]}', '{row[16]}', '{row[18]}', '{row[19]}', {row20}, {row21}, '{row[22]}', '{row[23]}')"

        # value = (
        #     f"({'Null' if row[1] == '' else {f"'{row[1]}'"}}, '{row[2]}', '{row[3]}', {'Null' if row[4] == '' else {f"'{row[4]}'"}}, '{row[5]}',"
        #     f"'{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}', "
        #     f"'{row[11]}', '{row[12]}', {'Null' if row[13] == '' else {f"'{row[13]}'"}}, '{row[14]}', '{row[15]}', "
        #     f"'{row[16]}', '{row[18]}', '{row[19]}', {'Null' if row[20] == '' else {f"'{row[20]}'"}}, {'Null' if row[21] == '' else {f"'{row[21]}'"}}, "
        #     f"'{row[22]}', '{row[23]}')")
        values.append(value)
    
    insert_sql += ', '.join(values)

    db.session.execute(text(insert_sql))
    db.session.commit()


def remove_portfolio(ids):
    sql = """
        DELETE FROM hr_employee_portfolio_assigned
        WHERE portfolio_id in :portfolio_ids;

        DELETE FROM hr_employee_portfolio
        WHERE id in :ids;
    """
    
    params = {
        'ids': ids,
        'portfolio_ids': ids
    }

    db.session.execute(text(sql), params)
    db.session.commit()


def remove_portfolio_group(ids):
    sql = """
        DELETE FROM hr_employee_portfolio_group WHERE id in :ids;
    """

    db.session.execute(text(sql), {'ids': ids})
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
    
    # new_file_name = file_uuid + extension
    
    params = {
        'employee_id': employee_id,
        'extension': extension[1:] if len(extension) > 1 else extension,
        'original_file_name': original_file_name,
        'file_uuid': file_uuid
    }
    
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
    
    db.session.execute(text(sql), params)
    db.session.commit()
    
    sql = '''
        SELECT LAST_INSERT_ID()
    '''
    
    last_inserted_id = db.session.execute(text(sql)).scalar()
    
    # file name: original file name + first 8 digits of uuid + file id + extension
    new_file_name = Path(file.filename).stem + '_' + file_uuid[0:8] + '_' + str(last_inserted_id) + extension
    
    save_path = os.path.join(current_app.config['DOCUMENT_ROOT_PATH'], new_file_name)
    file.save(save_path)

    sql = '''
        UPDATE hr_employee_document
        SET file_name = :file_name
        WHERE id = :id
    '''
    
    params = {
        'file_name': new_file_name,
        'id': last_inserted_id
    }
    
    db.session.execute(text(sql), params)
    db.session.commit()

    return jsonify({'message': f'File {file.filename} uploaded successfully'})


@bp.route('/get-employee-documents', methods=('POST',))
def get_employee_documents():
    data = request.get_json()    
    employee_id = data['employee_id']

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
    
    # delete employee in backend
    [remove_employee(id) for id in ids]

    return jsonify({'status': 'success', 'message': 'Employee data deleted successfully'}), 200   


@bp.route('/download-employee-document', methods=('POST',))
def download_employee_document():
    data = request.get_json()    
    document_id = data['document_id']

    select_sql = '''
        SELECT file_name FROM hr_employee_document WHERE id = :document_id
    '''

    result = db.session.execute(text(select_sql), {'document_id': document_id})

    row = result.fetchone()
    if row:
        file_path = os.path.join(current_app.config['DOCUMENT_ROOT_PATH'], row[0])
        if os.path.exists(file_path):
            
            return send_file(file_path, as_attachment=True)

    return jsonify({'status': 'error', 'message': 'Document not existing.'}), 400


@bp.route('/update-employee', methods=('POST',))
def update_employee():
    
    data = request.get_json()
    # employee_id = data['employee_id']
    
    portfolios = data['portfolio_assigned']
    employee_id = data['employee_id']
    
    data.pop('portfolio_assigned')

    sql = '''
        UPDATE hr_employee
        SET full_name = :full_name,
            gender = :gender,
            position = :position,
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
            leave_reason = :leave_reason,
            comments = :comments,
            updated_at = now()
        WHERE id = :employee_id
    '''
    
    db.session.execute(text(sql), data)
    db.session.commit()
    
    
    # update portfolio assigned
    sql = '''
        delete from hr_employee_portfolio_assigned
        where employee_id = :employee_id
    '''
    db.session.execute(text(sql), {'employee_id': employee_id})
    db.session.commit()
    
    sql = 'insert into hr_employee_portfolio_assigned (employee_id, portfolio_id) values '
    s = ', '.join([f'({employee_id}, {p})' for p in portfolios])
    
    sql += s
    
    db.session.execute(text(sql))
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Profile data updated successfully'}), 200


@bp.route('/create-employee', methods=('POST',))
def create_employee():
    data = request.get_json()
    
    full_name = data.get('full_name')
    if full_name is None or full_name == '':
        return jsonify({'status': 'error', 'message': 'Name is empty'}), 400

    portfolios = data.get('portfolio_assigned')
    data.pop('portfolio_assigned')


    sql = '''
        INSERT INTO hr_employee
        (
            full_name, 
            gender,
            position,
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
        )
        VALUES
        (
            :full_name, 
            :gender,
            :position,
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
    
    db.session.execute(text(sql), data)
    db.session.commit()
    
    sql = '''
        SELECT LAST_INSERT_ID()
    '''
    
    last_inserted_id = db.session.execute(text(sql)).scalar()
    # print('-------- last inserted id ----------')
    # print(last_inserted_id)
    
    sql = 'insert into hr_employee_portfolio_assigned (employee_id, portfolio_id) values '
    s = ', '.join([f'({last_inserted_id}, {p})' for p in portfolios])
    
    sql += s
    
    # print('insertion sql')
    # print(sql)
    
    db.session.execute(text(sql))
    db.session.commit()
    
    
    
    
    return jsonify({'status': 'success', 'message': 'Profile data added successfully', 'employee_id': last_inserted_id}), 200


# @bp.route('/export-employee-data', methods=('GET',))
# def export_employee_data():
#     pass


@bp.route('/import-employee', methods=('POST',))
def import_employee():

    file = request.files['file']
    filename = file.filename

    save_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
    file.save(save_path)

    try:
        emp_records = pe.get_array(file_name=save_path, start_row=1)

        import_employee_data(emp_records)

    except Exception as e:
        return jsonify({'message': repr(e)}), 400

    return jsonify({'message': 'imported successfully'}), 200


@bp.route('/change-user-name', methods=('POST',))
def change_user_name():
    data = request.get_json()

    sql = """
        UPDATE auth_user
        SET full_name = :full_name
        WHERE id = :id
    """

    db.session.execute(text(sql), data)
    db.session.commit()

    return jsonify({'message': 'User name changed successfully'}), 200


@bp.route('/change-user-password', methods=('POST',))
def change_user_password():
    data = request.get_json()

    password = data.get('password')
    password_confirm = data.get('password_confirm')

    if password != password_confirm:
        return jsonify({'status': 'error', 'message': 'Confirm password is not the same'}), 400

    current_user.set_password(password)
    db.session.commit()

    return jsonify({'message': 'Password changed successfully'}), 200


@bp.route('/update-portfolio', methods=('POST',))
def update_portfolio():
    data = request.get_json()

    sql = """
        UPDATE hr_employee_portfolio
        SET portfolio = :portfolio
        WHERE id = :id
    """

    db.session.execute(text(sql), data)
    db.session.commit()

    return jsonify({'message': 'Portfolio changed successfully'}), 200


@bp.route('/remove-portfolio-list', methods=('POST',))
def remove_portfolio_list():
    data = request.get_json()
    ids = data['ids']

    # print(ids)

    remove_portfolio(ids)

    return jsonify({'message': 'Portfolio deleted successfully'}), 200


@bp.route('/update-portfolio-group', methods=('POST',))
def update_portfolio_group():
    data = request.get_json()

    sql = """
        UPDATE hr_employee_portfolio_group
        SET group_name = :group_name
        WHERE id = :group_id
    """

    db.session.execute(text(sql), data)
    db.session.commit()

    return jsonify({'message': 'Portfolio group changed successfully'}), 200


@bp.route('/remove-portfolio-group-list', methods=('POST',))
def remove_portfolio_group_list():
    data = request.get_json()
    ids = data['ids']


    sql = """
        SELECT * FROM hr_employee_portfolio WHERE group_id IN :ids
    """

    result = db.session.execute(text(sql), {'ids': ids}).fetchall()

    if len(result) > 0:
        return jsonify({'status': 'error', 'message': 'Portfolio exists in this group.'}), 400


    remove_portfolio_group(ids)

    # [remove_portfolio_group(id) for id in ids]

    return jsonify({'message': 'Portfolio deleted successfully'}), 200
