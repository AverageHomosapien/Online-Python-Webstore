from flask import Flask, render_template, flash, redirect
import flask_login
from flask_login import current_user, LoginManager
from forms import RegistrationForm, LoginForm
#from config import Config

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = "has8d912hA9j0dJAS9077ghasdNmNU642"
#app.config.from_object('config.cfg')
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

# Register/Login Page
@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('register.html')

# Logging in
@app.route('/loginform', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.is_submitted():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.password.data))
        return redirect('/index')
    return render_template('login_form.html', form=form)

# Registering
@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    form = RegistrationForm()
    if form.is_submitted():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.email.data, form.password.data, form.name.data, form.address.data))
        return redirect('/index')
    return render_template('registration_form.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #logout the user
    return render_template("register.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
        app.run(debug=True)
