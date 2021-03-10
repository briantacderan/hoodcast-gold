from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login

class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cik_str = db.Column(db.String(140), index=True)
    ticker = db.Column(db.String(140), index=True, unique=True)
    title = db.Column(db.String(140), index=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    statements = db.relationship('Statement', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return '<Company {}>'.format(self.title)

class Statement(UserMixin, db.Model):
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
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    api_key = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#@login.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None
