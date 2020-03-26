"""Use Cases for account-related logic."""

from typing import Optional
from pyrecipe.storage import User


def login_user(email: str, password: str) -> Optional[User]:
    """
    Login the user and return their DB instance.

    Returns the user from the DB or None if no user exists or
    the password is incorrect.
    """
    user = User.login_user(email, password)
    return user


def register_user(name: str, email: str, password: str) -> Optional[User]:
    """
    Create a new user upon registration.

    Returns the new user instance or None if the user with the
    same email address already exists.
    """
    user = User.create_user(name, email, password)
    return user


def find_user_by_id(user_id: str) -> Optional[User]:
    """
    Get the user object by the supplied user_id.

    Returns the user object or None if the user doesn't exist.
    """
    user = User.find_user_by_id(user_id)
    return user
