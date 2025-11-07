from app.services.match_service import (
    classify_subtype,
    calculate_confidence_score,
    get_match_reasons
)
from app.models.trial import Trial

def test_classify_triple_negative():
    biomarkers = {
        'er_status': 'Negative',
        'pr_status': 'Negative',
        'her2_status': 'Negative'
    }
    subtype = classify_subtype(biomarkers)
    assert subtype == 'Triple-Negative'

def test_classify_her2_positive():
    biomarkers = {
        'er_status': 'Positive',
        'pr_status': 'Positive',
        'her2_status': 'Positive'
    }
    subtype = classify_subtype(biomarkers)
    assert subtype == 'HER2-Positive'

def test_classify_luminal():
    biomarkers = {
        'er_status': 'Positive',
        'pr_status': 'Negative',
        'her2_status': 'Negative'
    }
    subtype = classify_subtype(biomarkers)
    assert subtype == 'Luminal A/B'

def test_confidence_score_calculation():
    patient = {
        'age': 50,
        'gender': 'Female',
        'subtype': 'Triple-Negative',
        'biomarkers': {
            'er_status': 'Negative',
            'pr_status': 'Negative',
            'her2_status': 'Negative'
        }
    }
    trial = Trial(
        target_subtype='Triple-Negative',
        min_age=18,
        max_age=65,
        gender='All',
        status='Recruiting',
        locations=[{'facility': 'Penn', 'city': 'Philly', 'state': 'PA'}]
    )
    score = calculate_confidence_score(patient, trial, 'Triple-Negative')
    assert score >= 70 and score <= 100

def test_match_reasons_generation():
    patient = {
        'age': 55,
        'subtype': 'Luminal A/B',
        'gender': 'Female'
    }
    trial = Trial(
        target_subtype='Luminal A/B',
        min_age=18,
        max_age=65,
        gender='Female',
        phase='Phase III',
        status='Recruiting',
        locations=[{'facility': 'U Penn', 'city': 'Philadelphia', 'state': 'PA'}]
    )
    reasons = get_match_reasons(patient, trial, 'Luminal A/B')
    assert any('Luminal' in r for r in reasons)
    assert any('within range' in r or 'Age' in r for r in reasons)
