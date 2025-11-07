import json
from app.models.trial import Trial
from app.extensions import db

def test_get_trials(client, app):
    with app.app_context():
        trial = Trial(
            nct_id='NCT00000001',
            title='Test Trial',
            phase='Phase II',
            status='Recruiting',
            target_subtype='Triple-Negative',
            min_age=18,
            max_age=65
        )
        db.session.add(trial)
        db.session.commit()
    resp = client.get('/api/trials/')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['count'] > 0
    assert 'trials' in data

def test_get_trial_by_nct_id(client, app):
    with app.app_context():
        trial = Trial(
            nct_id='NCT00000002',
            title='HER2 Study',
            phase='Phase III',
            status='Recruiting',
            target_subtype='HER2-Positive'
        )
        db.session.add(trial)
        db.session.commit()
    resp = client.get('/api/trials/NCT00000002')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['nct_id'] == 'NCT00000002'
    assert data['title'] == 'HER2 Study'

def test_match_trials(client, app):
    # Create trial
    with app.app_context():
        trial = Trial(
            nct_id='NCT00000003',
            title='TNBC Match',
            phase='Phase III',
            status='Recruiting',
            target_subtype='Triple-Negative',
            min_age=30,
            max_age=80,
            locations=[{'facility': 'Test Hospital', 'city': 'Philly', 'state': 'PA', 'zip': '19104'}]
        )
        db.session.add(trial)
        db.session.commit()
    # Direct patient data
    response = client.post('/api/trials/match', json={
        'age': 35,
        'biomarkers': {
            'er_status': 'Negative',
            'pr_status': 'Negative',
            'her2_status': 'Negative'
        }
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] > 0
    match = data['matches'][0]
    assert 'trial' in match
    assert 'confidence' in match
    assert 'reasons' in match
    assert 'recommendation' in match

def test_filter_trials(client, app):
    with app.app_context():
        tn_trial = Trial(
            nct_id='NCT00000004',
            title='TN Filter',
            phase='Phase II',
            status='Recruiting',
            target_subtype='Triple-Negative',
            min_age=21,
            max_age=64
        )
        lum_trial = Trial(
            nct_id='NCT00000005',
            title='Lum Filter',
            phase='Phase III',
            status='Recruiting',
            target_subtype='Luminal A/B',
            min_age=18,
            max_age=70
        )
        db.session.add_all([tn_trial, lum_trial])
        db.session.commit()
    resp = client.get('/api/trials/filter?subtype=Triple-Negative')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['count'] == 1
    assert data['trials'][0]['target_subtype'] == 'Triple-Negative'
