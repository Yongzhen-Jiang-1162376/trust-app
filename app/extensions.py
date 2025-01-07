from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

from flask_migrate import Migrate
migrate = Migrate()

from flask_login import LoginManager
login_manager = LoginManager()

from flask_marshmallow import Marshmallow
ma = Marshmallow()
