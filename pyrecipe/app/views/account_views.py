"""View controllers associated with account features."""

import flask

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.storage import User


blueprint = flask.Blueprint(
    "account", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


@blueprint.route("/account", methods=["GET"])
def account():
    return "Not Implemented... yet!"


@blueprint.route("/account/login", methods=["GET"])
@blueprint.route("/login", methods=["GET"])
@response(template_file="account/login.html")
def login_get():
    return {"msg": "Not Implemented... yet!"}


@blueprint.route("/account/login", methods=["POST"])
@blueprint.route("/login", methods=["POST"])
@response(template_file="account/login.html")
def login_post():
    r = flask.request
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not email or not password:
        return {
            "email": email,
            "password": password,
            "error": "Some required fields are missing."
        }

    # TODO: validate the user
    user = User.login_user(email=email, password=password)
    if not user:
        return {
            "email": email,
            "password": password,
            "error": "The account does not exist or the password is incorrect."
        }
    # log in browser as a session
    return flask.redirect(flask.url_for("account.account"))


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
    r = flask.request
    name = r.form.get('name')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not name or not email or not password:
        return {
            "name": name,
            "email": email,
            "password": password,
            "error": "Some required fields are missing."
        }

    user = User.login_user(email=email, password=password)
    if not user:
        return {
            "name": name,
            "email": email,
            "password": password,
            "error": "A user with that email already exists."
        }
    # log in browser as a session
    return flask.redirect(flask.url_for("account.account"))
