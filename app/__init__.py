from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
#from app import routes, models

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.run(port=5000, debug=True)

from app import routes, models
