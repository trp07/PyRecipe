"""
Custom exceptions module
"""

class UserNotFoundError(Exception):
    """User is not found in the Database."""
    def __init__(self, name):
        self.error = "User <{}> was not found in the Database.".format(name)
        super().__init__(UserNotFoundError, self.error)

