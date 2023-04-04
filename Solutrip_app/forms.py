from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from Solutrip_app.models import User, UserInfo, Company

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
    cv = FileField('Upload your CV', validators=[FileRequired(), FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Update')

class RequestPassForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')

    def validate_email (self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('There is no account with that mail. Please register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class DeleteAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Delete Account')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tag = SelectField('Tag', choices=[('technology', 'Technology'), ('science', 'Science'), ('education', 'Education'), ('jobs', 'Jobs')], validators=[DataRequired()], render_kw={"class": "form-control"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"rows": 10, "style": "height: 300px; width: 100%;"})
    submit = SubmitField('Post', render_kw={"class": " btn btn-primary"})

class CompanyForm(FlaskForm):
    companyname = StringField('Company Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()]) 
    location = StringField('Location', validators=[DataRequired()])
    industry = SelectField('Industry', choices=[('software_development', 'Software Development'), ('network_and_system_administration', 'Network and System Administration'), ('cyber_security', 'Cyber Security'), ('cloud_computing', 'Cloud Computing'), ('mobile_app_development', 'Mobile App Development'), ('recruitment', 'Recruitment'), ('data', 'Data'), ('web_development_and_design', 'Web Development and Design'), ('digital_marketing', 'Digital Marketing'), ('game_development', 'Game Development'), ('artificial_intelligence', 'Artificial Intelligence'), ('customer_service', 'Customer Service') ], validators=[DataRequired()], render_kw={"class": "form-control"})
    phone = StringField('Phone', validators=[DataRequired()])
    website = StringField('Website', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"rows": 5, "style": "height: 120px; width: 100%;"})
    qualifications = TextAreaField('Responsibilities', validators=[DataRequired()], render_kw={"rows": 8, "style": "height: 150px; width: 100%;"}) 
    requirements = TextAreaField('Requirements', validators=[DataRequired()], render_kw={"rows": 8, "style": "height: 150px; width: 100%;"})
    company_id =SelectField('Company', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_id.choices = [(c.id, c.companyname) for c in Company.query.all()]