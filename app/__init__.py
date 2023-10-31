import os
from flask import Flask, render_template, redirect, url_for
from app.extensions import db, bcrypt, mail, login_manager, google_client
from dotenv import load_dotenv
load_dotenv()

# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_mail import Mail
# from flask_login import LoginManager

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# mail = Mail(app)
# login_manager = LoginManager()
# login_manager.init_app(app)



def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS')) # ...(dev mode right now, not prod mode)
    
    # Initialize Flask extensions here
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints here
    from app.LoginApp.loginapp import login_bp
    app.register_blueprint(login_bp, url_prefix='/loginapp')

    @app.route('/')
    def home():
        return render_template("index.html")

    return app


# if __name__ == 'main':
#     app.run(debug=True, ssl_context="adhoc")

