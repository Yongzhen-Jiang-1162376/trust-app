from flask import request, jsonify, current_app
from sqlalchemy import text
from app.blueprints.api import bp
from app.extensions import db
import os
import uuid
from pathlib import Path


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
        'extension': extension,
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
    print('entering api')
    
    data = request.get_json()
    
    employee_id = data['employee_id']
    
    print(data)
    print(employee_id)
    
    sql = '''
        SELECT
            id,
            employee_id,
            original_file_name,
            extension,
            file_uuid,
            created_at
        FROM hr_employee_document
        WHERE employee_id = :employee_id
        ORDER BY original_file_name
    '''
    
    result = db.session.execute(text(sql), {'employee_id': employee_id}).fetchall()
    
    print(result)
    
    return jsonify(result)

