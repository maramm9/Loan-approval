from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'

class LoanRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    gender = db.Column(db.String(10))
    married = db.Column(db.String(3))
    dependents = db.Column(db.Integer)
    education = db.Column(db.String(20))
    self_employed = db.Column(db.String(3))
    applicant_income = db.Column(db.Float)
    coapplicant_income = db.Column(db.Float)
    loan_amount = db.Column(db.Float)
    loan_term = db.Column(db.Float)
    credit_history = db.Column(db.Float)
    property_area = db.Column(db.String(20))
    prediction = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)