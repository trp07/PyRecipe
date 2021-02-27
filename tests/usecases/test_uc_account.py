"""Test for the usecases/account_uc.py module."""

from unittest.mock import Mock

import pytest

from pyrecipe.usecases.account_uc import AccountUC


def test_accountuc_instantiation():
    """
    GIVEN a DB driver to instantiate in the Use Case
    WHEN instantiating
    THEN assert it is created
    """
    a = AccountUC(Mock())
    assert a._driver is not None


def test_login_user():
    """
    GIVEN users in the DB
    WHEN trying to log in
    THEN assert user logs in
    """
    a = AccountUC(Mock())
    a._driver.user_login.return_value = "UserModel"

    result = a.login_user("bob@mail.com", "bobrulz")
    assert result == "UserModel"


def test_register_user():
    """
    GIVEN a new user to register
    WHEN registering
    THEN assert user is returned
    """
    a = AccountUC(Mock())
    a._driver.user_create.return_value = "UserModel"

    user = a.register_user("arthur", "arthur@mail.com", "arthurrulz")
    assert user == "UserModel"


def test_find_user_by_id():
    a = AccountUC(Mock())
    a._driver.user_find_by_id.return_value = "UserModel"

    result = a.find_user_by_id("12345")
    assert result == "UserModel"
