import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from pyblog import app, db, bcrypt
from pyblog.forms import RegistrationForm, LoginForm, UpdateAccForm
from pyblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Kenji Tagawa',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 5th, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'MEI 5th, 2021'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    # Random name
    random_hex = secrets.token_hex(8)
    
    # File extension
    _, f_ext = os.path.splitext(form_picture.filename)

    # File name
    picture_fn = random_hex + f_ext

    # Setting the file path
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)

    # Output size 125 by 125 px
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Saving file to path
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        # Update user information
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        # Update database
        db.session.commit()
    
        # Alerting the user
        flash(f'Your new username is set to "{current_user.username}" and your email is "{current_user.email}"!',
                'success')
        
        # Redirecting user back to his page for the update
        return redirect(url_for('account'))
    
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
