from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from Solutrip_app.models import User, UserInfo

class RegistrationForm(FlaskForm):
    # To validate that user write some data and user name has some specific lenght.
    username = StringField('Username',
                             validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username')

    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username')

    remember = BooleanField('Remember me')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    # To keep the user login.
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('That username is not registered yet. Please register first')

class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()]) 
    location = StringField('Location', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    profession = StringField('Profession', validators=[DataRequired()])
    education = StringField('Education', validators=[DataRequired()])
    linkedin = StringField('Linkedin', validators=[DataRequired()])
    github_account = StringField('Github account', validators=[DataRequired()], description='Enter your cryptocurrency account address. If you do not have, write *')
    cv = FileField('Upload your CV', validators=[FileAllowed(['pdf', 'doc', 'docx'])])
    submit = SubmitField('Update')

class RequestPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email (self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('Email is not registered yet. Please register first')
