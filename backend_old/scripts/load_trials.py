import csv
import sys
import json
from app import create_app
from app.models.trial import Trial
from app.extensions import db

def load_csv(csv_path):
    app = create_app()
    with app.app_context():
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if Trial.query.filter_by(nct_id=row['nct_id']).first():
                    continue  # skip duplicates
                locs = json.loads(row['locations'])
                trial = Trial(
                    nct_id=row['nct_id'],
                    title=row['title'],
                    phase=row['phase'],
                    status=row['status'],
                    target_subtype=row['target_subtype'],
                    min_age=int(row['min_age']),
                    max_age=int(row['max_age']),
                    gender=row['gender'],
                    description=row['description'],
                    locations=locs
                )
                db.session.add(trial)
        db.session.commit()
        print("Trials loaded")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/load_trials.py path/to/trials.csv")
    else:
        load_csv(sys.argv[1])
