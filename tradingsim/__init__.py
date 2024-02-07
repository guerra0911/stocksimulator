from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)       #app = class of Flask
app.config['SECRET_KEY'] = '2134a260716814ec7c9d781f885ef9e1'   #Protect Against Cyber Attacks, etc. Will make environment variable later on
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)        #Have an SQL Alchemy Instance called db

from tradingsim import routes       #Avod Circular Import Loop