"""Tests for pyrecipe/app/viewmodels."""

import pytest

from flask import Response

from pyrecipe.usecases.account_uc import AccountUC
from pyrecipe.app.viewmodels.account import IndexViewModel
from pyrecipe.app.viewmodels.account import RegisterViewModel
from pyrecipe.app.viewmodels.account import LoginViewModel
from pyrecipe.app import app as flask_app


def test_idxvm(mocker):
    """
    GIVEN
    WHEN a request is passed through the IndexViewModel
    THEN assert no errors are received
    """
    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account", data=None):
        vm = IndexViewModel()

    vm.to_dict()
    assert vm.error is None


def test_logvm_valid(mocker):
    """
    GIVEN a user login POST
    WHEN passed through the LoginViewModel
    THEN assert no errors are received
    """
    form_data = {
        "email": "dude@mail.com",
        "password": "123456"
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/login", data=form_data):
        vm = LoginViewModel()

    vm.validate()
    assert vm.error is None


def test_logvm_noemail(mocker):
    """
    GIVEN a user login POST with no email address
    WHEN passed through the LoginViewModel
    THEN assert the correct error is received
    """
    form_data = {
        "email": None,
        "password": "123456"
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/login", data=form_data):
        vm = LoginViewModel()

    vm.validate()
    assert vm.error == "Please enter an email address."


def test_logvm_nopwd(mocker):
    """
    GIVEN a user login POST with no password
    WHEN passed through the LoginViewModel
    THEN assert the correct error is received
    """
    form_data = {
        "email": "dude@mail.com",
        "password": None,
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/login", data=form_data):
        vm = LoginViewModel()

    vm.validate()
    assert vm.error == "Please enter a password."


def test_regvm_valid(mocker):
    """
    GIVEN valid user form data
    WHEN passed through the RegisterViewModel
    THEN assert no errors are received
    """
    form_data = {
        "name": "dude",
        "email": "dude@mail.com",
        "password": "123456"
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/register", data=form_data):
        vm = RegisterViewModel()

    vm.validate()
    assert vm.error is None


def test_regvm_noname(mocker):
    """
    GIVEN user form data with no given name
    WHEN passed through the RegisterViewModel
    THEN assert proper error returned
    """
    form_data = {
        "name": None,
        "email": "dude@mail.com",
        "password": "123456"
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/register", data=form_data):
        vm = RegisterViewModel()

    vm.validate()
    assert vm.error == "You must specify a name."


def test_regvm_noemail(mocker):
    """
    GIVEN user form data with no given email
    WHEN passed through the RegisterViewModel
    THEN assert proper error returned
    """
    form_data = {
        "name": "dude",
        "email": None,
        "password": "123456"
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/register", data=form_data):
        vm = RegisterViewModel()

    vm.validate()
    assert vm.error == "You must specify an email address."


def test_regvm_nopassword(mocker):
    """
    GIVEN user form data with no given password
    WHEN passed through the RegisterViewModel
    THEN assert proper error returned
    """
    form_data = {
        "name": "dude",
        "email": "dude@mail.com",
        "password": None
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/register", data=form_data):
        vm = RegisterViewModel()

    vm.validate()
    assert vm.error == "You must specify a password."


def test_regvm_badpassword(mocker):
    """
    GIVEN user form data with a short password
    WHEN passed through the RegisterViewModel
    THEN assert proper error returned
    """
    form_data = {
        "name": "dude",
        "email": "dude@mail.com",
        "password": "1234",
    }

    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path="/account/register", data=form_data):
        vm = RegisterViewModel()

    vm.validate()
    assert vm.error == "The password must be at least 5 characters."
