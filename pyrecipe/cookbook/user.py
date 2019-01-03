"""
Cookbook interface to Database

Interfaces:
* UserInterface -- Interface to be implemented by User* classes.

Implementations:
* UserMongo -- User class that interacts with MongoDB.
"""

import abc
import datetime
from typing import List

import pyrecipe.storage as db
from .recipe import Recipe
from pyrecipe.errors import UserNotFoundError
from pyrecipe.errors import UserCreationError


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

    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe) -> int:
        """
        Adds a recipe reference to the user's recipes.

        User.add_recipe(self, recipe)

        :param recipe: (Recipe) an instance of a cookbook.Recipe class.
        :returns: (int) 1 for success, 0 if unsuccessful.
        """

    @classmethod
    @abc.abstractmethod
    def create_user(cls, name: str, email: str) -> 'User':
        """
        Create a new User and insert into DB.

        User.create_user(name, email)

        :param name: (str) name of the user.
        :param email: (str) email address of the user.
        :returns: (User) the new user.
        :raises: UserCreationError if a user with the same email address
            already exists.
        """

    @classmethod
    @abc.abstractmethod
    def login_user(cls, name: str, email: str) -> 'User':
        """
        Logs in and returns the user.

        User.login_user()

        :param name: (str) the user's name.
        :param email: (str) the user's email address.
        :returns: (User) the user.
        :raises: UserNotFoundError if user with name and email doesn't
            exist.
        """

    @staticmethod
    @abc.abstractmethod
    def list_users() -> List['User']:
        """
        Returns a list of all Users.

        User.list_users()

        :returns: list(User)
        """



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
    :attr created_date: (datetime) date the user was created.
    :attr last_modified_date: (datetime) date the user was last modified.
    :attr recipes: (list(Recipe)) list of recipe's owned by user.
    :attr view: (str) default recipe view [list, grid].
    :attr page_size: (str) max number of recipes to display before paginating.
    :attr email_distros: (dict) email distros for emailing recipes to.
        i.e. {"family": "email1, email2, email3"}
    :attr _id: (str) user id in the database.
    """

    def __init__(self, user=None):
        self._user = user

    @classmethod
    def create_user(cls, name:str=None, email:str=None) -> 'User':
        # see UserInterface docstring.
        if db.User.objects().filter(email=email).count():
            raise UserCreationError(email=email)
        _user = db.User()
        _user.name = name
        _user.email = email
        _user.save()
        return cls(_user)


    @classmethod
    def login_user(cls, name: str, email: str) -> 'User':
        # see UserInterface docstring.
        _user = db.User.objects().filter(name=name, email=email).first()
        if not _user:
            raise UserNotFoundError(name)
        return cls(_user)

    @staticmethod
    def list_users() -> List['User']:
        # see UserInterface docstring.
        users = db.User.objects()
        return list(users)

    @property
    def _id(self):
        return str(self._user.id)

    @property
    def name(self):
        return self._user.name

    @property
    def email(self):
        return self._user.email

    @property
    def created_date(self):
        return self._user.created_date

    @property
    def last_modified_date(self):
        return self._user.last_modified_date

    @property
    def recipes(self):
        return self._user.recipes

    @property
    def view(self):
        return self._user.view

    @property
    def page_size(self):
        return self._user.page_size

    @property
    def email_distros(self):
        return self._user.email_distros

    def update_user_data(self, data: dict) -> int:
        # see UserInterface docstring.
        count = 0
        for key, val in data.items():
            if key in ("name", "email", "view", "page_size", "email_distros"):
                setattr(self._user, key, val)
                count += 1
        self._user.save()
        self._update_last_mod_date()
        self._user = self._refresh_user()
        return count

    def add_recipe(self, recipe: Recipe) -> int:
        # see UserInterface docstring.
        result = self._user.update(add_to_set__recipes=recipe.id)
        if result:
            self._update_last_mod_date()
            self._user = self._refresh_user()
        return result

    def _refresh_user(self) -> db.User:
        """
        Ensure user information is refreshed after saving/updating to the DB.

        user._refresh_user()

        :returns: (db.User) refreshed user document after updating the DB.
        """
        return db.User.objects().filter(id=self._id).first()

    def _update_last_mod_date(self) -> int:
        """
        Updates the user's "last_updated_date" attribute in the DB.

        user._update_last_mod_date()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        result = self._user.update(last_modified_date=datetime.datetime.utcnow())
        return result
