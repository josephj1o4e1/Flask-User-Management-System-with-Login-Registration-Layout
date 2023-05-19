from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)

# Configuration values (secret_key is a builtin config value)
app.secret_key = "goofygroove" # DANGEROUS..but first we need secret_key for sessions to work properly
app.database = "sample.db"

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
# a decorator: when url '/' is requested by client, it triggers home()
@app.route('/')
@login_required
def home():
    # return "Hello World!"
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
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
    return render_template("login.html", error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('you were just logged out')
    return redirect(url_for('welcome'))


def connect_db(): # to establish a database
    return sqlite3.connect(app.database)



if __name__ == "__main__":
    app.run(debug=True) # `debug=True` gives us a fancier flask debugger in the browser
