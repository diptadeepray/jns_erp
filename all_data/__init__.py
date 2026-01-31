# This file can be empty or contain package-level imports
# e.g., importing routes to ensure they are registered

from flask import Blueprint

all_data_bp = Blueprint('all_data', __name__, template_folder='../templates')

from . import routes
