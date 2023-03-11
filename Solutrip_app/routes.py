import os
from Solutrip_app import app,db
from flask import render_template, url_for, flash, redirect, request
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
    JOBS = [{ "Id": 1,
              "Title": "Data Analyst JR",
              "Location": "Europe",
              "Salary": "$900 USD" 
            },
            { "Id": 2,
              "Title": "Full Stack Developer",
              "Location": "Europe",
              "Salary": "$2,800 USD" 
            },
            { "Id": 3,
              "Title": "Cloud Architect",
              "Location": "USA",
              "Salary": "$2,000 USD" 
            }
    ]
    return render_template("candidates.html", jobs = JOBS)

@app.route("/employers")
def employers():
    return render_template("employers.html", title = "Employers")

@app.route("/blog")
def blog():
    posts = [ {
        "author": "joe.solutrip@gmail.com",
        "title": "Why work remote in 2023?",
        "content": """Remote work is a great option in 2023 for a variety of reasons,
         including flexibility, cost savings, a larger talent pool, 
         and environmental benefits. As technology continues to advance and remote work becomes 
         more common, we can expect to see even more companies and employees embracing this way 
         of working. Get the maximum benefits from this new way of working! """,
        "date_posted": "1 of March 2023"  

        },
        { 
        "author": "joe.solutrip@gmail.com",
        "title": "Tips to pass your English interview",
        "content": """Speak clearly and confidently: Speak slowly and clearly so that the interviewer can
        understand you. Take your time when answering questions and try to speak confidently. If you're
        not sure about something, it's okay to take a moment to think before you answer. Be prepared to talk about 
        yourself: In many interviews, the interviewer will ask you to talk about yourself. Prepare a short introduction that highlights your skills, experience, and why you're interested in the job.""",
        "date_posted": "10 of March 2023"  
        },
        { 
        "author": "eze.solutrip@gmail.com",
        "title": "How to make a Github Portfolio",
        "content": """Creating a GitHub portfolio is a great way to showcase your programming skills and projects to potential employers and collaborators.
        GitHub allows you to customize your repository's appearance by adding a profile picture, a cover photo, and a description. You can also add badges and labels to your projects to make them more appealing""",
        "date_posted": "7 of March 2023"  
        }
    ]
    return render_template("blog.html", posts = posts, title = "Blog")

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
        userinfo.profession = form.profession.data
        userinfo.education = form.education.data
        userinfo.github_account = form.github_account.data

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
            form.profession.data = userinfo.profession
            form.education.data = userinfo.education
            form.github_account.data = userinfo.github_account
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route("/requestpassword", methods=['GET', 'POST'])
def request_pass():
    form= RequestPassForm()
    if form.validate_on_submit():
        None


# #ADMIN SESSION

# user = User.query.filter_by(email='ezelevy87@gmail.com').first()
# user.role = 'admin'

# def is_admin(user):
#     return user.role == 'admin'
    
# @app.route("/admin")
# @login_required
# def admin():
#     if not is_admin(current_user):
#         flash("Sorry you must be Admin!")
#         return redirect(url_for('home'))
#     return render_template("admin.html")

