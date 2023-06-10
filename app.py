from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user
# from functools import wraps
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
login_manager.login_message = ""

import os
app.config.from_object(os.getenv('APP_SETTINGS')) # ...(dev mode right now, not prod mode)

# create the sqlalchemy object
db = SQLAlchemy(app)

# import db schema
from models import *
from forms import LoginForm, RegisterForm

# Gets the user information from userid, and store the retrieved data in the session cookie. 
# load_user is a required callbackfunction to be defined for the user_loader decorator. 
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
    # return User.get_id(user_id)

# set route. use a decorator to link a url to a function. (see flasknotes)
# decorator @app.route('/'): before triggering home(), we need to detect if url '/' is requested by client before executing home().  
@app.route('/')
@login_required
def home():
    posts = BlogPost.query.all()
    return render_template("index.html", posts=posts) # posts=posts --> past our `posts` variable to index.html template

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        foundUser = User.query.filter_by(name=form.username.data).first()
        if foundUser!=None and bcrypt.check_password_hash(foundUser.password, form.password.data): 
            # session['logged_in']=True
            login_user(foundUser)
            flash('you were just logged in')
            return redirect(url_for('home'))
        else: 
            error = 'Invalid credentials, please try again. '

    return render_template("login.html", form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data,
            is_confirmed=False
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # session.pop('logged_in', None)
    logout_user()
    flash('you were just logged out')
    return redirect(url_for('welcome'))

if __name__ == "__main__":
    app.run(debug=True) # `debug=True` gives us a fancier flask debugger in the browser
