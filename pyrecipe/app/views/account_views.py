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
    pass


@blueprint.route("/logout")
def logout():
    pass


@blueprint.route("/register", methods=["GET"])
def register_get():
    pass


@blueprint.route("/register", methods=["POST"])
def register_post():
    pass


@blueprint.route("/account")
def account():
    pass
