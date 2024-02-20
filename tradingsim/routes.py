import secrets  #           Encode file names
import os                   #Keep file extensions (jpg, png)
from PIL import Image       #Image Resizing
from flask import render_template, url_for, flash, redirect, request
from flask_socketio import emit
from tradingsim import app, db, bcrypt, socketio
from tradingsim.models import User, Transaction
from tradingsim.forms import RegistrationForm, LoginForm, UpdateProfileForm, UpdateStockDashboard, DepositForm, WithdrawForm, BuyForm
from flask_login import login_user, logout_user, current_user, login_required
import yfinance as yf
import pandas as pd
from datetime import datetime

@app.route("/", methods=['GET', 'POST'])                     #Initial Directory
@login_required
def home():
    #Pass into HTML
    dt1 = current_user.dt1
    dt2 = current_user.dt2
    dt3 = current_user.dt3
    dt4 = current_user.dt4

    userTransactions = db.session.query(Transaction.type, Transaction.ticker, Transaction.numShares, Transaction.price, Transaction.date_posted).\
        filter(Transaction.userid == current_user.id).all()
    
    # Format the date and time for each row
    formatted_userTransactions = []
    for transaction in userTransactions:
        formatted_userTransaction = {
            'type': transaction.type,
            'ticker': transaction.ticker,
            'numShares': transaction.numShares,
            'price': transaction.price,
            'date_posted': transaction.date_posted.strftime('%B %d, %Y, %H:%M:%S')  # Include time
        }
        formatted_userTransactions.append(formatted_userTransaction)

    # Sort transactions by date in descending order
    formatted_userTransactions.sort(key=lambda x: x['date_posted'], reverse=True)

    # Create a dictionary to store the data for each stock
    user_stocks = {}

    # Process each transaction
    for transaction in formatted_userTransactions:
        ticker = transaction['ticker']
        numShares = transaction['numShares']
        price = transaction['price']

        # If this is the first transaction for this stock, initialize the data
        if ticker not in user_stocks:
            user_stocks[ticker] = {'numShares': 0, 'totalValue': 0}

        # Update the number of shares and total value
        if transaction['type'] == 'Buy':
            user_stocks[ticker]['numShares'] += numShares
            user_stocks[ticker]['totalValue'] += numShares * price
        elif transaction['type'] == 'Sell':
            user_stocks[ticker]['numShares'] -= numShares
            user_stocks[ticker]['totalValue'] -= numShares * price

    # Calculate the current value for each stock
    for ticker in user_stocks:
        stock = yf.Ticker(ticker)
        stock_history = stock.history()
        current_price = round(stock_history['Close'].iloc[-1], 2)
        user_stocks[ticker]['currentValue'] = user_stocks[ticker]['numShares'] * current_price

    # Calculate the total current value of all stocks
    total_current_value = sum(stock['currentValue'] for stock in user_stocks.values()) + current_user.balance

    # Calculate the total value from stocks
    total_stock_value = sum(stock['currentValue'] for stock in user_stocks.values())

    # Calculate the percent increase
    if total_stock_value != 0:
        percent_increase = ((total_current_value - total_stock_value) / total_stock_value) * 100
    else:
        percent_increase = 0

    # Create BuyStockForm instances for each stock
    update_forms = {dt: UpdateStockDashboard(prefix=dt) for dt in ['dt1', 'dt2', 'dt3', 'dt4']}
    print(update_forms.keys())

    #Check if any of the buy forms have been submitted
    for dt, update_form in update_forms.items():
        if update_form.validate_on_submit() and update_form.submit.data:
            if dt == 'dt1':
                current_user.dt1 = update_form.tickerToUpdate.data
                dt1 = update_form.tickerToUpdate.data
                db.session.commit()
                flash(f'Added {dt1} to your Dashboard', 'success')
                return redirect(url_for('home'))
            elif dt == 'dt2':
                current_user.dt2 = update_form.tickerToUpdate.data
                dt2 = update_form.tickerToUpdate.data
                db.session.commit()
                flash(f'Added {dt2} to your Dashboard', 'success')
                return redirect(url_for('home'))
            elif dt == 'dt3':
                current_user.dt3 = update_form.tickerToUpdate.data
                dt3 = update_form.tickerToUpdate.data
                db.session.commit()
                flash(f'Added {dt3} to your Dashboard', 'success')
                return redirect(url_for('home'))
            elif dt == 'dt4':
                current_user.dt4 = update_form.tickerToUpdate.data
                dt4 = update_form.tickerToUpdate.data
                db.session.commit()
                flash(f'Added {dt4} to your Dashboard', 'success')
                return redirect(url_for('home'))

    #Get Live Price
    dt1Ticker = yf.Ticker(dt1)
    dt2Ticker = yf.Ticker(dt2)
    dt3Ticker = yf.Ticker(dt3)
    dt4Ticker = yf.Ticker(dt4)

    data1 = dt1Ticker.history()
    data2 = dt2Ticker.history()
    data3 = dt3Ticker.history()
    data4 = dt4Ticker.history()

    dt1LastPrice = round(data1['Close'].iloc[-1], 2)
    dt1SecondLastPrice = round(data1['Close'].iloc[-2], 2)
    if dt1LastPrice >= dt1SecondLastPrice:
        dt1Change = 1
    else:
        dt1Change = 0

    dt2LastPrice = round(data2['Close'].iloc[-1], 2)
    dt2SecondLastPrice = round(data2['Close'].iloc[-2], 2)
    if dt2LastPrice >= dt2SecondLastPrice:
        dt2Change = 1
    else:
        dt2Change = 0

    dt3LastPrice = round(data3['Close'].iloc[-1], 2)
    dt3SecondLastPrice = round(data3['Close'].iloc[-2], 2)
    if dt3LastPrice >= dt3SecondLastPrice:
        dt3Change = 1
    else:
        dt3Change = 0

    dt4LastPrice = round(data4['Close'].iloc[-1], 2)
    dt4SecondLastPrice = round(data4['Close'].iloc[-2], 2)
    if dt4LastPrice > dt4SecondLastPrice:
        dt4Change = 1
    else:
        dt4Change = 0

    # Create BuyStockForm instances for each stock
    buy_forms = {dt: BuyForm(prefix=dt, ticker=getattr(current_user, dt)) for dt in ['dt1', 'dt2', 'dt3', 'dt4']}
    print(buy_forms.keys())

    #Check if any of the buy forms have been submitted
    for dt, buy_form in buy_forms.items():
        if buy_form.validate_on_submit() and buy_form.submit.data:
            if dt == 'dt1':
                cost = dt1LastPrice * buy_form.numShares.data
                if cost < current_user.balance:
                    current_user.balance -= cost
                    transaction = Transaction(client=current_user, type="Buy", ticker=dt1, numShares=buy_form.numShares.data, price=dt1LastPrice,date_posted=datetime.utcnow())
                    db.session.add(transaction)
                    db.session.commit()
                    flash(f'Successful Transaction, {dt1} was purchased', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Insufficient Funds, you only have ${format(current_user.balance, ".2f")}', 'danger')
                    return redirect(url_for('home'))
            elif dt == 'dt2':
                cost = dt2LastPrice * buy_form.numShares.data
                if cost < current_user.balance:
                    current_user.balance -= cost
                    transaction = Transaction(client=current_user, type="Buy", ticker=dt2, numShares=buy_form.numShares.data, price=dt2LastPrice,date_posted=datetime.utcnow())
                    db.session.add(transaction)
                    db.session.commit()
                    flash(f'Successful Transaction, {dt2} was purchased', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Insufficient Funds, you only have ${format(current_user.balance, ".2f")}', 'danger')
                    return redirect(url_for('home'))
            elif dt == 'dt3':
                cost = dt3LastPrice * buy_form.numShares.data
                if cost < current_user.balance:
                    current_user.balance -= cost
                    transaction = Transaction(client=current_user, type="Buy", ticker=dt3, numShares=buy_form.numShares.data, price=dt3LastPrice,date_posted=datetime.utcnow())
                    db.session.add(transaction)
                    db.session.commit()
                    flash(f'Successful Transaction, {dt3} was purchased', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Insufficient Funds, you only have ${format(current_user.balance, ".2f")}', 'danger')
                    return redirect(url_for('home'))
            elif dt == 'dt4':
                cost = dt4LastPrice * buy_form.numShares.data
                if cost < current_user.balance:
                    current_user.balance -= cost
                    transaction = Transaction(client=current_user, type="Buy", ticker=dt4, numShares=buy_form.numShares.data, price=dt4LastPrice,date_posted=datetime.utcnow())
                    db.session.add(transaction)
                    db.session.commit()
                    flash(f'Successful Transaction, {dt4} was purchased', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Insufficient Funds, you only have ${format(current_user.balance, ".2f")}', 'danger')
                    return redirect(url_for('home'))
                
    return render_template('home.html', update_forms=update_forms, buy_forms=buy_forms, dt1=dt1, dt2=dt2, dt3=dt3, dt4=dt4, 
                           dt1LastPrice=dt1LastPrice, dt2LastPrice=dt2LastPrice, dt3LastPrice=dt3LastPrice, dt4LastPrice=dt4LastPrice, 
                           dt1Change=dt1Change, dt2Change=dt2Change, dt3Change=dt3Change, dt4Change=dt4Change, 
                           userTransactions=formatted_userTransactions, user_stocks=user_stocks, 
                           total_current_value=total_current_value, total_stock_value=total_stock_value, percent_increase=percent_increase)

    
@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@app.route("/portfolio")                #page directory at /portfolio
@login_required
def portfolio():
    return render_template('portfolio.html', title='Portfolio') 

@socketio.on('get_stock_data')
def get_stock_data(dt1, dt2, dt3, dt4):
    tickers = [dt1, dt2, dt3, dt4]
    data_list = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.history(period="max", interval="1d")  # fetches daily data
        data_list.append({'ohlc': data['Close'].tolist(), 'time': data.index.strftime('%Y-%m-%d').tolist()})
    emit('new_stock_data', data_list)

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
    depositForm = DepositForm()
    withdrawForm = WithdrawForm()
    if request.method == 'POST':
        if 'Update Profile' in request.form:
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
        elif 'Deposit' in request.form:
            if depositForm.validate_on_submit():
                current_user.balance = current_user.balance + depositForm.depositAmount.data
                db.session.commit()
                flash(f"Successfully Deposited ${depositForm.depositAmount.data}", 'success')

                depositForm.depositAmount.data = None
        elif 'Withdraw' in request.form:
            if withdrawForm.validate_on_submit():
                if withdrawForm.withdrawAmount.data > current_user.balance:
                    flash(f"Insufficient Funds!",'danger')
                else:
                    current_user.balance -= withdrawForm.withdrawAmount.data
                    db.session.commit()
                    withdrawForm.withdrawAmount.data = None
                    flash(f"Successfully Withdrew ${withdrawForm.withdrawAmount.data}", 'success')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html',title='Profile', image_file=image_file, form=form, depositForm=depositForm, withdrawForm=withdrawForm)

@app.route("/stock/<string:ticker_name>")       #Get the post.id attribute when the post is clicked, send it here and route the user to a new page particular to the post based on its id. This is variable passed in, is dynamic
def stock(ticker_name):                      #Needs post_id when passed in, in home.html. So when redirecting users here, you need to also include the passed in parameter post_id                    
    # Create an object from the ticker_name
    stock = yf.Ticker(ticker_name)
    # Get the stock history
    stock_history = stock.history()
    # Get the last price
    stock_lastPrice = round(stock_history['Close'].iloc[-1], 2)
    # Get the income statement
    stock_income = stock.financials
    # Get the balance sheet
    stock_balance = stock.balance_sheet
    # Get the cash flow statement
    stock_cashflow = stock.cashflow
    # Get the major holders
    stock_major_holders = stock.major_holders
    # Get the mutual fund holders
    stock_mutual_fund_holders = stock.mutualfund_holders
    # Get the stock name
    stock_name = stock.info['longName']
    # Pass the data to the stock.html template
    return render_template('stock.html', ind_stock=ticker_name, stock_lastPrice=stock_lastPrice, stock_income=stock_income, stock_balance=stock_balance, stock_cashflow=stock_cashflow, stock_major_holders=stock_major_holders, stock_mutual_fund_holders=stock_mutual_fund_holders, stock_name=stock_name)

@socketio.on('get_ind_stock_data')
def get_ind_stock_data(ind_stock):
    # No need to use a list for one stock
    stock = yf.Ticker(ind_stock)
    data = stock.history(period="max", interval="1d")  # fetches daily data
    # No need to use a list for one data
    data_dict = {'ohlc': data['Close'].tolist(), 'time': data.index.strftime('%Y-%m-%d').tolist()}
    emit('new_ind_stock_data', data_dict)