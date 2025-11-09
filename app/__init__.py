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

    # Register blueprints here if needed:
    # from .routes import bp as main_bp
    # app.register_blueprint(main_bp)

    return app
