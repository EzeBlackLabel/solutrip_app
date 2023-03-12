from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField
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
    profession = SelectField('Profession', choices=[('software_developer', 'Software Developer'), ('front_end_developer', 'Front End Developer'), ('back_end_developer', 'Back End Developer'), ('full_stack_developer', 'Full Stack Developer'), ('mobile_developer', 'Mobile Developer'), ('data_scientist', 'Data Scientist'), ('data_analyst', 'Data Analyst'), ('network_engineer', 'Network Engineer'), ('database_administrator', 'Database Administrator'), ('security_analyst', 'Security Analyst'), ('cloud_architect', 'Cloud Architect'), ('artificial_intelligence_engineer', 'Artificial Intelligence Engineer'), ('designer', 'Designer'), ('customer_service', 'Customer Service'), ('other', 'Other') ], validators=[DataRequired()], render_kw={"class": "form-control"})
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


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tag = SelectField('Tag', choices=[('technology', 'Technology'), ('science', 'Science'), ('education', 'Education'), ('jobs', 'Jobs')], validators=[DataRequired()], render_kw={"class": "form-control"})
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Confirm', render_kw={"class": " btn btn-primary"})

