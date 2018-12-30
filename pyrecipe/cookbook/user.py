"""
Cookbook interface to Database

* User -- Python representation of a User in the Database
"""

import abc


class User(metaclass=abc.ABCMeta):
    """Class for interacting with the PyRecipe Database User Collection."""

    @abc.abstractmethod
    def update_user_data(self, data: dict) -> int:
        """
        User.update_user_data(self, data)

        :param data: (dict) data fields to change.
            i.e. {"name": "Bob", "email": "newAddress@here.com"}
        :returns: (int) total number of successfully changed fields.
            i.e. 2 for the above example
        """
        raise NotImplementedError
