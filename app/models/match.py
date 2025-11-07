from app.extensions import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    trial_id = db.Column(db.Integer, db.ForeignKey('trials.id'), nullable=False)
    confidence_score = db.Column(db.Float)
    match_reasons = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'trial': self.trial.to_dict(),
            'confidence': self.confidence_score,
            'reasons': self.match_reasons,
            'created_at': self.created_at.isoformat()
        }
