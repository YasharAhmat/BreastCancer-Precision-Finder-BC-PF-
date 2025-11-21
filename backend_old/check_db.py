from app import create_app
from app.models.trial import Trial

app = create_app()
with app.app_context():
    count = Trial.query.count()
    print(f"Total trials in database: {count}")

    if count > 0:
        trial = Trial.query.first()
        print(f"\nFirst trial:")
        print(f"NCT ID: {trial.nct_id}")
        print(f"trial.min_age: {trial.min_age}")
        print(f"trial.max_age: {trial.max_age}")
        print(f"trial.gender: {trial.gender}")
        print(f"trial.target_subtype: {trial.target_subtype}")
    else:
        print("\n⚠️  No trials found in database!")
        print("You need to populate the database first.")
