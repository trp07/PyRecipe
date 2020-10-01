import hashlib
from unittest.mock import MagicMock

import pytest
import flask

from pyrecipe.security import cookie_auth


def test_set_auth(mocker):
    """
    GIVEN an http request
    WHEN setting the cookie
    THEN assert it is set in the proper format
    """
    response = MagicMock()
    response.set_cookie.return_value = None
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    cookie_auth.set_auth(response, "12345", "pyrecipe", "salt")
    response.set_cookie.assert_called_with("pyrecipe", "12345:test")


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


def test_user_id_via_auth_cookie_good(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with good parameters
    THEN assert the correct user_id is returned
    """
    request = MagicMock()
    request.cookies = {"pyrecipe_dev": "12345:test"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    result = cookie_auth.get_user_id_via_auth_cookie(request, "pyrecipe_dev", "salt")
    assert result == "12345"


def test_user_id_via_auth_cookie_badcookiename(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with a cookiename not found in the request
    THEN assert None is returned
    """
    request = MagicMock()
    request.cookies = {"pyrecipe_dev": "12345:test"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    result = cookie_auth.get_user_id_via_auth_cookie(request, "bad", "salt")
    assert result is None


def test_user_id_via_auth_cookie_badcookieformat(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with a cookie not in the correct format
    THEN assert None is returned
    """
    request = MagicMock()
    request.cookies = {"pyrecipe_dev": "badformat"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "test"

    result = cookie_auth.get_user_id_via_auth_cookie(request, "pyrecipe_dev", "salt")
    assert result is None


def test_user_id_via_auth_cookie_badhashcheck(mocker):
    """
    GIVEN an http request with a pyrecipe cookie
    WHEN the func is called with a cookie that does not pass the hash check
    THEN assert None is returned
    """
    request = MagicMock()
    request.cookies = {"pyrecipe_dev": "12345:test"}
    hash_mock = mocker.patch.object(cookie_auth, "_hash_text")
    hash_mock.return_value = "something other value"

    result = cookie_auth.get_user_id_via_auth_cookie(request, "pyrecipe_dev", "salt")
    assert result is None


def test_logout():
    """
    GIVEN an http response to logout
    WHEN the func is called
    THEN assert no errors and the correct internals are called
    """
    response = MagicMock()
    response.delete_cookie.return_value = None

    cookie_auth.logout(response, "pyrecipe_dev")
    response.delete_cookie.assert_called_with("pyrecipe_dev")
