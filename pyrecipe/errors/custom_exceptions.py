"""
Custom exceptions module
"""


class UserNotFoundError(Exception):
    """User is not found in the Database."""

    def __init__(self, name):
        self.error = "User <{}> was not found in the Database.".format(name)
        super().__init__(UserNotFoundError, self.error)


class UserLoginError(ValueError):
    """User Authentication Error."""

    def __init__(self, message):
        self.error = message
        super().__init__(UserLoginError, self.error)


class UserCreationError(ValueError):
    """
    Cannot create user because:
    1.  Email address already in use
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if key == "email":
                self.error = "Email address <{}> used by another user.".format(val)
        super().__init__(UserCreationError, self.error)
