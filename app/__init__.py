from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig  # Use DevelopmentConfig for local testing
from .extensions import db  # Import the shared SQLAlchemy instance

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS - Allow requests from your frontend
    CORS(app, origins=['http://localhost:3004', 'http://localhost:3000'])

    # Initialize extensions
    db.init_app(app)

    # Example route for health checking
    @app.route('/api/health')
    def health():
        return {"status": "healthy"}

    # Register blueprints
    from app.routes.patient_routes import bp as patient_bp
    from app.routes.trial_routes import bp as trial_bp
    from app.routes.healthcheck import bp as health_bp

    app.register_blueprint(patient_bp)
    app.register_blueprint(trial_bp)
    app.register_blueprint(health_bp)

    return app
