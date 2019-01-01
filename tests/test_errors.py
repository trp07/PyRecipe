"""
Tests for the pyrecipe.errors.custom_exceptions.py module.
"""

import pytest

from pyrecipe.errors.custom_exceptions import UserNotFoundError


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
