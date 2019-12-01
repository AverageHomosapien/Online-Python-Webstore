from flask import Flask, render_template
import random
import flask_login
from flask_login import current_user, LoginManager
from config import Config

app = Flask(__name__, static_folder="static")
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

#@app.route('/hello/<user>')
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def names():        #return render_template('index_for_user.html', names=names)
    #facultyId = name if facultyId else None
    #if current_user.is_authenticated:
    #     return render_template("index.html")
    #else:
    #     return render_template("register.html")
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template("index_for_user.html")
    else:
        return render_template("register.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #logout the user
    render_template("register.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
        app.run(debug=True)
