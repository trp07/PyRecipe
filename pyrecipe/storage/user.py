"""
ODM for MongoDB

* User -- DB representation of User instance.
"""

import datetime
from typing import List, Optional

import mongoengine
import werkzeug.security as ws
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from pyrecipe.errors import UserNotFoundError, UserLoginError
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
    :param view: (str) default recipe view [list, grid].
    :param page_size: (int) max number of recipes to display before paginating.
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
    view = mongoengine.StringField(default="list")
    page_size = mongoengine.IntField(default=100, min_val=10)
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
    def create_user(name: str, email: str, password: str) -> "User":
        """
        Create and return the user.

        user = User.create_user(name, email, password)

        :param name: (str) the user's name.
        :param email: (str) the user's email address.
        :param password: (str) the user's password.
        :returns: (User) the user or None if user email already in use.
        """
        if User.find_user_by_email(email):
            return None
        user = User()
        user.name = name
        user.username = name
        user.email = email
        user.password_hash = User._hash_text(password)
        user.save()
        return user

    @staticmethod
    def find_user_by_id(user_id: str) -> Optional["User"]:
        """
        Check to see if a user with that user_id exists.

        user = User.find_user_by_id(user_id)

        :param user_id: (str) the user's id number.
        :returns: (User) the user or None.
        """
        user = User.objects().filter(id=user_id).first()
        return user

    @staticmethod
    def find_user_by_email(email: str) -> Optional["User"]:
        """
        Check to see if user with email address already exists.

        user = User.find_user_by_email(email)

        :param email: (str) the user's email address.
        :returns: (User) the user or None.
        """
        user = User.objects().filter(email=email).first()
        return user

    @staticmethod
    def login_user(email: str, password: str) -> Optional["User"]:
        """
        Logs in and returns the user.

        user = User.login_user(email, password)

        :param email: (str) the user's email address.
        :param password: (str) the supplied password.
        :returns: (User) the user.  None if user doesn't exist.
        :raises: UserNotFoundError if user with email doesn't exist.
        """
        user = User.find_user_by_email(email)
        if not user:
            return None
        if not User._verify_hash(user.password_hash, password):
            return None
        return user

    @staticmethod
    def list_users() -> List["User"]:
        """
        Returns a list of all Users.

        User.list_users()

        :returns: list(User)
        """
        return list(User.objects())

    @staticmethod
    def user_id_to_int(text) -> int:
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
        self.reload()
        return result

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

    def set_password(self, password: str) -> str:
        """
        Sets password_hash as the hash of the user's password and reloads
        the DB instance.

        user.set_password('p@ssw0rd')

        :returns: (str) the hash of the provided password
        """
        password_hash = User._hash_text(password)
        if self.id:
            self.update(password_hash=password_hash)
            self.reload()
        else:
            self.password_hash = password_hash
        return password_hash

    @staticmethod
    def _verify_hash(hashed_text: str, plain_text: str) -> bool:
        """
        Checks the supplied password's hash against the one stored in the DB.

        User._verify_hash(password_hash, password)

        :returns: (bool) True for a good match, False otherwise
        """
        return crypto.verify(plain_text, hashed_text)

    @staticmethod
    def _hash_text(text: str) -> str:
        """
        Hash the given text.

        hashed = User._hash_text(text)

        :param text: (str) the text to hash.
        :returns: (str) the hash of the supplied text.
        """
        hashed_text = crypto.encrypt(text, rounds=121547)
        return hashed_text
