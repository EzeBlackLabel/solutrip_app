from Solutrip_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String(64), unique=True, nullable=False) 
    email = db.Column (db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #Link to tables.
    user_info = db.relationship('UserInfo', backref='user', lazy=True)
    companies = db.relationship('Company', backref='user', lazy=True) 

class UserInfo(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(60)) 
    surname = db.Column(db.String(60)) 
    location = db.Column(db.String(60)) 
    phone = db.Column(db.String(60), unique=True)
    skill = db.Column(db.String(100))
    crypto_account = db.Column(db.String(50), unique=True)
    #Link to user.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Company(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    companyname = db.Column (db.String(80), unique=True, nullable=False) 
    email = db.Column (db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    industry = db.Column(db.String(60), nullable=False) 
    phone = db.Column(db.String(60), unique=True, nullable=False)
    website = db.Column(db.String(100), nullable=False)
    #Link to User, UserInfo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_info_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)  
