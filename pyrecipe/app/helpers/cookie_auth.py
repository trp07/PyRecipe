"""Module to create session cookies."""

import hashlib
from datetime import timedelta
from typing import Optional

from flask import Request
from flask import Response

from pyrecipe.storage import User

AUTH_COOKIE_NAME = "pyrecipe_demo_user"


def set_auth(response: Response, user_id: int):
    """Sets the response cookie, placing it into browser headers."""
    hash_val = _hash_text(str(user_id))
    val = "{}:{}".format(user_id, hash_val)
    response.set_cookie(AUTH_COOKIE_NAME, val)


def _hash_text(text: str) -> str:
    """Hash the given text."""
    text = "salty__" + text + "__text"
    return hashlib.sha512(text.encode("utf-8")).hexdigest()


def _add_cookie_callback(_, response: Response, name: str, value: str):
    response.set_cookie(name, value, max_age=timedelta(days=30))


def get_user_id_via_auth_cookie(request: Request) -> Optional[int]:
    """Verifies a cookie is set and the cookie is valid.    """
    if AUTH_COOKIE_NAME not in request.cookies:
        return None

    val = request.cookies[AUTH_COOKIE_NAME]
    parts = val.split(":")
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]
    hash_val_check = _hash_text(user_id)
    if hash_val != hash_val_check:
        print("Warning: Hash mismatch, invalid cookie value")
        return None

    return user_id


def logout(response: Response):
    """Removes the user cookie, logging out the user."""
    response.delete_cookie(AUTH_COOKIE_NAME)
