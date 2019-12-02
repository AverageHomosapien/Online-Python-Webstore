from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)
    db.init_app(app)
    #db.create_all()
    #db.create_all()
    return app
