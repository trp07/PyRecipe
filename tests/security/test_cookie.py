import hashlib
from unittest.mock import MagicMock

import pytest

from pyrecipe.security import cookie_auth


def test_get_auth_cookie(mocker):
    """
    GIVEN an http request
    WHEN setting the cookie
    THEN assert it is set in the proper format
    """
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    result = cookie_auth.get_auth_cookie(user_id="12345", salt="salt")
    assert result == "12345:test"


def test_hash_text():
    """
    GIVEN a text and salt to hash
    WHEN calling the func with the params
    THEN assert the correct result is returned
    """
    text = "test"
    salt = "12345"
    expected = hashlib.sha512((text + salt).encode("utf-8")).hexdigest()
    result = cookie_auth._hash_text(text, salt)
    assert result == expected


def test_user_id_from_cookie_good(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with good parameters
    THEN assert the correct user_id is returned
    """
    #request = MagicMock()
    #request.cookies = {"pyrecipe_dev": "12345:test"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    result = cookie_auth.get_user_id_from_cookie("12345:test", "salt")
    assert result == "12345"


def test_user_id_from_cookie_badcookieformat(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with a cookie not in the correct format
    THEN assert None is returned
    """
    #request = MagicMock()
    #request.cookies = {"pyrecipe_dev": "badformat"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    result = cookie_auth.get_user_id_from_cookie("badformat", "salt")
    assert result is None


def test_user_id_from_cookie_badhashcheck(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with a cookie that does not pass the hash check
    THEN assert None is returned
    """
    #request = MagicMock()
    #request.cookies = {"pyrecipe_dev": "12345:test"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "something other value"

    result = cookie_auth.get_user_id_from_cookie("12345:test", "salt")
    assert result is None

