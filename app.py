from flask import Flask, g, render_template, flash, redirect, url_for
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user
import forms
import models

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'njgnbfdng!2fkgj9856&!jmbk[pln]wrtj,.kydaSHAPA'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None



@app.before_request
def before_request():
    """Connect to the database before each request. """
    g.db = models.DATABASE
    g.db.connect(reuse_if_open=True)
    # g.db = models.DATABASE.connect()


@app.after_request
def after_request(response):
    """Close to the database after each request. """
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You registered!", 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email==form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return 'Hey'

if __name__ == '__main__':
    models.initiatize()
    try:
        models.User.create_user(
            username="MoatazBellah",
            email="moatazbellah@gmail.com",
            password='123456',
            admin=True,
            bio='I am software engineer'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
