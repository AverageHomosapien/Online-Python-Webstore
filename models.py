from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from common import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    name = db.Column(db.String(80))
    address = db.Column(db.String(160))
    orders = db.relationship('Order', backref='ordered', lazy='dynamic')

    def __init__(self, username, email, password_hash, name, address):
        self.username = username
        self.password_hash = password_hash
    #    #self.password = set_password(password)
        self.email = email
        self.name = name
        self.address = address
    #    self.save_to_db()

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bought = db.relationship('OrderItem', backref='items', lazy='dynamic')

    def __repr__(self):
        return '<Order {}>'.format(self.id)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return '<Order {}>'.format(self.id)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    ordered = db.relationship('OrderItem', backref='ordered', lazy='dynamic')

    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return '<Item {}>'.format(self.id)
