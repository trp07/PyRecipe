import datetime

import pytest

from pyrecipe.storage.shared import UserModel

####### globals #########

DATE = datetime.datetime.utcnow()

USER = {
    "_id": "123456",
    "name": "Tester",
    "username": "tester",
    "email": "tester@mail.com",
    "password_hash": "abcdefg",
    "created_date": DATE,
    "last_modified_date": DATE,
    "recipe_ids": ["1", "2", "3"],
    "shared_recipe_ids": ["4", "5"],
    "email_distros": {"family": ["mom@mail.com", "dad@mail.com"]},
}


###### test funcs #########


def test_usermodel_init():
    """Verifies a UserModel is properly instantiated."""
    user = UserModel(**USER)
    assert user.id == "123456"
    assert user.name == "Tester"
    assert user.username == "tester"
    assert user.email == "tester@mail.com"
    assert user.password_hash == "abcdefg"
    assert user.created_date == DATE
    assert user.last_modified_date == DATE
    assert user.recipe_ids == ["1", "2", "3"]
    assert user.shared_recipe_ids == ["4", "5"]
    assert user.email_distros == {"family": ["mom@mail.com", "dad@mail.com"]}


def test_usermodel_fromdict():
    """Verifies a UserModel is properly instantiated via the
    from_dict() method."""
    user = UserModel.from_dict(USER)
    assert user.id == "123456"
    assert user.name == "Tester"
    assert user.username == "tester"
    assert user.email == "tester@mail.com"
    assert user.password_hash == "abcdefg"
    assert user.created_date == DATE
    assert user.last_modified_date == DATE
    assert user.recipe_ids == ["1", "2", "3"]
    assert user.shared_recipe_ids == ["4", "5"]
    assert user.email_distros == {"family": ["mom@mail.com", "dad@mail.com"]}


def test_usermodel_todict():
    """Verifies a properly formed dict is returned from the
    UserModel.to_dict() method."""
    user = UserModel(**USER)
    user_dict = user.to_dict()
    assert user_dict == USER
