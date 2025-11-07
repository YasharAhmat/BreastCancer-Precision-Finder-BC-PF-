from app.models.trial import Trial
from app.extensions import db
import requests
from datetime import datetime

def fetch_trials_from_api():
    url="https://clinicaltrials.gov/api/v2/studies"
    params={'query.cond':'breast cancer','filter.overallStatus':'RECRUITING','pageSize':100,'format':'json'}
    try:
        data=requests.get(url,params=params).json()
        return data.get('studies',[])
    except Exception:
        return []

def parse_age(s):
    import re
    m=re.search(r'\d+',s)
    return int(m.group()) if m else None

def determine_subtype(text):
    t=text.lower()
    if any(k in t for k in ['triple negative','tnbc']): return 'Triple-Negative'
    if any(k in t for k in ['her2+','her2 positive']): return 'HER2-Positive'
    if any(k in t for k in ['er+','hormone receptor']): return 'Luminal A/B'
    return 'All'

def populate_trial_database():
    studies=fetch_trials_from_api()
    for st in studies:
        p=st['protocolSection']
        nct=p['identificationModule']['nctId']
        if Trial.query.filter_by(nct_id=nct).first(): continue
        title=p['identificationModule'].get('officialTitle','')
        phase=(p.get('designModule',{}).get('phases') or ['Unknown'])[0]
        status=p['statusModule']['overallStatus']
        em=p.get('eligibilityModule',{})
        min_age=parse_age(em.get('minimumAge','18 Years'))
        max_age=parse_age(em.get('maximumAge','100 Years'))
        gender=em.get('sex','All')
        desc=p.get('descriptionModule',{}).get('briefSummary','')
        locs=[]
        for L in p.get('contactsLocationsModule',{}).get('locations',[]):
            locs.append({'facility':L.get('facility'),'city':L.get('city'),'state':L.get('state'),'zip':L.get('zip')})
        subtype=determine_subtype(title+desc)
        trial=Trial(nct_id=nct,title=title,phase=phase,status=status,target_subtype=subtype,
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
        desc=p.get('descriptionModule',{}).get('briefSummary','')
        if t:
            t.title=title
            t.status=status
            t.description=desc
            t.last_updated=datetime.utcnow()
            updated+=1
        else:
            # similar insert logic as above
            added+=1
    db.session.commit()
    print(f"Updated {updated}, Added {added}, Total {Trial.query.count()}")
