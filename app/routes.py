from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import RegistrationForm, LoginForm
from app.models import User, Order, OrderItem, Item
from app import app, db
from datetime import datetime
import os
from pathlib import Path

cart = []

#######################################
# Functions to interact with Database #
#######################################

# Adds user to the database
def add_user(username, email, password, name, address):
    try:
        u = User(username, email, password, name, address)
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

# Checks to see if an image string (without extension) exists by checking image with various file extensions
def check_img_extension(file_string):
    if os.path.exists(file_string + ".jpg"):
        return ".jpg"
    elif os.path.exists(file_string + ".png"):
        return ".png"
    elif os.path.exists(file_string + ".gif"):
        return ".gif"
    return ""

#####################
# Routing functions #
#####################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def names():
    if not current_user.is_authenticated:
        return redirect('/register')
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
        flash('Registration requested for user {}, remember_me={}'.format(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data))
        add_user(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data)
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

@app.route('/category', methods=['GET'])
@app.route('/category/<type>', methods=['GET', 'POST'])
def category(type=""):
    if not current_user.is_authenticated:
        return redirect('/register')
    if type == "": # If category hasn't been selected yet
        count = 1
        item_ids = []
        item_categories = []
        file_names = []
        for cat in Item.query.distinct(Item.category):
            if cat.category not in item_categories:
                item_categories.append(cat.category)
                item_ids.append(count)
                dir = os.path.join(app.config['ITEM_FOLDER'], str(count))
                ext = check_img_extension(dir)
                if ext == "": # Remove from list
                    item_categories.pop()
                    item_ids.pop()
                else:
                    file_names.append("static/img/items/" + str(count) + ext)
            count+=1
        return render_template("category.html", categories = item_categories, files = file_names)
    else: # if category has been selected
        count = 1
        item_ids, file_names, items, item_price, item_quantity, item_categories = [], [], [], [], [], []
        type = str(type)
        for cat in Item.query.distinct(Item.category):
            if cat.category == type:
                item_ids.append(count)
                items.append(cat.name)
                item_price.append(cat.amount)
                item_quantity.append(cat.quantity)
                dir = os.path.join(app.config['ITEM_FOLDER'], str(count))
                ext = check_img_extension(dir)
                if ext == "": # Remove from list
                    item_categories.pop()
                    item_ids.pop()
                    item_price.pop()
                    item_quantity.pop()
                else:
                    file_names.append("../static/img/items/" + str(count) + ext)
            count+=1
        if request.method == 'POST':
            contained = False
            item_count = 0
            for item in items:
                if item == request.form['button']:
                    for product in cart:
                        if item_ids[item_count] == product[0]:
                            contained = True
                            product[1] += 1
                    if contained == False:
                        cart.append([item_ids[item_count], 1])
                item_count += 1
        return render_template("category_items.html", categories = items, files = file_names, quantity = item_quantity, price = item_price, subcat = type)

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("basket.html")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("checkout.html", basket = [[2,3],[4,1],[5,2]],
        categories = ["Basketball", "Nintendo Switch", "iPhone X"], cost = [12.95,450.99,659.99],
        stock = [23, 9, 12], files = ["static/img/items/2.png", "static/img/items/4.jpg", "static/img/items/5.png"],
        total_cost = 1809.82)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    print_to_console(str(current_user) + " Logged Out")
    logout_user()
    return redirect('/register')
