import secrets  #           Encode file names
import os                   #Keep file extensions (jpg, png)
from PIL import Image       #Image Resizing
from flask import render_template, url_for, flash, redirect, request
from flask_socketio import emit
from tradingsim import app, db, bcrypt, socketio
from tradingsim.models import User, Transaction
from tradingsim.forms import RegistrationForm, LoginForm, UpdateProfileForm, UpdateStockDashboard
from flask_login import login_user, logout_user, current_user, login_required
import yfinance as yf

@app.route("/", methods=['GET', 'POST'])                     #Initial Directory
@login_required
def home():
    form = UpdateStockDashboard()
    if form.validate_on_submit(): 
        current_user.dt1 = form.dt1.data
        current_user.dt2 = form.dt2.data
        current_user.dt3 = form.dt3.data
        current_user.dt4 = form.dt4.data
        db.session.commit()
    elif request.method == 'GET':
        form.dt1.data = current_user.dt1
        form.dt2.data = current_user.dt2
        form.dt3.data = current_user.dt3
        form.dt4.data = current_user.dt4

    dt1 = current_user.dt1
    dt2 = current_user.dt2
    dt3 = current_user.dt3
    dt4 = current_user.dt4

    return render_template('home.html', form=form, dt1=dt1, dt2=dt2, dt3=dt3, dt4=dt4)   

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@app.route("/portfolio")                #page directory at /portfolio
@login_required
def portfolio():
    return render_template('portfolio.html', title='Portfolio') 

@socketio.on('get_stock_data')
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="max", interval="1d")  # fetches daily data
    emit('new_stock_data', {'ohlc': data['Close'].tolist(), 'time': data.index.strftime('%Y-%m-%d').tolist()})


@app.route("/register", methods=['GET', 'POST'])                #Accepts POST & GET Methods, or else 405 Error, Method Not Allowed
def register():
    #If User is Logged In, Redirect Register Page to Home, Don't Let them Register Again
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    #Registration Form
    form = RegistrationForm()                                               #Create an Instance of the Registration Form Created in forms.py
    if form.validate_on_submit():                                           #If form Validated when Submitted
        
        #Create Account in Database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')             #Create Hashed Pass
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)       #Create New User
        db.session.add(user)                                                                            #Commit & Add to DB
        db.session.commit()
        flash(f'Your Account has been Created! Please Log In.', 'success')      #Flash Message, using 'success' style from main.css
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)    #Give access to form in html by passing form

@app.route("/login", methods=['GET', 'POST'])               
def login():
    #If User is Logged In, Redirect Login Page to Home, Don't Let them Login Again
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #Login Form
    form = LoginForm()                                                      #Create an Instance of the Login Form Created in forms.py
    
    #Validate Login
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()                          #Check if Email User enters matches an email in the database, return all User data for that User found
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #Check if Passwords Entered, matches password just retrieved from User object from email query
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')                                    #Check if User was Redirected to Login Page after trying to access a page only accessible by a logged in user
            return redirect(next_page) if next_page else redirect(url_for('home'))  #Redirect them back to their initial request if they got redirected, otherwise just go home
        else:
            flash('Login Unsuccessful. Please Check Email & Password', 'danger')
    return render_template('login.html', title='Login', form=form) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):                                 #Save picture file that user uploads
    random_hex = secrets.token_hex(8)                           #Randomize name of user inputted file to not interfere with stored pics in our file system
    _, picExt = os.path.splitext(form_picture.filename)        #Keep jpg or png extension and save it. form_picture is passed in. Data that user submitted
    picture_fn = random_hex + picExt                            #Concatenate random file name plus the extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)   #Join the picture filename (picture_fn) into the correct folder
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)                             #Save the image in that correct path
    return picture_fn


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():                       #If update form is validated and passes checks
        #If the User Changed their Picture
        if form.profilePic.data:                                #If there is a picture change request
            picture_file = save_picture(form.profilePic.data)   #Save the new photo the input into the form
            current_user.image_file = picture_file              #Set the current users image_file attribute to the newly saved pic
        current_user.username = form.username.data      #Change Username    
        current_user.email = form.email.data            #Change Email
        db.session.commit()                             #Change Database
        flash('Your Account has Been Updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username      #Fill form with Current Username before they change it
        form.email.data = current_user.email            #Fill form with Current Email before they change it
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html',title='Profile', image_file=image_file, form=form)