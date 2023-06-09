# flask-wtf forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match.'),
            Regexp(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[ !"#$%&\'()*+,-.\/:;<=>?@[\]^_`{|}~])[A-Za-z\d !"#$%&\'()*+,-.\/:;<=>?@[\]^_`{|}~]',
                   message='Password must contain at least 6 characters with:\n1. at least 1 special character(between the double quotes): " !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"\n2. letters(1 lowercase and 1 uppercase)\n3. at least 1 number')
        ]
    )
    submit = SubmitField('Register')