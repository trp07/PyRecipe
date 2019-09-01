"""
TODO
relocate: login, logout, register, etc.
"""
import flask

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.storage import User


blueprint = flask.Blueprint('account', __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR))


@blueprint.route("/login")
def login():
    return "Not Implemented... yet!"


@blueprint.route("/logout")
def logout():
    return "Not Implemented... yet!"


@blueprint.route("/register", methods=["GET"])
def register_get():
    return "Not Implemented... yet!"


@blueprint.route("/register", methods=["POST"])
def register_post():
    return "Not Implemented... yet!"


@blueprint.route("/account")
def account():
    return "Not Implemented... yet!"
