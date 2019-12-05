from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

from app import routes, models
