from tradingsim import db, login_manager
import datetime
from flask_login import UserMixin

#From Flask Website
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default = 'defaultProfilePic.jpg')
    password = db.Column(db.String(60), nullable=False)
    transactions = db.relationship('Transaction', backref='author', lazy=True)

    def __repr__(self):      #How our object is printed, whenever we print it out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Transaction(db.Model):
    #Append -> Type, # SHARES, Stock, Price, Date to Portfolio Table for user
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(5), nullable=False)
    ticker = db.Column(db.String(5), nullable=False)
    numShares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.UTC)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):      #How our object is printed, whenever we print it out
        return f"Transaction('{self.type}', '{self.ticker}', '{self.numShares}')"
