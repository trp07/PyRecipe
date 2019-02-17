"""
Tests for the pyrecipe.storage.user.py module.

Fixtures found in conftest.py
1. mongodb
2. user_setup
"""

import datetime

import pytest

from pyrecipe.storage.user import User
from pyrecipe.storage.user import ws
from pyrecipe.storage import Recipe
from pyrecipe.errors import UserNotFoundError
from pyrecipe.errors import UserLoginError


def test_user_creation_specific(user_setup):
    """
    GIVEN a mongodb instance
    WHEN a User is added with no specified values set, just using default values
    THEN assert a correct User is added
    """
    user = user_setup
    user.name = 'Bob'
    user.username = "bobby"
    user.email = 'bob@here.com'
    user.password_hash = 'p@ssw0rd'
    user.view = 'grid'
    user.page_size = '30'
    user.email_distros = {'family': 'mom@there.com'}
    user.save()

    assert user.name == 'Bob'
    assert user.username == 'bobby'
    assert user.email == 'bob@here.com'
    assert user.password_hash == 'p@ssw0rd'
    assert user.view == 'grid'
    assert user.page_size == '30'
    assert user.email_distros == {'family': 'mom@there.com'}


def test_user_repr(capsys, mongodb):
    """
    GIVEN a mongodb instance
    WHEN repr(user) is called on a User instance
    THEN assert the correct output prints
    """
    db = mongodb
    user = User.objects().filter().first()
    print(repr(user))
    out, err = capsys.readouterr()
    assert "<User: king_arthur:kingarthur@mail.com>" in out


def test_user_login_good(mongodb):
    """
    GIVEN a mongodb instance
    WHEN User.login() is called with known-good params
    THEN assert the correct user is returned
    """
    db = mongodb
    user = User.login(email="brian@mail.com", password_hash="fakePasswordHash")
    assert isinstance(user, User)
    assert user.name == "Brian"


def test_user_login_raises_UserNotFoundError(mongodb):
    """
    GIVEN a mongodb instance
    WHEN User.login() is called with a non-existent user email
    THEN assert UserNotFoundError is raised
    """
    db = mongodb
    with pytest.raises(UserNotFoundError):
        user = User.login(email="nobody@mail.com", password_hash="fakePasswordHash")



def test_user_login_raises_UserLoginError(mongodb):
    """
    GIVEN a mongodb instance
    WHEN User.login() is called with an incorrect password_hash
    THEN assert UserLoginError is raised
    """
    db = mongodb
    with pytest.raises(UserLoginError):
        user = User.login(email="kingarthur@mail.com", password_hash="incorrect")



def test_user_list_users(mongodb):
    """
    GIVEN a mongodb instance
    WHEN User.list_users() is called
    THEN assert the proper count is returned
    """
    db = mongodb
    users = User.list_users()
    assert len(users) == 3


def test_user_add_recipe(mongodb, mocker):
    """
    GIVEN a mongodb instance
    WHEN user.add_recipe is called
    THEN assert the recipe is added, _update_last_mod_date is called, and
        the proper return value is returned
    """
    date_mock = mocker.patch.object(User, '_update_last_mod_date')

    db = mongodb
    user = User.objects().filter().first()
    recipe = list(Recipe.objects())[-1]

    num_recipes = len(user.recipe_ids)

    result = user.add_recipe(recipe)
    assert result == 1
    assert len(user.recipe_ids) == num_recipes + 1
    assert date_mock.call_count == 1
    user.recipe_ids.pop()
    assert len(user.recipe_ids) == num_recipes
    user.save()


def test_user_update_last_mod_date(mongodb):
    """
    GIVEN a mongodb instance
    WHEN user._update_last_mod_date is called
    THEN assert the a new date is inserted
    """
    db = mongodb
    user = User.list_users()[0]

    result = user._update_last_mod_date()
    assert result == 1
    assert isinstance(user.last_modified_date, datetime.datetime)


def test_user_save_goodID(mongodb, mocker):
    """
    GIVEN a mongodb instance
    WHEN user.save() is called on an already existing record
    THEN assert the record is saved with an updated modification date
    """
    date_mock = mocker.patch.object(User, '_update_last_mod_date')
    user = User.list_users()[0]
    user.save()
    assert date_mock.call_count == 1


def test_user_save_noID(mongodb, mocker):
    """
    GIVEN a mongodb instance
    WHEN user.save() is called on an newly created record
    THEN assert the record is saved without an updated modification date
    """
    date_mock = mocker.patch.object(User, '_update_last_mod_date')
    user = User()
    user.name = 'test user'
    user.username = 'test_user'
    user.email = 'testuser@mail.com'
    user.password_hash = 'fakePassword'
    user.save()
    assert date_mock.call_count == 0
    user.delete()


def test_user_set_password(mongodb):
    """
    GIVEN a mongodb instance
    WHEN user.set_password() is called
    THEN assert the password hash is saved in the DB instance.
    """
    user = User.objects().filter(name='Black Knight').first()
    user.password_hash = 'fakehash'

    result = user.set_password('p@ssw0rd')
    assert user.password_hash == result
    assert user.password_hash.startswith('pbkdf2:sha256:')

def test_user_check_password(mongodb, mocker):
    """
    GIVEN a mongodb instance
    WHEN user.check_password() is called
    THEN assert a bool is returned
    """
    hash_mock = mocker.patch.object(ws, 'check_password_hash')
    hash_mock.return_value = True

    user = User.objects().filter(name='Black Knight').first()
    result = user.check_password('p@ssw0rd')
    assert result == True

def test_user_load_user(mongodb):
    """
    GIVEN a mongodb instance
    WHEN User.load_user() is called with a known valid user_id
    THEN assert the correct user is returned
    """
    user = User.objects().filter(name='Black Knight').first()
    user_id = str(user.id)

    new_user = User.load_user(user_id)
    assert new_user.name == 'Black Knight'
