from flask_wtf import FlaskForm                                         #Flask Add-On for Forms to Login/Register/Validate Accounts
from wtforms import StringField, PasswordField, SubmitField, BooleanField                          #Class to define Usernames & Passwords
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError     #Validators/Checks to be accepted to form
from tradingsim.models import User

class RegistrationForm(FlaskForm):      #Inherits from flask form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])   

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    #Check to See if Username Exists Already, Pass in Username entered into form
    def validate_username(self, username):                              
        user = User.query.filter_by(username=username.data).first()     #If query returns a value, it means username already exists in DB
        if user:
            raise ValidationError('This Username is Taken. Choose Another.')
        
    #Check to See if Username Exists Already, Pass in Email entered into form
    def validate_email(self, email):                              
        user = User.query.filter_by(email=email.data).first()     #If query returns a value, it means username already exists in DB
        if user:
            raise ValidationError('This Email is Taken. Choose Another.')

class LoginForm(FlaskForm):      
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')      #Stay Logged in using Secure Cookies even if Browser Closes

    submit = SubmitField('Login')

