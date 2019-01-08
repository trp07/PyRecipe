"""
Tests for the pyrecipe.storage.user.py module.

"mongodb" is a fixture defined in conftest.py
"""

import datetime

import pytest
import mongoengine

from pyrecipe.storage.user import User


def test_user_creation_defaults(mongodb):
    """
    GIVEN a mongodb instance
    WHEN a User is added with no specified values set, just using default values
    THEN assert a correct User is added
    """
    db = mongodb
    user = User()
    user.save()

    assert isinstance(user.name, str)
    assert user.email is None
    assert user.auth == 'Not Implemented'
    assert isinstance(user.created_date, datetime.datetime)
    assert isinstance(user.last_modified_date, datetime.datetime)
    assert user.recipe_ids == []
    assert user.shared_recipe_ids == []
    assert user.view == 'list'
    assert user.page_size == 100
    assert user.email_distros == dict()


def test_user_creation_specific(mongodb):
    """
    GIVEN a mongodb instance
    WHEN a User is added with no specified values set, just using default values
    THEN assert a correct User is added
    """
    db = mongodb
    user = User()
    user.name = 'Bob'
    user.email = 'bob@here.com'
    user.auth = 'p@ssw0rd'
    user.view = 'grid'
    user.page_size = '30'
    user.email_distros = {'family': 'mom@there.com'}
    user.save()

    assert user.name == 'Bob'
    assert user.email == 'bob@here.com'
    assert user.auth == 'p@ssw0rd'
    assert user.view == 'grid'
    assert user.page_size == '30'
    assert user.email_distros == {'family': 'mom@there.com'}
