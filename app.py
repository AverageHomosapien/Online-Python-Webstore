from flask import Flask, render_template
import random
from flask_login import current_user

app = Flask(__name__, static_folder="static")
user_auth = False

@app.route('/')
@app.route('/index')
def names():
    #names = ["Harry", "Tommy", "Johnny", "Franz Winklebottom"]
    #return render_template('index_for_user.html', names=names)
    if current_user.is_authenticated:
         return render_template("index_for_user.html")
    else:
         return render_template("index_for_anomymous.html")


@app.route('/register')
@app.route('/login')
def login():
    return render_template('register.html')


if __name__ == '__main__':
        app.run(debug=True)
