from datetime import datetime
from app import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cik_str = db.Column(db.String(140), index=True)
    ticker = db.Column(db.String(140), index=True, unique=True)
    title = db.Column(db.String(140), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    statements = db.relationship('Statement', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return '<Company {}>'.format(self.title)

class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(140), index=True)
    year = db.Column(db.String(140), index=True)
    company = db.Column(db.String(140), index=True)
    bs = db.Column(db.String(140), index=True, unique=True)
    income = db.Column(db.String(140), index=True, unique=True)
    ops = db.Column(db.String(140), index=True, unique=True)
    equity = db.Column(db.String(140), index=True, unique=True)
    cash = db.Column(db.String(140), index=True, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return '<Statement {}>'.format(self.form_type)
