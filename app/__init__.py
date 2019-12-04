from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from app import routes
#from app import routes, models

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.run(port=5000, debug=True)
