import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    UPLOAD_PATH = os.path.join(os.path.dirname(basedir), 'uploads')
    DOCUMENT_ROOT_PATH = os.path.join(os.path.dirname(basedir), 'documents_root')
    DOWNLOAD_PATH = os.path.join(os.path.dirname(basedir), 'downloads')
