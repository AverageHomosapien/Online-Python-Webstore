from flask import Flask, render_template, flash, redirect
import flask_login
from flask_login import current_user, LoginManager
import forms
from database import db
from models import models
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from common import db
from config import Config
from forms import RegistrationForm, LoginForm
from __init__ import create_app

app = create_app()
db.app = app
app.app_context().push()
#db.app = app
db.create_all(app=create_app())

#app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)


#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

#db.app = app
#db.create_all()
#models.db.init_app(app)
#with app.app_context():
#    db.init_app(app)
#    models.db.create_all()

u = models.User(username = 'John012', email = 'john@gmail.com', password_hash = 'dinkle', name = 'John Smith', address = '5 beach road')
models.db.session.add(u)
models.db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def names():
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
        app.run(debug=True)
