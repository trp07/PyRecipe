"""ODM for MongoDB User Collection."""

import datetime

import mongoengine

from .recipe import Recipe
from .shared import BaseDocument


class User(BaseDocument):
    """
    ODM Class that maps to the Users collection in MongoDB.  Each user will have a
    reference to a recipe that is added.

    REQUIRED params:
    :param name: (str) name of the user.
    :param username: (str) username of the user.
    :param email: (str) email address of the user.
    :param password_hash: (str) hash of password.

    NOT-REQUIRED params:
    :param created_date: (datetime) defaults to UTC time of when user is created.
    :param last_modified_date: (datetime) UTC time of when user is last modified.
    :param recipe_ids: (list(Recipe)) recipe ids that user owns/created.
    :param shared_recipe_ids: (list(Recipe)) recipe ids that are shared with user.
    :param email_distros: (dict) email distros for emailing recipes to.
        i.e. {"family": "email1, email2, email3"}

    TODO:
      * only allow one entry per username/email, so multiple users
        don't have same login credentials.
        Raise an Error is user creation is attempted with a username/email
        already in use.
    """

    name = mongoengine.StringField(required=True)
    username = mongoengine.StringField(required=True, unique=True)
    email = mongoengine.StringField(required=True, unique=True)
    password_hash = mongoengine.StringField(required=True)
    created_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    last_modified_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    recipe_ids = mongoengine.ListField(
        field=mongoengine.ReferenceField(Recipe), required=False
    )
    shared_recipe_ids = mongoengine.ListField(
        field=mongoengine.ReferenceField(Recipe), required=False
    )
    email_distros = mongoengine.MapField(
        field=mongoengine.StringField(), required=False
    )

    meta = {
        "db_alias": "core",
        "collection": "users",
        "indexes": ["name", "email", "username", "recipe_ids"],
    }

    def __repr__(self):
        """Repr of instance for quick debugging purposes."""
        return "<User: {}:{}>".format(self.username, self.email)
