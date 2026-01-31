# This file can be empty or contain package-level imports
# e.g., importing routes to ensure they are registered

from flask import Blueprint

delete_data_bp = Blueprint('delete_data', __name__, template_folder='../templates')

from . import routes
