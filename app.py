import os, datetime, json
from flask import Flask, render_template, request, redirect, url_for, flash, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS')) # ...(dev mode right now, not prod mode)

bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
login_manager.login_message = ""

from models import * # import db schema
from forms import LoginForm, RegisterForm
from tokens import generate_confirmation_token, confirm_token
from emails import send_email
from utils import url_has_allowed_host_and_scheme

# OAuth 2 client setup
client = WebApplicationClient(app.config['OAUTH_CREDENTIALS']['google']['id'])
def get_google_provider_cfg(): # naive function to retrieve google oauth's provider config. Need to retrieve the base URI from the Discovery document using the `authorization_endpoint` metadata value.
    try:
        response = requests.get(app.config['OAUTH_CREDENTIALS']['google']['disc_url'])
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print(f"Error retrieving Google provider config: {e}")
        return None


# Gets the user information from userid, and store the retrieved data in the session cookie. 
# load_user is a required callbackfunction to be defined for the user_loader decorator. 
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first() or UserOAuth.query.filter(UserOAuth.id == int(user_id)).first()
    # return User.get_id(user_id)

# set route. use a decorator to link a url to a function. (see flasknotes)
# decorator @app.route('/'): before triggering home(), we need to detect if url '/' is requested by client, and later do the login confirmation before executing home().  
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
    if request.method == 'POST':
        if form.validate_on_submit():
            foundUser = User.query.filter_by(name=form.username.data).first()
            if foundUser!=None and bcrypt.check_password_hash(foundUser.password, form.password.data): 
                # session['logged_in']=True
                login_user(foundUser)
                flash('you were just logged in')

                next = request.args.get('next')
                # # url_has_allowed_host_and_scheme should check if the url is safe
                # # for redirects, meaning it matches the request host.
                # # See Django's url_has_allowed_host_and_scheme for an example.
                # if not url_has_allowed_host_and_scheme(next, request.host):
                #     return abort(400, message="redirect url is not safe.")
                
                return redirect(next or url_for('home'))
                # return redirect(url_for('home'))
            else: 
                error = 'Invalid credentials, please try again. '

    return render_template("login.html", form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                name=form.username.data,
                email=form.email.data,
                password=form.password.data,
                is_confirmed=False
            )
            db.session.add(user)
            db.session.commit()

            # token = generate_confirmation_token(user.email)
            # confirm_url = url_for('confirm_email', token=token, _external=True) # _external=true adds the full absolute URL that includes the hostname and port
            # html = render_template('activate.html', confirm_url=confirm_url)
            # subject = "Please confirm your email"
            # send_email(user.email, subject, html)

            login_user(user)
            flash('you were just logged in')

            # flash('A confirmation email has been sent via email.', 'success')
            return redirect(url_for('home'))
    
    return render_template('register.html', form=form)


@app.route('/google_login')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/authorized",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route('/google_login/authorized')
def authorized():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['OAUTH_CREDENTIALS']['google']['id'], app.config['OAUTH_CREDENTIALS']['google']['secret']),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]
        users_name = userinfo_response.json()["name"]

        foundUser = UserOAuth.query.filter_by(name=users_name).first()
        print(f'!!!! users_name = {users_name}')
        print(f'!! foundUser = {foundUser}')
        if foundUser==None: 
            foundUser = UserOAuth(
                google_id=unique_id, 
                name=users_name,
                email=users_email,
                profile_pic=picture
            )        
            db.session.add(foundUser)
            db.session.commit()
        login_user(foundUser)
        flash('you were just logged in')

        next = request.args.get('next')
        # # url_has_allowed_host_and_scheme should check if the url is safe
        # # for redirects, meaning it matches the request host.
        # # See Django's url_has_allowed_host_and_scheme for an example.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400, message="redirect url is not safe.")
        
        return redirect(next or url_for('home'))
        # return redirect(url_for('home'))
        
    else:
        return "User email not available or not verified by Google.", 400


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    # session.pop('logged_in', None)
    logout_user()
    flash('you were just logged out')
    return redirect(url_for('welcome'))

if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc") # `debug=True` gives us a fancier flask debugger in the browser
