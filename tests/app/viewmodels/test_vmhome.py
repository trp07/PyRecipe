"""Tests for pyrecipe/app/viewmodels."""

from collections import namedtuple

import pytest

from flask import Response

from pyrecipe.usecases.account_uc import AccountUC
from pyrecipe.app.viewmodels.home import AboutViewModel
from pyrecipe.app.viewmodels.home import IndexViewModel
from pyrecipe.app import app as flask_app


USER = namedtuple("User", ["name"])


def test_idxvm_nouser(mocker):
    """
    GIVEN a no logged-in user
    WHEN a view request for /index is initiated
    THEN assert no errors and the user is "Guest"
    """
    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path='/index', data=None):
        vm = IndexViewModel()

    vm.validate()
    result = vm.to_dict()
    assert vm.error is None
    assert result["name"] == "Guest"


def test_idxvm_withuser(mocker):
    """
    GIVEN a logged in user
    WHEN a view request for /index is initiated
    THEN assert no errors and the user is the logged in user
    """
    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = USER("Dude")
    with flask_app.test_request_context(path='/index', data=None):
        vm = IndexViewModel()

    vm.validate()
    result = vm.to_dict()
    assert vm.error is None
    assert result["name"] == "Dude"


def test_aboutvm(mocker):
    """
    GIVEN a running app
    WHEN /about view is requested
    THEN assert no errors
    """
    target = mocker.patch.object(AccountUC, "find_user_by_id")
    target.return_value = None
    with flask_app.test_request_context(path='/about', data=None):
        vm = AboutViewModel()
    assert isinstance(vm, AboutViewModel)
