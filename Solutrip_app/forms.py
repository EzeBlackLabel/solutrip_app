from flask_wtf import FlaskForm
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
    # To validate that user write some data and user name has some specific lenght.
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()]) 
    location = StringField('Location', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    skill = StringField('Skill', validators=[DataRequired()])
    crypto_account = StringField('Crypto account', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username')

    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another username')