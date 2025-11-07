from app import create_app
from app.extensions import db
from app.models import Trial, Match, Patient
from app.services.trial_service import populate_trial_database

app = create_app()
with app.app_context():
    populate_trial_database()
