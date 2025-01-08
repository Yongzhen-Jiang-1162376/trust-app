from flask import request, jsonify, current_app
from app.blueprints.api import bp
from app.extensions import db
import os


@bp.route('/upload-employee-documents', methods=('POST',))
def getEmployeeDocumentList():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    save_path = os.path.join(current_app.config['UPLOAD_PATH'], file.filename)
    file.save(save_path)

    return jsonify({'message': f'File {file.filename} uploaded successfully'})
