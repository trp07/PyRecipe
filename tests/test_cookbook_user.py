"""
Tests for the pyrecipe.cookbook.user.py module.

"get_user" is a fixture defined in conftest.py
"""

import collections.abc
import datetime

import pytest

from pyrecipe.cookbook.user import UserMongo as User
from pyrecipe.cookbook.user import db
from pyrecipe.errors import UserNotFoundError
from pyrecipe.errors import UserCreationError


def test_user_init(get_user):
    """
    GIVEN a User instance
    WHEN instantiated
    THEN assert it is correctly created
    """
    user = User(get_user)
    assert user._id == '123'
    assert user.name == 'Tester'
    assert user.email == 'tester@here.com'
    assert isinstance(user.created_date, datetime.datetime)
    assert isinstance(user.last_modified_date, datetime.datetime)
    assert user.recipes == []
    assert user.shared_recipes == []
    assert user.view == 'list'
    assert user.page_size == 100
    assert user.email_distros == {}

def test_create_user(get_user, mocker):
    """
    GIVEN a need to create a user
    WHEN User.create_user is called with valid params
    THEN assert a User is returned
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.return_value = get_user
    db_mock.objects.return_value.filter.return_value.count.return_value = 0

    user = User.create_user(name='test', email='fake')
    assert isinstance(user, User)


def test_create_user_raisesExc(mocker):
    """
    GIVEN a need to create a user
    WHEN User.create_user is called with an email address already in use
    THEN assert UserCreationError exception is raised
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.count.return_value = 1

    with pytest.raises(UserCreationError):
        user = User.create_user()

def test_login_user(get_user, mocker):
    """
    GIVEN a need to login a user
    WHEN User.login_user is called with valid params
    THEN assert a User is returned
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    user = User.login_user(email='fake')
    assert isinstance(user, User)

def test_login_user_raisesExc(mocker):
    """
    GIVEN a need to login a user
    WHEN User.login_user is called with valid params but not found in the DB
    THEN assert a UserNotFoundError is raised
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = None

    with pytest.raises(UserNotFoundError):
        user = User.login_user(email='fake')

def test_list_users(mocker):
    """
    GIVEN a need to list all users
    WHEN User.list_users() is called
    THEN assert a list is returned
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value = []

    users = User.list_users()
    assert isinstance(users, collections.abc.MutableSequence)


def test_update_user_data(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user.udpate_user_data(dict) is called
    THEN assert correct calls are made and correct count is returned
    """
    update_mock = mocker.patch.object(User, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(User, '_refresh_user')

    user = User(get_user)

    data = {'name': 'new_name', 'email': 'new_email', 'view': 'new_view',
        'page_size': 'new_page', 'email_distros': 'new_distros'}

    count = user.update_user_data(data)
    assert count == 5
    assert update_mock.call_count == 1
    assert refresh_mock.call_count == 1


def test_add_recipe_successful(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user.add_recipe(Recipe) is called and successfully inserts into the DB
    THEN assert return=1 and correct calls are made
    """
    update_mock = mocker.patch.object(User, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(User, '_refresh_user')

    user = User(get_user)

    class Recipe:
        id = 'good'

    result = user.add_recipe(Recipe())
    assert result == 1
    assert refresh_mock.call_count == 1
    assert update_mock.call_count == 1


def test_add_recipe_unsuccessful(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user.add_recipe(Recipe) is called and unsuccessfully inserts into the DB
    THEN assert return=0 and correct calls are made
    """
    update_mock = mocker.patch.object(User, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(User, '_refresh_user')

    user = User(get_user)

    class Recipe:
        id = 'bad'

    result = user.add_recipe(Recipe())
    assert result == 0
    assert refresh_mock.call_count == 0
    assert update_mock.call_count == 0


def test_refresh_user(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user._refresh_user is called
    THEN assert a user is mocked DB user document is returned
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    user = User(get_user)
    result = user._refresh_user()
    assert result.__class__.__name__ == 'Fake_User'


def test_update_last_mod_date(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user._update_last_mod_date is called and successfully entered in DB
    THEN assert return=1
    """
    user = User(get_user)
    result = user._update_last_mod_date()
    assert result == 1
