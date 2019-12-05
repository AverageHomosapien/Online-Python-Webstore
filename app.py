from datetime import datetime
from flaskapp import app, db

### Users
#add_user('John02', 'ginger@gmail.com', 'dinkladd', 'Joseph Smith', '8 beach road')
#add_user('Brad69', 'brad@gmail.com', '1234', 'Brad Johnston', '4 palm lane')

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User': User, 'Item': Item, 'Order': Order, 'OrderItem': OrderItem}
