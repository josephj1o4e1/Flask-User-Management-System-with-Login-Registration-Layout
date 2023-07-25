import os, datetime, json
from flask import Flask, render_template, request, redirect, url_for, flash, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from functools import wraps
from dotenv import load_dotenv
import secrets
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
from forms import LoginForm, RegisterForm, DeleteAccountForm
from tokens import generate_confirmation_token, confirm_token
from emails import send_email
from utils import url_has_allowed_host_and_scheme

# OAuth 2 client setup
google_client = WebApplicationClient(app.config['OAUTH_CREDENTIALS']['google']['id'])
def get_google_provider_cfg(): # naive function to retrieve google oauth's provider config. Need to retrieve the base URI from the Discovery document using the `authorization_endpoint` metadata value.
    try:
        response = requests.get(app.config['OAUTH_CREDENTIALS']['google']['config_url'])
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print(f"Error retrieving Google provider config: {e}")
        return None

github_client = WebApplicationClient(app.config['OAUTH_CREDENTIALS']['github']['id'])
def get_github_provider_cfg(): # naive function to retrieve google oauth's provider config. Need to retrieve the base URI from the Discovery document using the `authorization_endpoint` metadata value.
    try:
        response = requests.get(app.config['OAUTH_CREDENTIALS']['github']['config_url'])
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print(f"Error retrieving GitHub provider config: {e}")
        return None

orcid_client = WebApplicationClient(app.config['OAUTH_CREDENTIALS']['orcid']['id'])
def get_orcid_provider_cfg(): # naive function to retrieve google oauth's provider config. Need to retrieve the base URI from the Discovery document using the `authorization_endpoint` metadata value.
    try:
        response = requests.get(app.config['OAUTH_CREDENTIALS']['orcid']['config_url'])
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print(f"Error retrieving ORCID provider config: {e}")
        return None

facebook_client = WebApplicationClient(app.config['OAUTH_CREDENTIALS']['facebook']['id'])
def get_facebook_provider_cfg(): # naive function to retrieve google oauth's provider config. Need to retrieve the base URI from the Discovery document using the `authorization_endpoint` metadata value.
    try:
        response = requests.get(app.config['OAUTH_CREDENTIALS']['facebook']['config_url'])
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
    return User.query.filter(User.id == int(user_id)).first()
    # return User.query.filter(User.id == int(user_id)).first() or UserOAuth.query.filter(UserOAuth.id == int(user_id)).first()
    # return User.get_id(user_id)

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

# set route. use a decorator to link a url to a function. (see flasknotes)
# decorator @app.route('/'): before triggering home(), we need to detect if url '/' is requested by client, and later do the login confirmation before executing home().  
@app.route('/')
@login_required
@check_confirmed
def home():
    posts = BlogPost.query.all()
    form = DeleteAccountForm()
    status = "Not Confirmed"
    if current_user.is_confirmed:
        status = "Confirmed"
    return render_template("index.html", form=form, posts=posts, status=status) # posts=posts --> past our `posts` variable to index.html template

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    rform = RegisterForm()
    activePill = request.form.get('active_pill')

    if current_user.is_authenticated:
        next = request.args.get('next')
        # # url_has_allowed_host_and_scheme should check if the url is safe
        # # for redirects, meaning it matches the request host.
        # # See Django's url_has_allowed_host_and_scheme for an example.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400, message="redirect url is not safe.")
        
        return redirect(next or url_for('home'))
    
    if request.method == 'POST':
        # LOGIN
        if activePill=="active_pill_login" and form.validate_on_submit():
            foundUser = User.query.filter((User.username==form.username_email.data) | (User.email==form.username_email.data)).first()
            if foundUser!=None and bcrypt.check_password_hash(foundUser.password, form.password.data): 
                # if not foundUser.is_confirmed: 
                #     flash('Please confirm your email first. ')
                #     return render_template("loginRegist.html", form=form, rform=rform, error=error)

                if request.form.get('loginCheck'):
                    remember = True
                else:
                    remember=False
                print(f'remember = {remember}')
                login_user(foundUser, remember=remember)
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
        # REGISTER
        elif activePill=="active_pill_register" and rform.validate_on_submit():
            foundEmailUser = User.query.filter_by(email=rform.email.data).first()
            # only requires email to be unique
            if foundEmailUser:
                flash('This Email has been registered before. Please log in. ', category='error')
                return redirect(url_for('login'))

            # foundUser = User.query.filter_by(name=rform.username.data).first()
            # if foundUser:
            #     flash('Username has been taken, please try another one. ')
            #     return redirect(url_for('login'))

            # # do later: suggest usernames
            
            user = User(
                name=rform.name.data,
                username=rform.username.data,
                email=rform.email.data,
                password=rform.password.data,
                is_confirmed=False
            )
            
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True) # _external=true adds the full absolute URL that includes the hostname and port
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            
            flash('A confirmation email has been sent via email. confirm before login. ', 'success')

            login_user(user)
            flash('you were just logged in')

            # next = request.args.get('next')
            # # url_has_allowed_host_and_scheme should check if the url is safe
            # # for redirects, meaning it matches the request host.
            # # See Django's url_has_allowed_host_and_scheme for an example.
            # if not url_has_allowed_host_and_scheme(next, request.host):
            #     return abort(400, message="redirect url is not safe.")
            
            return redirect(url_for('login'))
            # return redirect(next or url_for('home'))
            # return redirect(url_for('home'))

    # return render_template("login.html", form=form, error=error)
    # return render_template("loginRegist.html", form=form, rform=rform, error=error)
    return render_template("loginRegistNew.html", form=form, rform=rform, error=error)

@app.route('/google_login')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/authorized",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route('/google_login/authorized')
def google_authorized():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = google_client.prepare_token_request(
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
    google_client.parse_request_body_response(json.dumps(token_response.json()))
    
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)
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

        foundUser = User.query.filter_by(email=users_email).first()
        # print(f'!!!! users_name = {users_name}')
        # print(f'!! foundUser = {foundUser}')
        if foundUser==None: 
            foundUser = User(
                google_id=unique_id, 
                name=users_name,
                username=users_email,
                email=users_email,
                profile_pic=picture, 
                password=bcrypt.generate_password_hash(secrets.token_hex(16)).decode('utf-8')
            )        
            db.session.add(foundUser)
            db.session.commit()
            token = generate_confirmation_token(foundUser.email)
            confirm_url = url_for('confirm_email', token=token, _external=True) # _external=true adds the full absolute URL that includes the hostname and port
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(foundUser.email, subject, html)
            
            flash('A confirmation email has been sent via email. confirm before login. ', 'success')

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

@app.route('/github_login')
def github_login():
    return render_template("notfinished.html")

@app.route('/github_login/authorized')
def github_authorized():
    pass

@app.route('/orcid_login')
def orcid_login():
    return render_template("notfinished.html")

@app.route('/orcid_login/authorized')
def orcid_authorized():
    pass

@app.route('/facebook_login')
def facebook_login():
    return render_template("notfinished.html")

@app.route('/facebook_login/authorized')
def facebook_authorized():
    pass


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    next = request.args.get('next')
    if current_user.is_confirmed: # If the user already confirmed the link and refreshes the "/unconfirmed" page, it will go to (next or homepage). 
        return redirect(next or url_for('home'))
    
    return render_template('unconfirmed.html')

@app.route('/invalidlink')
@login_required
def invalidLink():
    next = request.args.get('next')
    if current_user.is_confirmed: # If the user already confirmed the link and refreshes the "/unconfirmed" page, it will go to (next or homepage). 
        return redirect(next or url_for('home'))
    
    return render_template('invalidLink.html')

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        # flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('invalidLink'))

    user = User.query.filter_by(email=email).first_or_404()
    print(f'email= {email}')
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user) # "db.session.add" is also used to track changes made to existing objects. 
        db.session.commit()
        logout_user()
        flash('You have confirmed your account. Please login your new account', 'success')
    # return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True) # _external=true adds the full absolute URL that includes the hostname and port
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('unconfirmed'))

@app.route('/logout')
@login_required
def logout():
    # session.pop('logged_in', None)
    logout_user()
    flash('you were just logged out')
    return redirect(url_for('welcome'))

@app.route('/delete_account', methods=['POST'])
@login_required  # Ensure only authenticated users can access this route
def delete_account():
    # Delete the user account from the database
    user = current_user  # using Flask-Login's current_user
    db.session.delete(user)
    db.session.commit()

    # Log the user out
    logout_user()
    flash('You have DELETED your account!', 'success')
    # Redirect the user to a confirmation page or any desired destination
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc") # `debug=True` gives us a fancier flask debugger in the browser
