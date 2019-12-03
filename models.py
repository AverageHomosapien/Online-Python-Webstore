from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from common import db

# User DB
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    name = db.Column(db.String(80))
    address = db.Column(db.String(160))
    orders = db.relationship('Order', backref='ordered', lazy='dynamic')

    def __init__(self, username, email, password, name, address):
        self.username = username
        self.email = email
        self.name = name
        self.address = address
        self.set_password(password)

    # hashes the password and saves to user
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # checks the password to see if it's valid or not
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



# Order DB
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bought = db.relationship('OrderItem', backref='items', lazy='dynamic')

    def __init__(self, amount, user_id):
        self.amount = amount


    def __repr__(self):
        return '<Order {}>'.format(self.id)

# Order Item DB
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return '<Order {}>'.format(self.id)

# Item DB
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    ordered = db.relationship('OrderItem', backref='ordered', lazy='dynamic')

    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return '<Item {}>'.format(self.id)
