"""
ODM for MongoDB

* User -- DB representation of User instance.
"""

import datetime
from typing import List, Optional

import mongoengine

from .recipe import Recipe


class User(mongoengine.Document):
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

    @staticmethod
    def user_id_to_int(text: str) -> int:
        """
        Returns the User._id as an integer.

        User.user_id_to_int(idnum)

        :param text: (str) the text to convert.
        :returns: int of the user id or 0 if unable.
        """
        try:
            return int(str(text), 16)
        except:
            return 0

    def _update_last_mod_date(self) -> int:
        """
        Updates the user's "last_updated_date" attribute in the DB.

        user._update_last_mod_date()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        result = self.update(last_modified_date=datetime.datetime.utcnow())
        self.reload()
        return result

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
