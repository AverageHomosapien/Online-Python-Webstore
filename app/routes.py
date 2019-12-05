from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import RegistrationForm, LoginForm
from app.models import User, Order, OrderItem, Item
from app import app, db
from datetime import datetime
import os
from pathlib import Path

#######################################
# Functions to interact with Database #
#######################################

# Adds user to the database
def add_user(username, email, password, name, address):
    try:
        u = User(username, lower(email), password, name, address)
        db.session.add(u)
        db.session.commit()
    except:
        print_to_console(username + ") failed attempt to be added to the database")

# Removes user from the database (untested)
def remove_user(username):
    try:
        u = User(username = 'John02', email = 'ginger@gmail.com', password_hash = 'dinkladd', name = 'Joseph Smith', address = '8 beach road')
        db.session.query(u).delete()
        db.session.commit()
    except:
        print_to_console(username + ") failed attempt to be removed from the database")

# Prints a message to the console with a timestamp
def print_to_console(message):
    print(datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y") + " - " + str(message))

#####################
# Routing functions #
#####################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def names():
    return render_template("index.html")

# Register/Login Page
@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    return render_template('register.html')

# Logging in
@app.route('/loginform', methods=['GET', 'POST'])
def login_form():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        print_to_console("Login requested for user " + str(form.username.data))
        #if user is None or not user.check_password(form.password.data):
        if user is None:
            flash("Invalid username or password")
            print_to_console("Login failed for user " + str(form.username.data))
            return redirect('/loginform')
        elif not user.check_password(form.password.data):
            flash("Invalid username or password")
            print_to_console("Login failed for user " + str(form.username.data))
            return redirect('/loginform')
        print_to_console("Login successful for user " + str(form.username.data))
        login_user(user)
        return redirect('/index')
    return render_template('login_form.html', form=form)

# Registering
@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegistrationForm()
    if form.is_submitted():
        print("submitted!!")
        flash('Registration requested for user {}, remember_me={}'.format(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data))
        return redirect('/index')
    return render_template('registration_form.html', form=form)

@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/<user>', methods = ['GET', 'SET'])
def account(user=""):
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("account.html")

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("orders.html")

@app.route('/saved_items', methods=['GET', 'POST'])
def saveditems():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("saved_items.html")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("settings.html")

@app.route('/selling', methods=['GET', 'POST'])
def selling():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("selling.html")

@app.route('/category', methods=['GET', 'POST'])
def category():
    if not current_user.is_authenticated:
        return redirect('/register')
    count = 1
    item_ids = []
    item_categories = []
    file_names = []
    for cat in Item.query.distinct(Item.category):
        if cat.category not in item_categories:
            item_categories.append(cat.category)
            item_ids.append(count)
        count+=1
    for id in item_ids:
        dir = os.path.join(app.config['ITEM_FOLDER'], str(id))
        if os.path.exists(dir + ".jpg"):
            file_names.append("static/img/items/" + str(id) + ".jpg")
        elif os.path.exists(dir + ".png"):
            file_names.append("static/img/items/" + str(id) + ".png")
    return render_template("category.html", categories = item_categories, files = file_names)

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("basket.html")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("checkout.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/register')
