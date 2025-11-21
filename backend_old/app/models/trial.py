from app.extensions import db
from datetime import datetime


class Trial(db.Model):
    __tablename__ = 'trials'

    id = db.Column(db.Integer, primary_key=True)
    nct_id = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    phase = db.Column(db.String(50))
    status = db.Column(db.String(50))
    description = db.Column(db.Text)

    # Eligibility
    target_subtype = db.Column(db.String(50))
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    gender = db.Column(db.String(50))

    # JSON fields
    eligibility_criteria = db.Column(db.JSON)
    locations = db.Column(db.JSON)

    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    matches = db.relationship('Match', backref='trial', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'nct_id': self.nct_id,
            'title': self.title,
            'phase': self.phase,
            'status': self.status,
            'description': self.description,
            'target_subtype': self.target_subtype,
            'eligibility': {
                'min_age': self.min_age,
                'max_age': self.max_age,
                'gender': self.gender
            },
            'locations': self.locations or [],
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
