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
    dt1 = StringField('Stock 1', validators=[DataRequired()])
    dt2 = StringField('Stock 2', validators=[DataRequired()])
    dt3 = StringField('Stock 3', validators=[DataRequired()])
    dt4 = StringField('Stock 4', validators=[DataRequired()])

    submit1 = SubmitField('Update')
    submit2 = SubmitField('Update')
    submit3 = SubmitField('Update')
    submit4 = SubmitField('Update')
        
    def is_valid_ticker(self, ticker_symbol):
        print("In is_valid_ticker")
        ticker = yf.Ticker(ticker_symbol)
        try:
            info = ticker.info
            if not info or 'quoteType' not in info:
                print(f"Invalid ticker: {ticker_symbol}")  # Debug print
                raise ValidationError("Invalid Stock Ticker!")
            print(f"Valid ticker: {ticker_symbol}")  # Debug print
            return True
        except Exception:
            print("Exception for ticker: {ticker_symbol}")  # Debug print
            raise ValidationError("Invalid Stock Ticker!")


    def validate_dt1(self, dt1):
        if dt1.data != current_user.dt1:     #Only call if it is changed
            print(f"Validating dt1: {dt1.data}")  # Debug print
            self.is_valid_ticker(dt1.data)

    def validate_dt2(self, dt2):
        if dt2.data != current_user.dt2:     #Only call if it is changed
            print(f"Validating dt2: {dt2.data}")  # Debug print
            self.is_valid_ticker(dt2.data)

    def validate_dt3(self, dt3):
        if dt3.data != current_user.dt3:     #Only call if it is changed
            print(f"Validating dt3: {dt3.data}")  # Debug print
            self.is_valid_ticker(dt3.data)

    def validate_dt4(self, dt4):
        if dt4.data != current_user.dt4:     #Only call if it is changed
            print(f"Validating dt1: {dt4.data}")  # Debug print
            self.is_valid_ticker(dt4.data)


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