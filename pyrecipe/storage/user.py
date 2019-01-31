"""
ODM for MongoDB

* User -- DB representation of User instance.
"""

import datetime
import uuid
from typing import List

import mongoengine

from pyrecipe.errors import UserNotFoundError, UserLoginError
from .recipe import Recipe


class User(mongoengine.Document):
    """
    ODM Class that maps to the Users collection in MongoDB.  Each user will have a
    reference to a recipe that is added.

    REQUIRED params:
    N/A

    NOT-REQUIRED params:
    :param name: (str) name of the user, defaults to a UUID4 unless specified.
    :param username: (str) username of the user, defaults to a UUID4 unless specified.
    :param email: (str) email address of the user.
    :param password_hash: (str) hash of password (NOT IMPLEMENTED).
    :param created_date: (datetime) defaults to UTC time of when user is created.
    :param last_modified_date: (datetime) UTC time of when user is last modified.
    :param recipe_ids: (list(Recipe)) recipe ids that user owns/created.
    :param shared_recipe_ids: (list(Recipe)) recipe ids that are shared with user.
    :param view: (str) default recipe view [list, grid].
    :param page_size: (int) max number of recipes to display before paginating.
    :param email_distros: (dict) email distros for emailing recipes to.
        i.e. {"family": "email1, email2, email3"}
    """

    name = mongoengine.StringField(default=lambda: str(uuid.uuid4()))
    username = mongoengine.StringField(default=lambda: str(uuid.uuid4()))
    email = mongoengine.StringField(required=False)
    password_hash = mongoengine.StringField(default="Not Implemented")
    created_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    last_modified_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    recipe_ids = mongoengine.ListField(
        field=mongoengine.ReferenceField(Recipe), required=False
    )
    shared_recipe_ids = mongoengine.ListField(
        field=mongoengine.ReferenceField(Recipe), required=False
    )
    view = mongoengine.StringField(default="list")
    page_size = mongoengine.IntField(default=100, min_val=10)
    email_distros = mongoengine.MapField(
        field=mongoengine.StringField(), required=False
    )

    meta = {"db_alias": "core", "collection": "users", "indexes": ["name", "email"]}


    def __repr__(self):
        """Repr of instance for quick debugging purposes."""
        return "<User: {}:{}>".format(self.username, self.email)


    @staticmethod
    def login(email:str, password_hash:str) -> "User":
        """
        Logs in and returns the user.

        user = User.login()

        :param email: (str) the user's email address.
        :param password_hash: (str) the hash of the supplied password.
        :returns: (User) the user.
        :raises: UserNotFoundError if user with email doesn't exist.
        """
        user = User.objects().filter(email=email).first()
        if not user:
            raise UserNotFoundError(email)
        if password_hash != user.password_hash:
            raise UserLoginError('incorrect password')
        return user


    @staticmethod
    def list_users() -> List["User"]:
        """
        Returns a list of all Users.

        User.list_users()

        :returns: list(User)
        """
        return list(User.objects())


    def add_recipe(self, recipe: Recipe) -> int:
        """
        Adds a recipe reference to the user's recipes.

        user.add_recipe(self, recipe)

        :param recipe: (Recipe) an instance of a storage.Recipe class.
        :returns: (int) 1 for success, 0 if unsuccessful.
        """
        result = self.update(add_to_set__recipe_ids=recipe.id)
        if result:
            self._update_last_mod_date()
        return result


    def _update_last_mod_date(self) -> int:
        """
        Updates the user's "last_updated_date" attribute in the DB.

        user._update_last_mod_date()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        return self.update(last_modified_date=datetime.datetime.utcnow())


    def save(self) -> int:
        """
        Save the user's current state in the DB.  First refreshes the last
        modified date if it's already a DB instance, before delegating to the
        built-in/inherited save() method.

        user.save()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        if self.id:
            self._update_last_mod_date()
        return super().save()
