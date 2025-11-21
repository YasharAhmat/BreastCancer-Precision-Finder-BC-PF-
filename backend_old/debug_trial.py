from app import create_app
from app.models.trial import Trial

app = create_app()
with app.app_context():
    trial = Trial.query.first()
    print(f"NCT ID: {trial.nct_id}")
    print(f"trial.min_age (column): {trial.min_age}")
    print(f"trial.max_age (column): {trial.max_age}")
    print(f"trial.gender (column): {trial.gender}")
    print(f"trial.target_subtype (column): {trial.target_subtype}")
    print(f"trial.to_dict(): {trial.to_dict()}")
