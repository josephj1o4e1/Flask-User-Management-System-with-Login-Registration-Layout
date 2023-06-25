# flask-wtf forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class LoginForm(FlaskForm):
    username_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField(
        'Full Name',
        validators=[DataRequired()]
    )
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=5, max=25)]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), 
                    Length(min=8, max=30),
                    Regexp(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[ !"#$%&\'()*+,-.\/:;<=>?@[\]^_`{|}~])[A-Za-z\d !"#$%&\'()*+,-.\/:;<=>?@[\]^_`{|}~]', 
                           message='''Password must contain at least 8 characters with:<br/>
                           1. at least 1 special character(between the double quotes): " !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"<br/>
                           2. letters(1 lowercase and 1 uppercase)<br/>
                           3. at least 1 number''')
                    ]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match.')
            ]
    )
    submit = SubmitField('Register')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')