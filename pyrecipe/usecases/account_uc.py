"""Use Cases for account-related logic."""

from typing import Optional


class AccountUC:
    """Class that provides all account-related use cases."""

    def __init__(self, db_driver):
        self._driver = db_driver

    def login_user(self, email: str, password: str) -> Optional["UserModel"]:
        """
        Login the user and return their DB instance.

        Returns the user from the DB or None if no user exists or
        the password is incorrect.
        """
        user = self._driver.user_login(email, password)
        return user


    def register_user(self, name: str, email: str, password: str) -> Optional["UserModel"]:
        """
        Create a new user upon registration.

        Returns the new user instance or None if the user with the
        same email address already exists.
        """
        user = self._driver.user_create(name, email, password)
        return user


    def find_user_by_id(self, user_id: str) -> Optional["User"]:
        """
        Get the user object by the supplied user_id.

        Returns the user object or None if the user doesn't exist.
        """
        user = self._driver.user_find_by_id(user_id)
        return user
