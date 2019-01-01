"""
Tests for the pyrecipe.cookbook.user.py module.

"get_user" is a fixture defined in conftest.py
"""

import datetime

import pytest

from pyrecipe.cookbook.user import UserMongo as User
from pyrecipe.cookbook.user import db
from pyrecipe.errors import UserNotFoundError


def test_user_init(get_user, mocker):
    """
    GIVEN a User instance
    WHEN instantiated
    THEN assert it is correctly created
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    user = User()
    assert user._id == '123'
    assert user.name == 'Tester'
    assert user.email == 'tester@here.com'
    assert isinstance(user.created_date, datetime.datetime)
    assert isinstance(user.last_modified_date, datetime.datetime)
    assert user.recipes == []
    assert user.view == 'list'
    assert user.page_size == 100
    assert user.email_distros == {}


def test_user_init_raisesExc(mocker):
    """
    GIVEN a User instance
    WHEN instantiated but not located in the DB
    THEN assert UserNotFoundError exception is raised
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = None

    with pytest.raises(UserNotFoundError):
        user = User()


def test_update_user_data(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user.udpate_user_data(dict) is called
    THEN assert correct calls are made and correct count is returned
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    update_mock = mocker.patch.object(User, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(User, '_refresh_user')

    user = User()

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
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    update_mock = mocker.patch.object(User, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(User, '_refresh_user')

    user = User()

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
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    update_mock = mocker.patch.object(User, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(User, '_refresh_user')

    user = User()

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

    user = User()
    result = user._refresh_user()
    assert result.__class__.__name__ == 'Fake_User'


def test_update_last_mod_date(get_user, mocker):
    """
    GIVEN a User instance
    WHEN user._update_last_mod_date is called and successfully entered in DB
    THEN assert return=1
    """
    db_mock = mocker.patch.object(db, 'User')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_user

    user = User()
    result = user._update_last_mod_date()
    assert result == 1
