from app.models.trial import Trial

def classify_subtype(bm):
    er,pr,her2 = bm.get('er_status','').lower(),bm.get('pr_status','').lower(),bm.get('her2_status','').lower()
    if 'negative' in er and 'negative' in pr and 'negative' in her2: return 'Triple-Negative'
    if 'positive' in her2: return 'HER2-Positive'
    if 'positive' in er or 'positive' in pr: return 'Luminal A/B'
    return 'All'

def match_patient_to_trials(pd,max_distance=50,preferred_phases=None):
    age,bm,subtype = pd.get('age'),pd.get('biomarkers',{}),pd.get('subtype') or classify_subtype(pd.get('biomarkers',{}))
    q=Trial.query.filter_by(status='Recruiting')
    q=q.filter((Trial.target_subtype==subtype)|(Trial.target_subtype=='All'))
    if preferred_phases: q=q.filter(Trial.phase.in_(preferred_phases))
    trials=q.all()
    matches=[]
    for t in trials:
        score=calculate_confidence_score(pd,t,subtype)
        if score>=50:
            matches.append({'trial':t,'confidence':score,'reasons':get_match_reasons(pd,t,subtype)})
    matches.sort(key=lambda x:x['confidence'],reverse=True)
    return matches

def calculate_confidence_score(pd,t,subtype):
    score=0
    if t.target_subtype==subtype: score+=40
    elif t.target_subtype=='All': score+=30
    age=pd.get('age')
    if age and t.min_age and t.max_age and t.min_age<=age<=t.max_age: score+=20
    if t.gender in ('All',pd.get('gender','Female')): score+=10
    if t.locations: score+=15
    if t.status=='Recruiting': score+=10
    if t.locations and len(t.locations)>1: score+=5
    return min(max(score,0),100)

def get_match_reasons(pd,t,subtype):
    r=[]
    if t.target_subtype==subtype: r.append(f"Trial targets {subtype} breast cancer")
    elif t.target_subtype=='All': r.append("Trial accepts all subtypes")
    age=pd.get('age')
    if age and t.min_age and t.max_age and t.min_age<=age<=t.max_age:
        r.append(f"Age {age} within range ({t.min_age}-{t.max_age})")
    if t.gender=='All': r.append("Trial open to all genders")
    elif t.gender==pd.get('gender','Female'): r.append(f"Trial accepts {pd.get('gender')}")
    if t.locations:
        loc=t.locations[0]
        r.append(f"Trial site at {loc.get('facility','nearby')}, {loc.get('city','')}, {loc.get('state','')}")
        if len(t.locations)>1: r.append(f"{len(t.locations)} sites available")
    r.append(f"{t.phase} study ({t.status})")
    return r
