from Solutrip_app import db, login_manager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String(64), unique=True, nullable=False) 
    email = db.Column (db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    role = db.Column(db.String(20), nullable=False, default='user')
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(100), unique=True)

    def get_reset_token (self, expires_sec =1800):
         s = Serializer(app.config['SECRET_KEY'], expires_sec)
         return s.dumps({'user.id': self.id}).decode('utf-8')
    
    #Validate Token
    @staticmethod
    def validate_token_confirmation(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data['user_id']
            confirmed = data['confirmed']
        except:
            return None
        return User.query.get(user_id) if confirmed else None
    
    def validate_token_reset(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    #Link to tables.
    user_info = db.relationship('UserInfo', backref='user', lazy=True)
    author = db.relationship('Post', backref='author', lazy=True )

class UserInfo(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(60)) 
    surname = db.Column(db.String(60)) 
    location = db.Column(db.String(60)) 
    phone = db.Column(db.String(20), nullable=True)
    linkedin = db.Column(db.String(100))
    profession = db.Column(db.String(200))
    education = db.Column(db.String(200))
    github_account = db.Column(db.String(50))
    cv = db.Column(db.LargeBinary, nullable=True) 
    #Link to user.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #Link to the Job Application
    job_applications = db.relationship('JobApplication', backref='user', lazy=True)


class Company(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    companyname = db.Column (db.String(80), unique=True, nullable=False) 
    email = db.Column (db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(60), nullable=False)
    industry = db.Column(db.String(60), nullable=False) 
    phone = db.Column(db.String(60), unique=True, nullable=False)
    website = db.Column(db.String(100), nullable=False)

class Jobs(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False) 
    location = db.Column(db.String(60), nullable=False) 
    salary = db.Column(db.String(60), nullable=False) 
    description = db.Column(db.Text, nullable=False) 
    requirements= db.Column(db.Text, nullable=False) 
    qualifications= db.Column(db.Text, nullable=False)
    #Link to Company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    #Link to Job Application
    job_applications = db.relationship('JobApplication', backref='job', lazy=True)

class Post(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    tag = db.Column(db.String(60), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    #Link to Company
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pending')
    # Link to Jobs table
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applied_job = db.relationship('Jobs', backref='applications')
    # Link to UserInfo table
    user_info_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    user_info = db.relationship('UserInfo', backref='applications')

