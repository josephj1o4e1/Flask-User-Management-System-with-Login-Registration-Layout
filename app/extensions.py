from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
import os
from dotenv import load_dotenv
load_dotenv()


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
google_client = WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID_ENV'))
github_client = WebApplicationClient(os.getenv('GITHUB_CLIENT_ID_ENV'))
orcid_client = WebApplicationClient(os.getenv('ORCID_CLIENT_ID_ENV'))
facebook_client = WebApplicationClient(os.getenv('FACEBOOK_CLIENT_ID_ENV'))