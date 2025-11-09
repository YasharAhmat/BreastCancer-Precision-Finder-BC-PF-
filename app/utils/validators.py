def validate_patient_data(data):
    if 'age' not in data or not isinstance(data['age'],int) or data['age']<18 or data['age']>120:
        return False,"Invalid age"
    bm=data.get('biomarkers',{})
    for m in ['er_status','pr_status','her2_status']:
        if m not in bm or bm[m] not in ['Positive','Negative','Unknown']:
            return False,f"Invalid {m}"
    if 'gender' in data and data['gender'] not in ['Female','Male','Other']:
        return False,"Invalid gender"
    return True,"Valid"
