from . import config

from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(config.Config)


# login context manager.
# if the user is not logged in, redirect the user
# to the login page, then back to the page they wish
# to view after successfully logging in.
login = LoginManager(app)
login.login_view = "login"


# import routes last after "app" is initialized.
from . import forms
from . import routes
