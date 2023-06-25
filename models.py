from app import db, bcrypt
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class BlogPost(db.Model):
    
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self): # specify how we want the object be represented when it's printed. 
        return '<title {}, desc {}'.format(self.title, self.description)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    posts = relationship("BlogPost", backref="author")

    def __init__(self, name, username, email, password, admin=False, is_confirmed=False, confirmed_on=None):
        self.name = name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8') # default salt value = 12 rounds
        self.is_authenticated = False
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self):
        return '<name {}'.format(self.username)
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return id to satisfy Flask-Login's requirements."""
        return str(self.id)

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class UserOAuth(db.Model):

    __tablename__ = "users_oauth"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String, unique=True, nullable=True)
    facebook_id = db.Column(db.String, unique=True, nullable=True)
    github_id = db.Column(db.String, unique=True, nullable=True)
    orcid_id = db.Column(db.String, unique=True, nullable=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.String, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    # posts = relationship("BlogPost", backref="author")

    def __init__(self, name, username, email, google_id=None, facebook_id=None, github_id=None, orcid_id=None, profile_pic=None, admin=False, is_confirmed=False, confirmed_on=None):
        self.name = name
        self.username = username
        self.email = email
        self.profile_pic = profile_pic
        self.google_id = google_id
        self.facebook_id = facebook_id
        self.github_id = github_id
        self.orcid_id = orcid_id
        self.is_authenticated = False
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self):
        return '<name {}'.format(self.username)
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return id to satisfy Flask-Login's requirements."""
        return str(self.id)

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



