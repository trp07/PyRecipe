"""
TODO
relocate: login, logout, register, etc.
"""
import flask

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.storage import User


blueprint = flask.Blueprint(
    "account", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


@blueprint.route("/account")
def account():
    return "Not Implemented... yet!"


@blueprint.route("/account/login", methods=["GET"])
@blueprint.route("/login")
@response(template_file="account/login.html")
def login_get():
    return "Not Implemented... yet!"


@blueprint.route("/account/login", methods=["POST"])
@blueprint.route("/login")
@response(template_file="account/login.html")
def login_post():
    return "Not Implemented... yet!"


@blueprint.route("/account/logout")
@blueprint.route("/logout")
@response(template_file="account/logout.html")
def logout():
    return "Not Implemented... yet!"


@blueprint.route("/account/register", methods=["GET"])
@blueprint.route("/register", methods=["GET"])
@response(template_file="account/register.html")
def register_get():
    return {}


@blueprint.route("/account/register", methods=["POST"])
@blueprint.route("/register", methods=["POST"])
@response(template_file="account/register.html")
def register_post():
    return {}
