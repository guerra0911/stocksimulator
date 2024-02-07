from flask import render_template, url_for, flash, redirect
from tradingsim import app
from tradingsim.models import User, Transaction
from tradingsim.forms import RegistrationForm, LoginForm

profile = [
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
    return render_template('home.html', profile=profile)   

@app.route("/portfolio")                #page directory at /portfolio
def portfolio():
    return render_template('portfolio.html', title='Portfolio') 

@app.route("/register", methods=['GET', 'POST'])                #Accepts POST & GET Methods, or else 405 Error, Method Not Allowed
def register():
    form = RegistrationForm()                                               #Create an Instance of the Registration Form Created in forms.py
    if form.validate_on_submit():                                           #If form Validated when Submitted
        flash(f'Account Created for {form.username.data}!', 'success')      #Flash Message, using 'success' style from main.css
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)    #Give access to form in html by passing form

@app.route("/login", methods=['GET', 'POST'])               
def login():
    form = LoginForm()                                                      #Create an Instance of the Login Form Created in forms.py
    if form.validate_on_submit():
        #IF USERNAME AND PASS MATCH IN DATABASE
        #flash('Successfully Logged In!', 'success')
        #return redirect(url_for('home'))
        pass
    else:
        #flash('Login Unsuccessful. Please Check Username & Password', 'danger')
        pass
    return render_template('login.html', title='Login', form=form) 