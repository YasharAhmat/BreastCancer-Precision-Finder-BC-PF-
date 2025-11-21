from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .extensions import db


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS (fixes 403 errors)
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Register blueprints (fixes 404 errors)
    from app.routes.healthcheck import bp as health_bp
    from app.routes.patient_routes import bp as patient_bp
    from app.routes.trial_routes import bp as trial_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(trial_bp)

    return app
