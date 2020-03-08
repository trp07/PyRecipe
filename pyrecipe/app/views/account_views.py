"""View controllers associated with account features."""

import flask

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.static import STATICDIR
from pyrecipe.storage import User
from pyrecipe.usecases import account_uc
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.viewmodels.account import IndexViewModel
from pyrecipe.app.viewmodels.account import RegisterViewModel
from pyrecipe.app.viewmodels.account import LoginViewModel
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
    vm = LoginViewModel()
    return vm.to_dict()


@blueprint.route("/account/login", methods=["POST"])
@blueprint.route("/login", methods=["POST"])
@response(template_file="account/login.html")
def login_post():
    vm = LoginViewModel()

    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = account_uc.login_user(email=vm.email, password=vm.password)
    if not user:
        vm.error = "Username or password are incorrect."
        return vm.to_dict()

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

    user = account_uc.register_user(name=vm.name, email=vm.email, password=vm.password)
    if not user:
        vm.error = "User with email address already exists."
        return vm.to_dict()

    response = flask.redirect(flask.url_for("account.index"))
    cookie_auth.set_auth(response, user.id)

    return response
