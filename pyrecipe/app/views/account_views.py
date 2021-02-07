"""View controllers associated with account features."""

import flask
from flask import current_app

from pyrecipe.frontend import TEMPLATESDIR
from pyrecipe.app.helpers.view_modifiers import response
from pyrecipe.app.viewmodels.account import IndexViewModel
from pyrecipe.app.viewmodels.account import RegisterViewModel
from pyrecipe.app.viewmodels.account import LoginViewModel
import pyrecipe.security.cookie_auth as cookie_auth
from pyrecipe.static import STATICDIR
from pyrecipe.usecases.account_uc import AccountUC


blueprint = flask.Blueprint(
    "account", __name__, template_folder=str(TEMPLATESDIR), static_folder=str(STATICDIR)
)


#################### Index ###################################################


@blueprint.route("/account", methods=["GET"])
@blueprint.route("/account/", methods=["GET"])
@response(template_file="account/index.html")
def index():
    vm = IndexViewModel()
    if not vm.user:
        flask.flash("You must be logged in", category="danger")
        return flask.redirect(flask.url_for("account.login_get"))

    return vm.to_dict()


#################### Login ###################################################

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

    uc = AccountUC(current_app.config["DB_DRIVER"])
    user = uc.login_user(email=vm.email, password=vm.password)
    if not user:
        vm.error = "Username or password are incorrect."
        return vm.to_dict()

    response = flask.redirect(flask.url_for("account.index"))
    cookie = cookie_auth.get_auth_cookie(user.id, current_app.config["SECRET_KEY"])
    response.set_cookie(
        key=current_app.config["COOKIE_NAME"],
        value=cookie,
        domain=current_app.config["DOMAIN"],
    )

    return response


#################### Logout ##################################################

@blueprint.route("/account/logout")
@blueprint.route("/logout")
@response(template_file="account/logout.html")
def logout():
    response = flask.redirect(flask.url_for("home.index"))
    response.delete_cookie(current_app.config["COOKIE_NAME"])
    flask.flash("You are logged out", category="primary")
    return response


#################### Register ################################################

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

    uc = AccountUC(current_app.config["DB_DRIVER"])
    user = uc.register_user(name=vm.name, email=vm.email, password=vm.password)
    if not user:
        flask.flash("Registration error", category="danger")
        vm.error = "User with email address already exists."
        return vm.to_dict()

    flask.flash("Registration successful", category="success")
    response = flask.redirect(flask.url_for("account.index"))
    cookie = cookie_auth.get_auth_cookie(user.id, current_app.config["SECRET_KEY"])
    response.set_cookie(
        key=current_app.config["COOKIE_NAME"],
        value=cookie,
        domain=current_app.config["DOMAIN"],
    )

    return response
