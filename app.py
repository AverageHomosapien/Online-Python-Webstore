from datetime import datetime
from app import app, db

### Users
#add_user('John02', 'ginger@gmail.com', 'dinkladd', 'Joseph Smith', '8 beach road')
#add_user('Brad69', 'brad@gmail.com', '1234', 'Brad Johnston', '4 palm lane')

#######################################
# Functions to interact with Database #
#######################################

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User': User, 'Item': Item, 'Order': Order, 'OrderItem': OrderItem}

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
