"""
Cookbook interface to Database

Interfaces:
* UserInterface -- Interface to be implemented by User* classes.

Implementations:
* UserMongo -- User class that interacts with MongoDB.
"""

import abc
import datetime

import pyrecipe.storage as db
from pyrecipe.cookbook import Recipe


##############################################################################
# Interfaces
##############################################################################


class UserInterface(metaclass=abc.ABCMeta):
    """Class for interacting with the PyRecipe Database User Collection."""

    @abc.abstractmethod
    def update_user_data(self, data: dict) -> int:
        """
        Updates a user's data.

        User.update_user_data(self, data)

        :param data: (dict) data fields to change.
            i.e. {"name": "Bob", "email": "newAddress@here.com"}
        :returns: (int) total number of successfully changed fields.
            i.e. 2 for the above example
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe) -> int:
        """
        Adds a recipe reference to the user's recipes.

        User.add_recipe(self, recipe)

        :param recipe: (Recipe) an instance of a cookbook.Recipe class.
        :returns: (int) 1 for success, 0 if unsuccessful.
        """
        raise NotImplementedError


##############################################################################
# Implementations
##############################################################################


class UserMongo(UserInterface):
    """
    Each Instance will hold a user's data from the database.

    PARAMS:
    :param name: (str) lookup user by name, OR
    :param email: (str) lookup user by email address.

    ATTRIBUTES:
    :attr name: (str) the user's name.
    :attr email: (str) the user's email address.
    :attr created: (datetime) date the user was created.
    :attr recipes: (list(Recipe)) list of recipe's owned by user.
    :attr view: (str) default recipe view [list, grid].
    :attr page_size: (str) max number of recipes to display before paginating.
    :attr email_distros: (dict) email distros for emailing recipes to.
        i.e. {"family": "email1, email2, email3"}
    :attr _id: (str) user id in the database.

    METHODS:
    """

    def __init__(self, name=None, email=None):
        self._user = db.User.objects().filter(name=name).first()
        if self._user:
            print("Found user: {}, {}".format(self._user.name, self._user.email))

        self._id = str(self._user.id)

    def update_user_data(self, data: dict) -> int:
        """
        Update user: name, email, view, page_size, email_distros

        user.update_user_data(data)

        :param data: (dict) data fields to change.
            i.e. {"name": "Bob", "email": "newAddress@here.com"}
        :returns: (int) total number of successfully changed fields.
            i.e. 2 for the above example
        """
        count = 0
        for key, val in data.items():
            if key in ("name", "email", "view", "page_size", "email_distros"):
                setattr(self._user, key, val)
                count += 1
        self._user.save()
        self._user = self._refresh_user()
        return count

    def add_recipe(self, recipe: Recipe) -> int:
        """
        Adds a recipe reference to the user's recipes.

        user.add_recipe(recipe)

        :param recipe: (Recipe) an instance of a cookbook.Recipe class.
        :returns: (int) 1 for success, 0 if unsuccessful.
        """
        result = self._user.update(add_to_set__recipes=recipe.id)
        if result:
            self._refresh_user()
            return result
        return 0

    def _refresh_user(self) -> db.User:
        """
        Ensure user information is refreshed after saving/updating to the DB.

        user._refresh_user()

        :returns: (db.User) refreshed user document after updating the DB.
        """
        return db.User.objects().filter(id=self._id).first()
