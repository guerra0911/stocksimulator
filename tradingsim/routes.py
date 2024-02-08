from flask import render_template, url_for, flash, redirect, request
from tradingsim import app, db, bcrypt
from tradingsim.models import User, Transaction
from tradingsim.forms import RegistrationForm, LoginForm, UpdateProfileForm
from flask_login import login_user, logout_user, current_user, login_required

dummyData = [
    {'username': 'Nicholas Guerra',
     'balance': '0',
     'stocks': 'APPL, MSFT, DOW'
    },
    {'username': 'Kallista Bliss',
     'balance': '100',
     'stocks': 'TSLA, NASA'
    }
]

@app.route("/")                     #Initial Directory
def home():
    return render_template('home.html', dummyData=dummyData)   

@app.route("/portfolio")                #page directory at /portfolio
def portfolio():
    return render_template('portfolio.html', title='Portfolio') 

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

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():                       #If update form is validated and passes checks
        current_user.username = form.username.data      #Change Username
        current_user.email = form.email.data            #Change Email
        db.session.commit()                             #Change Database
        flash('Account Details Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username      #Fill form with Current Username before they change it
        form.email.data = current_user.email            #Fill form with Current Email before they change it
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html',title='Profile', image_file=image_file, form=form)