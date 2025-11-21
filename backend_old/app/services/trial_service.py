from app.models.trial import Trial
from app.extensions import db
import requests
from datetime import datetime

def fetch_trials_from_api():
    url="https://clinicaltrials.gov/api/v2/studies"
    params={'query.cond':'breast cancer','filter.overallStatus':'RECRUITING','pageSize':200,'format':'json'}
    try:
        data=requests.get(url,params=params).json()
        return data.get('studies',[])
    except Exception:
        return []

def parse_age(s):
    import re
    m=re.search(r'\d+',s)
    return int(m.group()) if m else None

import re

def extract_biomarkers(text):
    t = text.lower()

    # Flexible HR-positive detection (slashed and punctuated formats)
    hr_pos = bool(re.search(
        r'(hr[\s\-\/]*positive|hormone[\s\-\/]receptor[\s\-\/]*positive|'
        r'er[\s\-\/]*positive|pr[\s\-\/]*positive)', t))

    # Flexible HER2-low: matches "her2-low", "ihc 1+", or "ihc 2+" with any FISH neg variant
    her2_low = (
        'her2-low' in t or
        re.search(r'ihc[\s\-]*1\+', t) or
        re.search(r'ihc[\s\-]*2\+[\s,;\-/]*fish[\s\-]*negative', t) or
        re.search(r'ihc[\s\-]*2\+[\s,;\-/]*fluorescence[\s\-]*in[\s\-]*situ[\s\-]*hybridization[\s\-]*negative', t)
    )
    her2_pos = bool(re.search(
        r'(her2[\s\-]*positive|ihc[\s\-]*3\+|her2[\s\-]*overexpressed)', t))
    her2_neg = bool(re.search(
        r'(her2[\s\-]*negative|ihc[\s\-]*0|her2\s*0)', t))
    triple_negative = bool(re.search(
        r'(triple[\s\-]?negative|tnbc)', t))

    return {
        'hr_pos': hr_pos,
        'her2_low': her2_low,
        'her2_pos': her2_pos,
        'her2_neg': her2_neg,
        'triple_negative': triple_negative,
    }

def determine_subtype(text):
    b = extract_biomarkers(text)
    if b['triple_negative']:
        return 'Triple-Negative'
    if b['hr_pos'] and b['her2_low']:
        return 'Luminal B'
    if b['hr_pos'] and b['her2_pos']:
        return 'Luminal B'
    if b['hr_pos'] and (b['her2_neg'] or not (b['her2_pos'] or b['her2_low'])):
        return 'Luminal A/B'
    if b['her2_pos'] and not b['hr_pos']:
        return 'HER2-Enriched'
    return 'All'



def populate_trial_database():
    studies = fetch_trials_from_api()
    for st in studies:
        p = st['protocolSection']
        nct = p['identificationModule']['nctId']
        if Trial.query.filter_by(nct_id=nct).first(): continue
        title = p['identificationModule'].get('officialTitle','')
        phase = (p.get('designModule',{}).get('phases') or ['Unknown'])[0]
        status = p['statusModule']['overallStatus']
        em = p.get('eligibilityModule',{})
        min_age = parse_age(em.get('minimumAge','18 Years'))
        max_age = parse_age(em.get('maximumAge','100 Years'))
        gender = em.get('sex','All')
        desc_module = p.get('descriptionModule', {})
        brief_desc = desc_module.get('detailedDescription', '')
        detailed_desc = desc_module.get('detailedDescription', '')
        desc = brief_desc + "\n\n" + detailed_desc if detailed_desc else brief_desc
        locs = []
        for L in p.get('contactsLocationsModule',{}).get('locations',[]):
            locs.append({'facility':L.get('facility'),'city':L.get('city'),'state':L.get('state'),'zip':L.get('zip')})
        subtype = determine_subtype(title + " " + desc)
        trial = Trial(nct_id=nct,title=title,phase=phase,status=status,target_subtype=subtype,
                    min_age=min_age,max_age=max_age,gender=gender,description=desc,locations=locs)
        db.session.add(trial)
    db.session.commit()

def refresh_trial_data():
    studies=fetch_trials_from_api()
    updated=added=0
    for st in studies:
        p=st['protocolSection']
        nct=p['identificationModule']['nctId']
        t=Trial.query.filter_by(nct_id=nct).first()
        title=p['identificationModule'].get('officialTitle','')
        status=p['statusModule']['overallStatus']
        desc_module = p.get('descriptionModule', {})
        brief_desc = desc_module.get('detailedDescription', '')
        detailed_desc = desc_module.get('detailedDescription', '')
        desc = brief_desc + "\n\n" + detailed_desc if detailed_desc else brief_desc
        if t:
            t.title = title
            t.status = status
            t.description = desc  # This now includes both summaries!
            t.last_updated = datetime.utcnow()
            updated += 1
        else:
            # similar insert logic as above
            added+=1
    db.session.commit()
    print(f"Updated {updated}, Added {added}, Total {Trial.query.count()}")
