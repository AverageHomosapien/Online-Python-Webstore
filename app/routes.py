from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import RegistrationForm, LoginForm
from app.models import User, Order, OrderItem, Item
from app import app, db
from datetime import datetime
import os
from pathlib import Path

cart = []
wishlist = []

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

# Homepage
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def names():
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("index.html")

# Register/Login Page
@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user registered return to homepage
    if current_user.is_authenticated:
        return redirect('/index')
    return render_template('register.html')

# Logging in
@app.route('/loginform', methods=['GET', 'POST'])
def login_form():
    # If user registered return to homepage
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

# Registration page
@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    # If user registered return to homepage
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegistrationForm()
    if form.is_submitted():
        flash('Registration requested for user {}, remember_me={}'.format(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data))
        add_user(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data)
        return redirect('/index')
    return render_template('registration_form.html', form=form)

# Account page
@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/<user>', methods = ['GET', 'SET'])
def account(user=""):
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("account.html")

# Orders page
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("orders.html")

# Wishlist page
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist_function():
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    # Checking for post
    if request.method == 'POST':
        item_name_to_del = str(request.form['button'])
        item_name_to_del = item_name_to_del[:-9] # Removing -wishlist from back of item - comes as 'Football-wishlist'
        for cat in Item.query.distinct(Item.name):
            # If DB item name matches page item
            if cat.name == item_name_to_del:
                if cat.id in wishlist:
                    wishlist.remove(cat.id)
    item_list, price_list, quantity_list, file_names = [], [], [], []
    # Checking through database for wishlist items based on ID
    for cat in Item.query.distinct(Item.id):
        if cat.id in wishlist:
            price_list.append(cat.amount)
            quantity_list.append(cat.quantity)
            item_list.append(cat.name)
            # Checking for file extension
            dir = os.path.join(app.config['ITEM_FOLDER'], str(cat.id))
            ext = check_img_extension(dir)
            if ext == "": # Remove from list
                item_categories.pop()
                item_ids.pop()
            else:
                file_names.append("static/img/items/" + str(cat.id) + ext)
    return render_template("wishlist.html", item_list = item_list, price = price_list, quantity = quantity_list, files = file_names)

# Settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("settings.html")

# Selling page
@app.route('/selling', methods=['GET', 'POST'])
def selling():
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    return render_template("selling.html")

# Category and subcategory pages
@app.route('/category', methods=['GET', 'POST'])
@app.route('/category/<type>', methods=['GET', 'POST'])
def category(type=""):
    item_ids, item_categories, file_names = [], [], []
    count = 1
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    if type == "": # If category unselected (base category page)
        for cat in Item.query.distinct(Item.category):
            if cat.category not in item_categories:
                item_categories.append(cat.category)
                item_ids.append(count)
                # Checking for file extension
                dir = os.path.join(app.config['ITEM_FOLDER'], str(count))
                ext = check_img_extension(dir)
                if ext == "": # Remove from list
                    item_categories.pop()
                    item_ids.pop()
                else:
                    file_names.append("static/img/items/" + str(count) + ext)
            count+=1
        return render_template("category.html", categories = item_categories, files = file_names)
    else: # if category selected (subcategory page)
        item_price, item_quantity, items = [], [], []
        type = str(type)
        # Checking through database by category to display category items
        for cat in Item.query.distinct(Item.category):
            if cat.category == type:
                item_ids.append(count)
                items.append(cat.name)
                item_price.append(cat.amount)
                item_quantity.append(cat.quantity)
                # Checking for file extension
                dir = os.path.join(app.config['ITEM_FOLDER'], str(count))
                ext = check_img_extension(dir)
                # If the image doesn't exist
                if ext == "":
                    item_categories.pop()
                    item_ids.pop()
                    item_price.pop()
                    item_quantity.pop()
                else: # If the image does exist and file extension has been found
                    file_names.append("../static/img/items/" + str(count) + ext)
            count+=1
        # Checking for post
        if request.method == 'POST':
            contained = False
            item_count = 0
            for item in items:
                if item == request.form['button']:
                    for product in cart:
                        # checking if product contained in cart
                        if item_ids[item_count] == product[0]:
                            contained = True
                            product[1] += 1
                    # otherwise adding a new entry
                    if contained == False:
                        cart.append([item_ids[item_count], 1])
                elif request.form['button'] == str(item) + "-wishlist":
                    # Checks each name in the database and matches the id
                    for dbitem in Item.query.distinct(Item.name):
                        if item == dbitem.name:
                            # Checking if unique
                            if dbitem.id not in wishlist:
                                wishlist.append(dbitem.id)
                item_count += 1
        return render_template("category_items.html", categories = items, files = file_names, quantity = item_quantity, price = item_price, subcat = type)

# Checks out the user items
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    basket, name, cost, stock, files, item_ids = [], [], [], [], [], []
    total_cost = 0.
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    # looping through the shopping cart [item ID][quantity requested]
    for item in cart:
        for db_item in Item.query.distinct(Item.id):
            if item[0] == db_item.id:
                # Getting item IDs, name, cost and stock levels
                item_ids.append(db_item.id)
                name.append(db_item.name)
                cost.append(db_item.amount)
                stock.append(db_item.quantity)
                # Checking for file extension
                temp_fp = app.config['ITEM_FOLDER'] + "\\" + str(db_item.id)
                string = check_img_extension(temp_fp)
                fp = "static/img/items/" + str(db_item.id) + string
                files.append(fp)
                # Updating total cost
                total_cost += (cost[-1] * item[1])
                break
    # If post method
    if request.method == 'POST':
        item_count = 0
        total_cost = 0
        button_type = "remove_item"
        try:
            if request.form.get('checkout-button') == "checkout":
                button_type = "checkout"
        finally:
            if button_type == "remove_item":
                for item in name:
                    if item == request.form['button']:
                        inner_count = 0
                        for product in cart:
                            if item_ids[item_count] == product[0]:
                                product[1] -= 1
                            # Checking if there are no items ordered for product 1
                            if product[1] == 0:
                                cart.pop(inner_count)
                            total_cost += (cost[inner_count] * product[1])
                            inner_count += 1
                    item_count += 1
            elif button_type == "checkout":
                for cart_item in cart:
                    for db_item in Item.query.distinct(Item.id):
                        if cart_item[0] == db_item.id: # If item in cart matches database item
                            db_item.quantity = db_item.quantity - cart_item[1]
                db.session.commit() # Commit to the database
                del cart[:] # Delete the cart's entire contents
                return render_template('/index.html')
    return render_template("checkout.html", basket = cart, name = name, cost = cost, stock = stock, files = files, value = total_cost)

# Logout page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # If user unregistered return to registration page
    if not current_user.is_authenticated:
        return redirect('/register')
    print_to_console(str(current_user) + " Logged Out")
    logout_user()
    return redirect('/register')
