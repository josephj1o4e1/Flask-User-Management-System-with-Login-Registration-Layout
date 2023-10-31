# flask-wtf forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class LoginForm(FlaskForm):
    username_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    # <input type="text" id="name" name="name" required>
    name = StringField(
        'Full Name',
        validators=[DataRequired()]
    )
    # <input type="text" id="username" name="username" required minlength="5" maxlength="25">
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=5, max=25)]
    )
    # <input type="email" id="email" name="email" required minlength="6" maxlength="40" data-error=None>
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )

    # <input type="password" id="password" name="password" required
    #    pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[ !&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\]^_`{|}~])[A-Za-z\d !&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\]^_`{|}~]{8,30}$"
    #    title="Password must contain at least 8 characters with:&#10;1. at least 1 special character (between the double quotes): &quot; !&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\]^_`{|}~&quot;&#10;2. letters (1 lowercase and 1 uppercase)&#10;3. at least 1 number">
    password = PasswordField(
        'Password',
        validators=[DataRequired(), 
                    Length(min=8, max=30),
                    Regexp(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[ !"#$%&\'()*+,-.\/:;<=>?@[\]^_`{|}~])[A-Za-z\d !"#$%&\'()*+,-.\/:;<=>?@[\]^_`{|}~]', 
                           message='''Password must contain at least 8 characters with:<br/>
                           1. at least 1 special character !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~<br/>
                           2. at least 1 lowercase and 1 uppercase letter <br/>
                           3. at least 1 number''')
                    ]
    )

    # <input type="password" id="confirm" name="confirm" required data-equal-to="#password" data-error-message="Passwords must match.">
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match.')
            ]
    )
    
    # <input type="checkbox" id="terms" name="terms" required>
    terms = BooleanField('I have read and agree to the terms', validators=[DataRequired()])
    
    # <button type="submit" id="submit" name="submit">Register</button>
    submit = SubmitField('Register')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')