from flask import Blueprint, jsonify
from app.extensions import db

bp = Blueprint('health', __name__)

@bp.route('/api/health', methods=['GET'])
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status':'healthy','database':'connected','service':'bc-pf-backend'}),200
    except Exception as e:
        return jsonify({'status':'unhealthy','database':'disconnected','error':str(e)}),500
