from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask.ext.login import LoginManager
import forms
import models

DEBUG = True
PORT = 8000
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
    if g.db.is_closed():
        g.db.connect()
    # g.db = models.DATABASE.connect()


@app.after_request
def after_request(response):
    """Close to the database after each request. """
    if not g.db.is_closed():
        g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/')
def index():
    return 'Hey'

if __name__ == '__main__':
    models.initiatize()
    try:
        models.User.create_user(
            username="MoatazBellah",
            email="moatazbellahhamdy@gmail.com",
            password='0185809035',
            admin=True,
            bio='I am google software engineer'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
