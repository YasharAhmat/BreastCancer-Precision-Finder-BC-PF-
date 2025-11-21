from flask import Blueprint, request, jsonify
from app.models.patient import Patient
from app.extensions import db
from app.utils.validation import validate_patient_data
from app.utils.formatters import format_error_response
from app.services.match_service import classify_subtype

bp = Blueprint('patient', __name__, url_prefix='/api/patient')


@bp.route('/', methods=['POST'])
def create_patient():
    data = request.json
    is_valid, msg = validate_patient_data(data)
    if not is_valid:
        return format_error_response(msg, 400)

    subtype = classify_subtype(data['biomarkers'])
    patient = Patient(
        age=data['age'],
        location=data.get('location'),
        gender=data.get('gender', 'Female'),
        er_status=data['biomarkers']['er_status'],
        pr_status=data['biomarkers']['pr_status'],
        her2_status=data['biomarkers']['her2_status'],
        subtype=subtype
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201


@bp.route('/', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict()), 200


@bp.route('/', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    patient = Patient.query.get_or_404(patient_id)
    if 'age' in data: patient.age = data['age']
    if 'location' in data: patient.location = data['location']
    if 'gender' in data: patient.gender = data['gender']
    if 'biomarkers' in data:
        bm = data['biomarkers']
        patient.er_status = bm.get('er_status', patient.er_status)
        patient.pr_status = bm.get('pr_status', patient.pr_status)
        patient.her2_status = bm.get('her2_status', patient.her2_status)
        patient.subtype = classify_subtype({
            'er_status': patient.er_status,
            'pr_status': patient.pr_status,
            'her2_status': patient.her2_status
        })
    db.session.commit()
    return jsonify(patient.to_dict()), 200


@bp.route('/', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return '', 204
