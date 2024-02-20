from flask_wtf import FlaskForm                                         #Flask Add-On for Forms to Login/Register/Validate Accounts
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, HiddenField                          #Class to define Usernames & Passwords
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange     #Validators/Checks to be accepted to form
from tradingsim.models import User
import yfinance as yf

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

class UpdateProfileForm(FlaskForm):      #Inherits from flask form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])   

    email = StringField('Email', validators=[DataRequired(), Email()])

    profilePic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Profile')

    #Check to See if Username Exists Already, ONLY if user changes data
    def validate_username(self, username):  
        if username.data != current_user.username:                          #As Long as User changes Data, then validate only                         
            user = User.query.filter_by(username=username.data).first()     #If query returns a value, it means username already exists in DB
            if user:
                raise ValidationError('This Username is Taken. Choose Another.')
        
    #Check to See if Username Exists Already, Pass in Email entered into form
    def validate_email(self, email):                              
        if email.data != current_user.email:                          #As Long as User changes Data, then validate only
            user = User.query.filter_by(email=email.data).first()     #If query returns a value, it means username already exists in DB
            if user:
                raise ValidationError('This Email is Taken. Choose Another.')
         
class UpdateStockDashboard(FlaskForm):
    tickerToUpdate = StringField('Stock', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_tickerToUpdate(self, tickerToUpdate):
        print("In is_valid_ticker")
        ticker = yf.Ticker(tickerToUpdate.data)
        try:
            info = ticker.info
            if not info or 'quoteType' not in info:
                print(f"Invalid ticker: {tickerToUpdate.data}")  # Debug print
                raise ValidationError("Invalid Stock Ticker!")
            print(f"Valid ticker: {tickerToUpdate.data}")  # Debug print
            return True
        except Exception:
            print(f"Exception for ticker: {tickerToUpdate.data}")  # Debug print
            raise ValidationError("Invalid Stock Ticker!")

class DepositForm(FlaskForm):
    depositAmount = FloatField('Deposit', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Deposit')

class WithdrawForm(FlaskForm):
    withdrawAmount = FloatField('Withdraw', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Withdraw')
    
class BuyForm(FlaskForm):
    ticker = HiddenField('Ticker')
    numShares = IntegerField('Number of Shares', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Buy')

class SellForm(FlaskForm):
    ticker = HiddenField('Ticker')
    numShares = IntegerField('Number of Shares', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Sell')