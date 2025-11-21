from app.extensions import db
from datetime import datetime


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255))
    gender = db.Column(db.String(50), default='Female')

    # Biomarker fields
    er_status = db.Column(db.String(20))
    pr_status = db.Column(db.String(20))
    her2_status = db.Column(db.String(20))

    # Computed/derived field
    subtype = db.Column(db.String(50))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    matches = db.relationship('Match', backref='patient', cascade='all, delete-orphan')

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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
