"""Test for the usecases/account_uc.py module."""

import pytest

from pyrecipe.usecases.account_uc import AccountUC


def test_recipeuc_instantiation(act_driver):
    """
    GIVEN a DB driver to instantiate in the Use Case
    WHEN instantiating
    THEN assert it is created
    """
    a = AccountUC(act_driver)
    assert a._driver is not None


def test_login_user(act_driver):
    """
    GIVEN users in the DB
    WHEN trying to log in
    THEN assert user logs in
    """
    a = AccountUC(act_driver)
    result = a.login_user("bob@mail.com", "bobrulz")
    assert result is not None


def test_register_user(act_driver):
    """
    GIVEN a new user to register
    WHEN registering
    THEN assert user is returned
    """
    a = AccountUC(act_driver)
    user = a.register_user("arthur", "arthur@mail.com", "arthurrulz")
    assert user.name == "arthur"


@pytest.mark.parametrize("_id, expected", [(123, "alice"), (456, "bob")])
def test_find_user_by_id(act_driver, _id, expected):
    a = AccountUC(act_driver)
    result = a.find_user_by_id(_id)
    assert result.name == expected
