from Solutrip_app import app,db
from flask import render_template, url_for, flash, redirect
from Solutrip_app.models import User, UserInfo, Company
from Solutrip_app.forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user

@app.route("/")
@app.route("/home")

def home():
    return render_template("index.html")
    
@app.route("/candidates")
def candidates():
    return render_template("candidates.html")

@app.route("/employers")
def employers():
    return render_template("employers.html", title = "Employers")

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/register", methods= ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Hashing
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # Check if user with the same email already exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("An account with this email already exists!", "danger")
            return redirect(url_for('login'))
        # Create a new user with the provided details
        user = User(
            username=form.username.data,
            email=form.email.data,
            password= hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # Import Flash and send a confirmation message.
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash (user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            flash(f"Login successful { form.email.data }!", "success")
            return redirect(url_for('about'))
        else:    
            flash(f"Login unsuccessful, please check username and password.", "danger")
    return render_template("login.html", title = "Login", form = form)
