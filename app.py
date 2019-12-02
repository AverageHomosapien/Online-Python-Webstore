from flask import Flask, render_template, flash, redirect
from flask_migrate import Migrate
from flask_login import current_user, LoginManager
import flask_login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import forms
from models import User, Order, OrderItem, Item
from common import db
from config import Config
from forms import RegistrationForm, LoginForm

#session = Session()
app = Flask(__name__, static_folder="static")
app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)

#app.app_context().push()

#db = SQLAlchemy(app)

# u = Item(655)
# db.session.add(u)
# db.session.commit()
#db.init_app(app)
#u = User(username = 'silly', email = 'mail.com', password_hash = 'dwaynetherock', name = 'Dookie Smith', address = '8 beach road')


def add_user():
    u = User(username = 'John02', email = 'ginger@gmail.com', password_hash = 'dinkladd', name = 'Joseph Smith', address = '8 beach road')
    db.session.add(u)
    db.session.commit()


def rem_user():
    u = User(username = 'John02', email = 'ginger@gmail.com', password_hash = 'dinkladd', name = 'Joseph Smith', address = '8 beach road')
    db.session.query(u).delete()
    db.session.commit()
    #models.db.session.rollback()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def names():
    add_user()
    return render_template("index.html")

# Register/Login Page
@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('register.html')

# Logging in
@app.route('/loginform', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.is_submitted():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.password.data))
        return redirect('/index')
    return render_template('login_form.html', form=form)

# Registering
@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    form = RegistrationForm()
    if form.is_submitted():
        flash('Registration requested for user {}, remember_me={}'.format(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data))
        return redirect('/index')
    return render_template('registration_form.html', form=form)

@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/<user>', methods = ['GET', 'SET'])
def account(user=""):
    return render_template("account.html")

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    return render_template("orders.html")

@app.route('/saved_items', methods=['GET', 'POST'])
def saveditems():
    return render_template("saved_items.html")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("settings.html")

@app.route('/selling', methods=['GET', 'POST'])
def selling():
    return render_template("selling.html")

@app.route('/category', methods=['GET', 'POST'])
def category():
    return render_template("category.html")

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    return render_template("basket.html")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template("checkout.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template("register.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)
