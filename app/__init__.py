import logging
from flask import Flask
from instance.config import Config
from app.extensions import db, login_manager, migrate, ma
import os


def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    if test_config:
        app.config.from_mapping(test_config)
    
    # Initialize Flask extensions here
    
    # Initialize SQLAlchemy
    db.init_app(app)
    # Initialize Flask Migrate
    migrate.init_app(app, db)
    
    # Initialize Flask Login
    login_manager.init_app(app)
    
    # Initialize Flask-Marshmallow
    ma.init_app(app)
    
    # Register blueprints here
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.blueprints.hr import bp as hr_bp
    app.register_blueprint(hr_bp)

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    from app.blueprints.utils import bp as utils_bp
    app.register_blueprint(utils_bp)
    
    
    with app.app_context():
        from app.models.auth.models import User
        from app.models.hr.models import Employee, EmployeeDocument, LeaveReason
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    return app
