
import pandas as pd
from app import create_app
from app.models import Trial
from app.extensions import db
from app.services.trial_service import determine_subtype
from app.services.trial_service import refresh_trial_data# Import the function

app = create_app()

with app.app_context():
    refresh_trial_data()

with app.app_context():
    # Select trials to refresh, e.g., the latest 100 for export
    trials = Trial.query.limit(200).all()
    # Update subtype for each trial using the latest logic
    for trial in trials:
        trial.target_subtype = determine_subtype(f"{trial.title} {trial.description}")
    db.session.commit()
    # Export with refreshed subtypes
    data = [trial.to_dict() for trial in trials]
    df = pd.DataFrame(data)
    df.to_excel('trials_export.xlsx', index=False)

print('Exported trials to trials_export.xlsx')

from app import create_app
from app.models import Trial

app = create_app()
with app.app_context():
    for trial in Trial.query.limit(5).all():
        print(trial.to_dict())

