from flask import Blueprint, request, jsonify
from app.models.trial import Trial
from app.models.patient import Patient
from app.services.match_service import match_patient_to_trials
from app.utils.formatters import format_error_response, format_match_results

bp = Blueprint('trials', __name__, url_prefix='/api/trials')

@bp.route('/', methods=['GET'])
def get_trials():
    subtype = request.args.get('subtype')
    phase = request.args.get('phase')
    status = request.args.get('status','Recruiting')
    q = Trial.query
    if subtype: q = q.filter_by(target_subtype=subtype)
    if phase: q = q.filter_by(phase=phase)
    if status: q = q.filter_by(status=status)
    trials = q.all()
    return jsonify({'count': len(trials),'trials':[t.to_dict() for t in trials]}), 200

@bp.route('/<string:nct_id>', methods=['GET'])
def get_trial(nct_id):
    trial = Trial.query.filter_by(nct_id=nct_id).first_or_404()
    return jsonify(trial.to_dict()), 200

@bp.route('/match', methods=['POST'])
def match_trials():
    data = request.json
    pid = data.get('patient_id')
    if pid:
        patient = Patient.query.get_or_404(pid)
        pdata = patient.to_dict()
    else:
        pdata = data
    maxd = data.get('max_distance_miles',50)
    phases = data.get('preferred_phases',[])
    matches = match_patient_to_trials(pdata,max_distance=maxd,preferred_phases=phases)
    return jsonify(format_match_results(matches)), 200

@bp.route('/filter', methods=['GET'])
def filter_trials():
    f = {
        'subtype': request.args.get('subtype'),
        'min_age': request.args.get('min_age',type=int),
        'max_age': request.args.get('max_age',type=int),
        'phase': request.args.get('phase'),
        'location': request.args.get('location')
    }
    q = Trial.query
    if f['subtype']: q = q.filter_by(target_subtype=f['subtype'])
    if f['phase']: q = q.filter_by(phase=f['phase'])
    if f['min_age']: q = q.filter(Trial.max_age>=f['min_age'])
    if f['max_age']: q = q.filter(Trial.min_age<=f['max_age'])
    trials = q.all()
    return jsonify({'count':len(trials),'trials':[t.to_dict() for t in trials]}), 200
