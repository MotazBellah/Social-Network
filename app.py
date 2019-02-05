from flask import Flask, g
from flask.ext.login import LoginManager
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
    g.db.connect()


@app.after_request
def after_request(response):
    """Close to the database after each request. """
    g.db.close()
    return response



if __name__ == '__main__':
    models.initiatize()
    models.User.create_user(
        name="MoatazBellah",
        email="moatazbellahhamdy@gmail.com",
        password='0185809035',
        admin=True,
        bio='I am google software engineer'
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)
