from app import create_app
from app.models import Trial

app = create_app()
with app.app_context():
    for trial in Trial.query.limit(5).all():
        print(trial.to_dict())
