from flask import Blueprint

# Create the main 'buddyprogram' blueprint
bp = Blueprint('buddyprogram', __name__, url_prefix='/buddyprogram')

# Import the sub-blueprints
from .match import bp as match_bp


# Register the sub-blueprints with the main blueprint
bp.register_blueprint(match_bp)



