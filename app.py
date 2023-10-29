import os
from flask import Flask, render_template, redirect, url_for
from blueprints.LoginApp.loginapp import login_bp

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS')) # ...(dev mode right now, not prod mode)
app.register_blueprint(login_bp, url_prefix='/loginapp')

# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_mail import Mail
# from flask_login import LoginManager

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# mail = Mail(app)
# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == 'main':
    app.run(debug=True, ssl_context="adhoc")

