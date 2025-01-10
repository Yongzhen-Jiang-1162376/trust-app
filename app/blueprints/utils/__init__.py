from flask import Blueprint
bp = Blueprint('utils', __name__, url_prefix='/utils')
from . import routes
