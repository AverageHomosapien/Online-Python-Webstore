from flask import Flask, render_template
import random

app = Flask(__name__, static_folder="static")

@app.route('/')
def names():
    names = ["Harry", "Tommy", "Johnny", "Franz Winklebottom"]
    return render_template('index.html', names=names)


if __name__ == '__main__':
        app.run(debug=True)
