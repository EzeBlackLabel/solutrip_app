import os
from Solutrip_app import app,db
from flask import render_template, url_for, flash, redirect, request, abort
from Solutrip_app.models import User, UserInfo, Company, Post, Jobs
from Solutrip_app.forms import RegistrationForm, LoginForm, UpdateForm,RequestPassForm,PostForm,CompanyForm,JobForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

@app.route("/")
@app.route("/home")

def home():
    return render_template("index.html")
    
@app.route("/candidates")
def candidates(): 
    jobs = Jobs.query.all()
    return render_template("candidates.html", jobs = jobs, title="Jobs")

@app.route("/employers")
def employers():
    return render_template("employers.html", title = "Employers")

@app.route("/blog")
def blog():
    posts = Post.query.all()
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
            password= hashed_password,
        )
        admin_mails = ["ezelevy87@gmail.com", "joe.solutrip.gmail.com", "admin@solutrip.com"]
        if user.email in admin_mails:
            user.role = "admin"
        else:
            user.role = "default"
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


#ADMIN SESSION

def is_admin(user):
    return user.role == 'admin'
    
@app.route("/admin")
@login_required
def admin():
    if not is_admin(current_user):
        flash("Sorry, you must be an admin to access this page.", "danger")
        return redirect(url_for('home'))
    return render_template("admin.html", Title = 'Admin')

@app.route("/admin/post", methods=['GET', 'POST'])
@login_required
def admin_post():
    if not is_admin(current_user):
        flash("Sorry, you must be an admin to access this page.","danger")
        return redirect(url_for('home'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            tag = form.tag.data,
            content = form.content.data,
            author = current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for('admin'))
    return render_template("admin_post.html", title='Admin Post', form=form,
                            legend = "New Post")

@app.route("/admin/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title= post.title, post = post)

@app.route("/admin/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.tag = form.tag.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.tag.data = post.tag
        form.content.data = post.content
    return render_template("admin_post.html", title="Edit Post", form=form, post=post, legend= "Edit Post")



@app.route("/admin/company", methods=['GET', 'POST'])
@login_required
def admin_company():
    if not is_admin(current_user):
        flash("Sorry, you must be an admin to access this page.","danger")
        return redirect(url_for('home'))
    form = CompanyForm()
    companies = Company.query.all()
    if form.validate_on_submit():
        company = Company(
            companyname = form.companyname.data,
            email = form.email.data,
            location = form.location.data,
            industry = form.industry.data,
            phone = form.phone.data,
            website = form.website.data,
        )
        db.session.add(company)
        db.session.commit()
        flash("Company created successfully!", "success")
        return redirect(url_for('admin'))
    return render_template("admin_company.html", title='Admin Company', form=form, companies = companies)

@app.route("/admin/job", methods=['GET', 'POST'])
@login_required
def admin_job():
    if not is_admin(current_user):
        flash("Sorry, you must be an admin to access this page.","danger")
        return redirect(url_for('home'))
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            title = form.title.data,
            location = form.location.data,
            salary = form.salary.data,
            description = form.description.data,
            requirements = form.requirements.data,
            qualifications = form.qualifications.data,
            company_id = form.company_id.data,
        )
        db.session.add(job)
        db.session.commit()
        flash("Job created successfully!", "success")
        return redirect(url_for('admin'))
    return render_template("admin_job.html", title='Admin Job', form=form)