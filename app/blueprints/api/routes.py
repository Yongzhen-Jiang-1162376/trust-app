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
    
    user_id = request.form['user_id']
    extension = Path(file.filename).suffix
    original_file_name = file.filename
    file_uuid = str(uuid.uuid4())
    
    new_file_name = file_uuid + extension
    
    params = {
        'user_id': user_id,
        'extension': extension,
        'original_file_name': original_file_name,
        'file_uuid': file_uuid
    }
    
    print(user_id, extension, original_file_name, file_uuid, new_file_name)
    
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
            :user_id,
            :original_file_name,
            :extension,
            :file_uuid,
            now()
        )
    '''
    
    save_path = os.path.join(current_app.config['UPLOAD_PATH'], new_file_name)
    print(save_path)
    file.save(save_path)
    
    db.session.execute(text(sql), params)
    db.session.commit()

    return jsonify({'message': f'File {file.filename} uploaded successfully'})

@bp.route('/get-employee-documents', methods=('POST',))
def get_employee_documents():
    pass
