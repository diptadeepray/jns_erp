# This file can be empty or contain package-level imports
# e.g., importing routes to ensure they are registered

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

from . import routes
