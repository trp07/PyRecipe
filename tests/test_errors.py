"""
Tests for the pyrecipe.errors.custom_exceptions.py module.
"""

import pytest

from pyrecipe.errors.custom_exceptions import UserNotFoundError
from pyrecipe.errors.custom_exceptions import UserCreationError


def test_UserNotFoundError(capsys):
    """
    GIVEN no user with 'Bob' in the DB
    WHEN a UserNotFoundError is triggered
    THEN assert correct output prints
    """
    with pytest.raises(UserNotFoundError):
        raise UserNotFoundError('Bob')
        out, err = capsys.readouterr()
        assert "User <Bob> was not found in the Database." in out


def test_UserCreationErrror_email(capsys):
    """
    GIVEN a reused email address upon user creation
    WHEN a UserCreationError is triggered
    THEN assert correct output prints
    """
    with pytest.raises(UserCreationError):
        raise UserCreationError(email='reused@mail.com')
        out, err = capsys.readouterr()
        assert "Email address <reused@mail.com> used by another user."
