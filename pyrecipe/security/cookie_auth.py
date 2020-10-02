"""Module to create session cookies."""

import hashlib
from datetime import timedelta
from enum import Enum
from typing import Optional

from secure import SecureCookie


class Framework(Enum):
    """Enum for supported frameworks so this module
    can be reused in other apps."""
    COOKIE = SecureCookie()
    FLASK = COOKIE.flask



def set_auth(response: "Response", user_id: int, cookiename: str, salt: str) -> None:
    """
    Sets the response cookie, placing it into browser headers.

    :response: (Response) http response object from webframework
    :user_id: (int) the user's database id
    :cookiename: (str) the name the cookie will get set to in the browser, likely
        the app's name
    :salt: (str) a random string to salt the resultant cookie's hash
    """
    hash_val = _hash_text(str(user_id), salt)
    val = "{}:{}".format(user_id, hash_val)
    Framework.FLASK(response, name=cookiename, value=val)



def _hash_text(text: str, salt: str) -> str:
    """Hash the given text."""
    salted = text + salt
    return hashlib.sha512(salted.encode("utf-8")).hexdigest()


def get_user_id_via_auth_cookie(request: "Request", cookiename: str, salt: str) -> Optional[int]:
    """
    Verifies a cookie is set and the cookie is valid.

    :response: (Response) http response object from webframework
    :cookiename: (str) the name the cookie will get set to in the browser, likely
        the app's name
    :salt: (str) a random string to salt the resultant cookie's hash
    """
    if cookiename not in request.cookies:
        return None

    val = request.cookies[cookiename]
    parts = val.split(":")
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]
    hash_val_check = _hash_text(user_id, salt)
    if hash_val != hash_val_check:
        return None

    return user_id


def logout(response: "Response", cookiename: str) -> None:
    """Removes the user cookie, logging out the user."""
    response.delete_cookie(cookiename)
