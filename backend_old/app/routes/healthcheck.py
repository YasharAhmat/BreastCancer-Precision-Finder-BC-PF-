from flask import Blueprint, jsonify
from app.extensions import db

bp = Blueprint('health', __name__, url_prefix='/api')


@bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        db.session.execute(text("SELECT 1"))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'

    return jsonify({
        'status': 'healthy',
        'database': db_status
    }), 200
