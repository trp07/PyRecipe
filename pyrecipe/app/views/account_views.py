"""View controllers associated with account features."""

import flask

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.storage import User
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.viewmodels.account import IndexViewModel, RegisterViewModel
import pyrecipe.app.helpers.cookie_auth as cookie_auth


blueprint = flask.Blueprint(
    "account", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)

#################### Index ##########################

@blueprint.route("/account", methods=["GET"])
@blueprint.route("/account/", methods=["GET"])
@response(template_file="account/index.html")
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect(flask.url_for("account.login_get"))

    return vm.to_dict()


#################### Login ##########################

@blueprint.route("/account/login", methods=["GET"])
@blueprint.route("/login", methods=["GET"])
@response(template_file="account/login.html")
def login_get():
    return {}


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

    user = User.login_user(email=email, password=password)
    if not user:
        return {
            "email": email,
            "password": password,
            "error": "The account does not exist or the password is incorrect."
        }

    response = flask.redirect(flask.url_for("account.index"))
    cookie_auth.set_auth(response, user.id)

    return response


#################### Logout #########################

@blueprint.route("/account/logout")
@blueprint.route("/logout")
@response(template_file="account/logout.html")
def logout():
    response = flask.redirect(flask.url_for("home.index"))
    cookie_auth.logout(response)
    return response


#################### Register #######################

@blueprint.route("/account/register", methods=["GET"])
@blueprint.route("/register", methods=["GET"])
@response(template_file="account/register.html")
def register_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route("/account/register", methods=["POST"])
@blueprint.route("/register", methods=["POST"])
@response(template_file="account/register.html")
def register_post():
    vm = RegisterViewModel()

    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = User.create_user(name=vm.name, email=vm.email, password=vm.password)
    if not user:
        return vm.to_dict()

    response = flask.redirect(flask.url_for("account.index"))
    cookie_auth.set_auth(response, user.id)

    return response

