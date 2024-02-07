from flask_wtf import FlaskForm                                         #Flask Add-On for Forms to Login/Register/Validate Accounts
from wtforms import StringField, PasswordField, SubmitField, BooleanField                          #Class to define Usernames & Passwords
from wtforms.validators import DataRequired, Length, Email, EqualTo     #Validators/Checks to be accepted to form

class RegistrationForm(FlaskForm):      #Inherits from flask form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])   

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):      
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')      #Stay Logged in using Secure Cookies even if Browser Closes

    submit = SubmitField('Login')

