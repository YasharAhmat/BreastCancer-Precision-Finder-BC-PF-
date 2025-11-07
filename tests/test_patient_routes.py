import json

def test_create_patient(client):
    response = client.post('/api/patient/', json={
        'age': 45,
        'location': 'Philadelphia, PA',
        'gender': 'Female',
        'biomarkers': {
            'er_status': 'Negative',
            'pr_status': 'Negative',
            'her2_status': 'Negative'
        }
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['age'] == 45
    assert data['subtype'] == 'Triple-Negative'
    assert 'id' in data

def test_get_patient(client):
    response = client.post('/api/patient/', json={
        'age': 53,
        'biomarkers': {
            'er_status': 'Positive',
            'pr_status': 'Positive',
            'her2_status': 'Negative'
        }
    })
    patient_id = json.loads(response.data)['id']
    get_resp = client.get(f'/api/patient/{patient_id}')
    assert get_resp.status_code == 200
    data = json.loads(get_resp.data)
    assert data['age'] == 53
    assert data['subtype'] == 'Luminal A/B'

def test_update_patient(client):
    response = client.post('/api/patient/', json={
        'age': 44,
        'biomarkers': {
            'er_status': 'Negative',
            'pr_status': 'Positive',
            'her2_status': 'Negative'
        }
    })
    patient_id = json.loads(response.data)['id']
    upd = client.put(f'/api/patient/{patient_id}', json={'age': 45, 'location': 'Boston'})
    assert upd.status_code == 200
    data = json.loads(upd.data)
    assert data['age'] == 45
    assert data['location'] == 'Boston'

def test_delete_patient(client):
    response = client.post('/api/patient/', json={
        'age': 41,
        'biomarkers': {
            'er_status': 'Negative',
            'pr_status': 'Negative',
            'her2_status': 'Negative'
        }
    })
    patient_id = json.loads(response.data)['id']
    delresp = client.delete(f'/api/patient/{patient_id}')
    assert delresp.status_code == 204
    getresp = client.get(f'/api/patient/{patient_id}')
    assert getresp.status_code == 404
