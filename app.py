from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

import os
app.config.from_object(os.getenv('APP_SETTINGS')) # ...(dev mode right now, not prod mode)

# create the sqlalchemy object
db = SQLAlchemy(app)

# import db schema
from models import *

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap 

# set route. use a decorator to link a url to a function. (see flasknotes)
# decorator @app.route('/'): before triggering home(), we need to detect if url '/' is requested by client before executing home().  
@app.route('/')
@login_required
def home():
    # # .....1st version
    # return "Hello World!" 

    # # .....2nd version
    # g.db = connect_db()
    # cur = g.db.execute('select * from posts')
    # posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    # g.db.close()

    # .....3rd version
    with app.app_context(): 
        posts = db.session.query(BlogPost).all()
    return render_template("index.html", posts=posts) # posts=posts --> past our `posts` variable to index.html template

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        if request.form['username']!='admin' or request.form['password']!='admin':
            error = 'Invalid credentials, please try again. '
        else :
            session['logged_in'] = True
            flash('you were just logged in')
            return redirect(url_for('home'))
    if 'logged_in' in session:
            return redirect(url_for('home'))
    return render_template("login.html", error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('you were just logged out')
    return redirect(url_for('welcome'))


# def connect_db(): # to establish a database
#     return sqlite3.connect(app.database)



if __name__ == "__main__":
    app.run(debug=True) # `debug=True` gives us a fancier flask debugger in the browser
