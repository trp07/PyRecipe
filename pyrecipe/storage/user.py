"""
ODM for MongoDB

* User -- DB representation of User instance.
"""

import datetime
import uuid

import mongoengine

from .recipe import Recipe


class User(mongoengine.Document):
    """
    ODM Class that maps to the Users collection in MongoDB.  Each user will have a
    reference to a recipe that is added.

    REQUIRED params:
    N/A

    NOT-REQUIRED params:
    :param name: (str) name of the user, defaults to a UUID4 unless specified.
    :param email: (str) email address of the user.
    :param auth: (hash) hash of password (NOT IMPLEMENTED).
    :param created: (datetime) defaults to UTC time of when user is created.
    :param recipes: (list(Recipe)) add a reference to a Recipe.
    :param view: (str) default recipe view [list, grid].
    :param page_size: (int) max number of recipes to display before paginating.
    :param email_distros: (dict) email distros for emailing recipes to.
        i.e. {"family": "email1, email2, email3"}
    """

    name = mongoengine.StringField(default=lambda: str(uuid.uuid4()))
    email = mongoengine.StringField(required=False)
    auth = mongoengine.StringField(default="Not Implemented")
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    recipes = mongoengine.ListField(field=mongoengine.ReferenceField(Recipe))
    view = mongoengine.StringField(default="list")
    page_size = mongoengine.IntField(default=100, min_val=10)
    email_distros = mongoengine.MapField(
        field=mongoengine.StringField(), required=False
    )

    meta = {"db_alias": "core", "collection": "users"}
