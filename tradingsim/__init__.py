from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)       #app = class of Flask
app.config['SECRET_KEY'] = '2134a260716814ec7c9d781f885ef9e1'   #Protect Against Cyber Attacks, etc. Will make environment variable later on
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ferrari11@localhost:5432/GUERRA'
db = SQLAlchemy(app)        #Have an SQL Alchemy Instance called db
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'       #Bootstrap Information Alert Style

from tradingsim import routes       #Avod Circular Import Loop