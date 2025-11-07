from app.extensions import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100))
    gender = db.Column(db.String(20), default='Female')
    er_status = db.Column(db.String(20))
    pr_status = db.Column(db.String(20))
    her2_status = db.Column(db.String(20))
    subtype = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    matches = db.relationship('Match', backref='patient', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'age': self.age,
            'location': self.location,
            'gender': self.gender,
            'biomarkers': {
                'er_status': self.er_status,
                'pr_status': self.pr_status,
                'her2_status': self.her2_status
            },
            'subtype': self.subtype,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
