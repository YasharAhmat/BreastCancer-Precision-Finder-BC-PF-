def validate_patient_data(data):
    if not data.get('age'):
        return False, "Age is required"
    age = data['age']
    if not isinstance(age, int) or age < 18 or age > 120:
        return False, "Invalid age"
    if 'biomarkers' not in data:
        return False, "Biomarkers are required"
    bm = data['biomarkers']
    valid_statuses = ['Positive', 'Negative', 'Unknown']
    for key in ['er_status', 'pr_status', 'her2_status']:
        if key not in bm or bm[key] not in valid_statuses:
            return False, f"Invalid {key}"
    return True, "Valid"
