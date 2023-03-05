import os
from Solutrip_app import app,db
from flask import render_template, url_for, flash, redirect, request, Flask
from Solutrip_app.models import User, UserInfo, Company
from Solutrip_app.forms import RegistrationForm, LoginForm, UpdateForm,RequestPassForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect (url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Hashing
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User.query.filter_by(email=form.email.data).first()
        # Create a new user with the provided details
        user = User(
            username=form.username.data,
            email=form.email.data,
            password= hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods= ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('home'))
    form = LoginForm()
    if form.validate_on_submit(): # Import Flash and send a confirmation message.
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash (user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            #To redirect to next page.
            next_page = request.args.get('next')
            flash(f"Login successful { form.email.data }!", "success")
            return redirect(next_page) if next_page else redirect(url_for('about'))
        else:    
            flash(f"Login unsuccessful, please check username and password.", "danger")
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_cv(form_cv):
    _,f_ext = os.path.splitext(form_cv.filename)
    cv_fn = current_user.username + f_ext
    cv_path = os.path.join (app.root_path,'static/cvs', cv_fn)
    form_cv.save(cv_path)
    return cv_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        userinfo = UserInfo.query.filter_by(user_id=current_user.id).first()
        if not userinfo:
            userinfo = UserInfo(user_id=current_user.id)
            db.session.add(userinfo)
        userinfo.name = form.name.data
        userinfo.surname = form.surname.data
        userinfo.location = form.location.data
        userinfo.phone = form.phone.data
        userinfo.linkedin = form.linkedin.data
        userinfo.experience = form.experience.data
        userinfo.education = form.education.data
        userinfo.crypto_account = form.crypto_account.data

        if form.cv.data:
            cv_file = save_cv(form.cv.data)
            current_user.cv = cv_file

        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        userinfo = UserInfo.query.filter_by(user_id=current_user.id).first()
        if userinfo:
            form.name.data = userinfo.name
            form.surname.data = userinfo.surname
            form.location.data = userinfo.location
            form.phone.data = userinfo.phone
            form.linkedin.data = userinfo.linkedin
            form.experience.data = userinfo.experience
            form.education.data = userinfo.education
            form.crypto_account.data = userinfo.crypto_account
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route("/requestpassword", methods=['GET', 'POST'])
def request_pass():
    form= RequestPassForm()
    if form.validate_on_submit():
        None