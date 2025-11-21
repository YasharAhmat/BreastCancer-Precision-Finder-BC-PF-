from app.models.trial import Trial
from sqlalchemy import or_, func


def classify_subtype(biomarkers):
    er = biomarkers.get('er_status', 'Unknown')
    pr = biomarkers.get('pr_status', 'Unknown')
    her2 = biomarkers.get('her2_status', 'Unknown')
    if er == 'Negative' and pr == 'Negative' and her2 == 'Negative':
        return 'Triple-Negative'
    if her2 == 'Positive':
        return 'HER2-Positive'
    if er == 'Positive' or pr == 'Positive':
        return 'Luminal A/B'
    return 'Unknown'


def match_patient_to_trials(patient_data, max_distance=50, preferred_phases=None):
    age = patient_data.get('age')
    subtype = patient_data.get('subtype')
    if subtype is None:
        biomarkers = patient_data.get('biomarkers', {})
        subtype = classify_subtype(biomarkers)

    # Normalize subtype to lowercase for case-insensitive comparison
    subtype = (subtype or '').strip().lower()

    # Case-insensitive status filter
    q = Trial.query.filter(func.lower(Trial.status) == 'recruiting')

    # Case-insensitive subtype filter
    q = q.filter(
        or_(
            func.lower(Trial.target_subtype) == subtype,
            func.lower(Trial.target_subtype) == 'all'
        )
    )

    if preferred_phases:
        q = q.filter(Trial.phase.in_(preferred_phases))

    trials = q.all()
    print(f"Found {len(trials)} trials after filtering")

    matches = []
    for trial in trials:
        # Normalize gender for case-insensitive comparison
        gender = (patient_data.get('gender', 'Female') or '').lower()
        trial_gender = (trial.gender or '').lower()

        # Check gender eligibility
        if trial_gender != 'all' and trial_gender != gender:
            print(f"SKIP {trial.nct_id}: gender mismatch ({trial_gender} vs {gender})")
            continue

        # Check age eligibility with safe defaults
        t_min_age = trial.min_age if trial.min_age is not None else 0
        t_max_age = trial.max_age if trial.max_age is not None else 130
        if age < t_min_age or age > t_max_age:
            print(f"SKIP {trial.nct_id}: age {age} not in range {t_min_age}-{t_max_age}")
            continue

        score = calculate_confidence_score(patient_data, trial, subtype)
        if score >= 50:
            reasons = get_match_reasons(patient_data, trial, subtype)
            matches.append({
                'trial': trial,
                'confidence': score,
                'reasons': reasons
            })
            print(f"MATCH {trial.nct_id}: score={score}")
        else:
            print(f"SKIP {trial.nct_id}: score {score} < 50")

    matches.sort(key=lambda x: x['confidence'], reverse=True)
    return matches


def calculate_confidence_score(patient_data, trial, subtype):
    score = 0
    trial_subtype = (trial.target_subtype or '').lower()
    if trial_subtype == subtype:
        score += 40
    elif trial_subtype == 'all':
        score += 30

    age = patient_data.get('age')
    t_min_age = trial.min_age if trial.min_age is not None else 0
    t_max_age = trial.max_age if trial.max_age is not None else 130
    if t_min_age <= age <= t_max_age:
        score += 20

    gender = (patient_data.get('gender', 'Female') or '').lower()
    trial_gender = (trial.gender or '').lower()
    if trial_gender == 'all' or trial_gender == gender:
        score += 10

    if trial.locations:
        score += 15
    if (trial.status or '').lower() == 'recruiting':
        score += 10
    if len(trial.locations or []) > 1:
        score += 5
    return min(max(score, 0), 100)


def get_match_reasons(patient_data, trial, subtype):
    reasons = []
    trial_subtype = (trial.target_subtype or '').lower()
    if trial_subtype == subtype:
        reasons.append(f"Trial targets {subtype} breast cancer")
    elif trial_subtype == 'all':
        reasons.append("Trial accepts all breast cancer subtypes")

    age = patient_data.get('age')
    t_min_age = trial.min_age if trial.min_age is not None else 0
    t_max_age = trial.max_age if trial.max_age is not None else 130
    if t_min_age <= age <= t_max_age:
        reasons.append(f"Age {age} within range ({t_min_age}-{t_max_age})")

    gender = (patient_data.get('gender', 'Female') or '').lower()
    trial_gender = (trial.gender or '').lower()
    if trial_gender == 'all':
        reasons.append("Trial open to all genders")
    elif trial_gender == gender:
        reasons.append(f"Trial accepts {gender.title()} patients")

    if trial.locations:
        loc = trial.locations[0]
        reasons.append(f"Trial site at {loc.get('facility', '')}, {loc.get('city', '')}, {loc.get('state', '')}")
        if len(trial.locations) > 1:
            reasons.append(f"{len(trial.locations)} sites available")
    if trial.phase:
        reasons.append(f"{trial.phase} study ({trial.status})")
    return reasons
