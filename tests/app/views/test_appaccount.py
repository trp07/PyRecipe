"""Tests for pyrecipe/app/views."""

import pytest

from flask import Response

from pyrecipe.usecases.account_uc import AccountUC
from pyrecipe.app.viewmodels.account import IndexViewModel
from pyrecipe.app import app as flask_app
from pyrecipe.app.views import account_views


#################### Index ##########################

def test_index_loggedin(mocker):
    """
    GIVEN user is already logged in
    WHEN user navigates to /account
    THEN assert no errors returned
    """
    acct = mocker.patch.object(AccountUC, "find_user_by_id")
    acct.return_value = "FOUND"
    idxvm = mocker.patch.object(IndexViewModel, "__call__")
    with flask_app.test_request_context(path="/account", data=None):
        resp: Response = account_views.index()
    assert resp.location is None


def test_index_loggedout(mocker):
    """
    GIVEN user is not already logged in
    WHEN user navigates to /account
    THEN assert redirected to /login
    """
    acct = mocker.patch.object(AccountUC, "find_user_by_id")
    acct.return_value = None
    idxvm = mocker.patch.object(IndexViewModel, "__call__")
    with flask_app.test_request_context(path="/account", data=None):
        resp: Response = account_views.index()
    assert resp.location in ("/login", "/account/login")


#################### Login ##########################

def test_login_get(mocker):
    """
    GIVEN a running app
    WHEN a get-request for /account/login occurs
    THEN assert no errors
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    with flask_app.test_request_context(path="/account/login", data=None):
        resp: Response = account_views.login_get()
    assert resp.location is None


def test_login_post_valid(mocker, testuser):
    """
    GIVEN a running app
    WHEN valid user logs in
    THEN assert no errors and redirected to /account
    """
    form_data = {
        "email": "dude@mail.com",
        "password": "123456"
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    login = mocker.patch.object(AccountUC, "login_user")
    login.return_value = testuser(**form_data)

    with flask_app.test_request_context(path="/account/login", data=form_data):
        resp: Response = account_views.login_post()
    assert resp.location in ("/account", "/account/")


def test_login_post_invalid(mocker):
    """
    GIVEN a running app
    WHEN invalid user logs int (bad password)
    THEN assert no redirect, stays at login
    """
    form_data = {
        "email": "dude@mail.com",
        "password": "123456"
    }
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    login = mocker.patch.object(AccountUC, "login_user")
    login.return_value = None

    with flask_app.test_request_context(path="/account/login", data=form_data):
        resp: Response = account_views.login_post()
    assert resp.location is None


#################### Logout #########################

def test_logout():
    """
    GIVEN a logged-in user
    WHEN user selects logout
    THEN assert no errors and user is returned to /index
    """
    with flask_app.test_request_context(path="/account/logout", data=None):
        resp: Response = account_views.logout()
    assert resp.location in ("/", "/index")


#################### Register #######################

def test_register_get(mocker):
    """
    GIVEN a running app
    WHEN a get-request for /account/register occurs
    THEN assert no errors
    """
    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    with flask_app.test_request_context(path="/account/register", data=None):
        resp: Response = account_views.register_get()
    assert resp.location is None


def test_register_post_valid(mocker, testuser):
    """
    GIVEN valid user form data
    WHEN posted through register_post
    THEN assert user routed to correct url
    """
    form_data = {
        "name": "dude",
        "email": "dude@mail.com",
        "password": "123456"
    }

    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    register = mocker.patch.object(AccountUC, "register_user")
    register.return_value = testuser(**form_data)

    with flask_app.test_request_context(path="/account/register", data=form_data):
        resp: Response = account_views.register_post()
    assert resp.location in ("/account", "/account/")


def test_register_post_invalid(mocker):
    """
    GIVEN user registration form data with email already in use
    WHEN posted through register_post
    THEN assert error is returned
    """
    form_data = {
        "name": "dude",
        "email": "dude@mail.com",
        "password": "123456"
    }

    find = mocker.patch.object(AccountUC, "find_user_by_id")
    find.return_value = None
    register = mocker.patch.object(AccountUC, "register_user")
    register.return_value = None

    with flask_app.test_request_context(path="/account/register", data=form_data):
        resp: Response = account_views.register_post()
    assert resp.location is None
