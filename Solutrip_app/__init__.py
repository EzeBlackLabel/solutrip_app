from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# Always create a secret key for the app.
app.config['SECRET_KEY'] = 'ffeaeae4d2ba6634d217528a4de4b8a2'
#Database set up
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solutrip_site.db'
db = SQLAlchemy(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from Solutrip_app import routes