from datetime import datetime
from flaskapp import app, db

@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User': User, 'Item': Item, 'Order': Order, 'OrderItem': OrderItem}
