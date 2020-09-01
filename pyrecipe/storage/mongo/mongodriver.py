"""Mongo DB Driver to use for all Mongo DB interactions."""

import datetime
from typing import List
from typing import Optional

import mongoengine

from pyrecipe.security import auth
from pyrecipe.storage.shared.db_interface import DBInitInt
from pyrecipe.storage.shared.recipe_interface import RecipeDBInt
from pyrecipe.storage.shared.user_interface import UserDBInt
from pyrecipe.storage.shared.user_model import UserModel
from pyrecipe.storage.shared.recipe_model import RecipeModel

from .recipe import Recipe
from .user import User


class MongoDriver(DBInitInt, RecipeDBInt, UserDBInt):
    """Singleton type class to drive all Mongo DB interactions."""

    #### DBInitInt methods ###################################################

    @staticmethod
    def db_initialize(db_name="pyrecipe", verbose=False) -> None:
        """Create/Register connection with mongodb.  DB name will be 'pyrecipe'."""
        mongoengine.register_connection(alias="core", name=db_name)
        if verbose:
            print("[+] MongoDB connection registered to database: {}".format(db_name))

    #### RecipeDBInt methods #################################################

    @staticmethod
    def _recipe_to_dict(recipe: Recipe) -> dict:
        """Given a mongo Recipe object, return it as a dict."""
        return {
            "_id": str(recipe.id),
            "name": recipe.name,
            "num_ingredients": recipe.num_ingredients,
            "ingredients": recipe.ingredients,
            "directions": recipe.directions,
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "servings": recipe.servings,
            "images": recipe.images,
            "tags": recipe.tags,
            "notes": recipe.notes,
            "rating": recipe.rating,
            "favorite": recipe.favorite,
            "when_made": recipe.when_made,
            "deleted": recipe.deleted,
            "created_date": recipe.created_date,
            "last_modified_date": recipe.last_modified_date,
        }

    @staticmethod
    def recipe_create(
        name: str,
        prep_time: int,
        cook_time: int,
        servings: int,
        ingredients: List["ingredients"],
        directions: List["directions"],
        tags: List["tags"] = [],
        notes: List["notes"] = [],
    ) -> RecipeModel:
        """
        Given the correct parameters, create a recipe.

        r = MongoDriver.recipe_create(**kwargs)

        :returns: Recipe instance and saves it into the DB.
        """
        r = Recipe()
        r.name = name
        r.prep_time = float(prep_time)
        r.cook_time = float(cook_time)
        r.servings = int(servings)
        r.ingredients = ingredients
        r.num_ingredients = len(ingredients)
        r.directions = directions
        r.tags = tags
        r.notes = notes
        r.save()
        return RecipeModel.from_dict(MongoDriver._recipe_to_dict(r))

    @staticmethod
    def recipe_edit(
        _id: str,
        name: str,
        prep_time: int,
        cook_time: int,
        servings: int,
        ingredients: List["ingredients"],
        directions: List["directions"],
        tags: List["tags"] = [],
        notes: List["notes"] = [],
    ) -> RecipeModel:
        """
        Wholescale edit a recipe's information.

        r = MongoDriver.recipe_edit(**kwargs)

        :returns: Recipe instance and saves it into the DB.
        """
        r = Recipe.objects().filter(id=_id).first()
        if r:
            r.update(
                name=name,
                prep_time=prep_time,
                cook_time=cook_time,
                servings=servings,
                ingredients=ingredients,
                directions=directions,
                tags=tags,
                notes=notes,
            )
            r.save()
            return RecipeModel.from_dict(MongoDriver._recipe_to_dict(r))


    @staticmethod
    def recipe_find_by_id(recipe_id: str) -> Optional[RecipeModel]:
        """
        Return the recipe with the given id.

        recipe = MongoDriver.recipe_find_by_id(recipe_id)

        :param recipe_id: (str) the recipe id as a string
        :returns: RecipeModel for the recipe found or None
        """
        r = Recipe.objects().filter(id=recipe_id).first()
        if r:
            return RecipeModel.from_dict(MongoDriver._recipe_to_dict(r))

    @staticmethod
    def recipes_find_by_name(search_string: str) -> Optional[RecipeModel]:
        """
        Returns a match of all recipes for the search_string using a case insensitive
        regex match in the Recipe.name field

        recipes = MongoDriver.recipe_find_by_name("spam")

        :param search_string: (str) string to search.
        :returns: List["RecipeModel"] a list of all recipes that match or None.
        """
        recipes = list(
            Recipe.objects().filter(name__icontains=search_string, deleted=False)
        )
        return [RecipeModel.from_dict(MongoDriver._recipe_to_dict(r)) for r in recipes]

    @staticmethod
    def recipes_find_by_tag(tags: List[str]) -> Optional[RecipeModel]:
        """
        Returns a match of all recipes for with the given tag.

        recipes = MongoDriver.recipe_find_by_tag(["tag1", "tag2"])

        :param tags: List[str] list of strings (tags) to search.
        :returns: List["RecipeModel"] a list of all recipes that match or None.
        """
        tags = [tag.lower() for tag in tags]
        recipes = list(Recipe.objects().filter(tags__all=tags, deleted=False))
        return [RecipeModel.from_dict(MongoDriver._recipe_to_dict(r)) for r in recipes]

    @staticmethod
    def recipes_get_tags() -> List["tags"]:
        """
        Returns a of all distinct tags in the recipe collection.

        recipes = MongoDriver.recipe_get_tags()

        :returns: List["tags"] a list of all distinct tags in the collection.
        """
        return list(Recipe.objects().distinct("tags"))

    @staticmethod
    def recipes_all() -> List[RecipeModel]:
        """
        Get all the recipes currently stored in DB.

        recipes = MongoDriver.recipe_all()

        :returns: List["RecipeModel"] of all recipes.
        """
        recipes = list(Recipe.objects())
        return [RecipeModel.from_dict(MongoDriver._recipe_to_dict(r)) for r in recipes]

    @staticmethod
    def recipes_active() -> List[RecipeModel]:
        """
        Get all the recipes that have not been marked as deleted.

        recipes = MongoDriver.recipe_active()

        :returns: List["RecipeModel"] of all recipes where deleted==False.
        """
        recipes = [r for r in Recipe.objects() if r.deleted == False]
        return [RecipeModel.from_dict(MongoDriver._recipe_to_dict(r)) for r in recipes]

    @staticmethod
    def recipes_deleted() -> Optional[RecipeModel]:
        """
        Get all the recipes that have been marked as deleted.

        recipes = MongoDriver.recipe_deleted()

        :returns: List["RecipeModel"] of all recipes where deleted==True.
        """
        recipes = [r for r in Recipe.objects() if r.deleted == True]
        return [RecipeModel.from_dict(MongoDriver._recipe_to_dict(r)) for r in recipes]

    @staticmethod
    def recipe_copy(recipe: RecipeModel) -> RecipeModel:
        """
        Given a Recipe instance, produce a copy of it with a modified name

        new_recipe = MongoDriver.recipe_copy(recipe)

        :param recipe: (Recipe) the Recipe instance to copy
        :returns: a Recipe instance with a modified name
            i.e. recipe.name = 'lasagna_COPY'
        """
        copy = Recipe()
        copy.name = recipe["name"] + "_COPY"
        copy.num_ingredients = recipe["num_ingredients"]
        copy.ingredients = recipe["ingredients"]
        copy.directions = recipe["directions"]
        copy.prep_time = recipe["prep_time"]
        copy.cook_time = recipe["cook_time"]
        copy.servings = recipe["servings"]
        copy.tags = recipe["tags"]
        copy.notes = recipe["notes"]
        copy.rating = recipe["rating"]
        copy.save()
        return RecipeModel.from_dict(MongoDriver._recipe_to_dict(copy))

    @staticmethod
    def recipe_add_tag(recipe: RecipeModel, tag: str) -> int:
        """
        Given a recipe instance, add a new tag

        MongoDriver.recipe_add_tag(recipe, "tag")

        :returns: (int) 1 for success, 0 for failure
        """
        r = Recipe.objects().filter(id=recipe.id).first()
        result = r.update(add_to_set__tags=tag.lower())
        r._update_last_mod_date()
        return result

    @staticmethod
    def recipe_delete_tag(recipe: RecipeModel, tag: str) -> int:
        """
        Given a recipe instance, delete a new tag

        MongoDriver.recipe_delete_tag(recipe, "tag")

        :returns: (int) 1 for success, 0 for failure
        """
        r = Recipe.objects().filter(id=recipe.id).first()
        result = r.update(pull__tags=tag.lower())
        r._update_last_mod_date()
        return result

    @staticmethod
    def recipe_mark_made(recipe: RecipeModel, date: datetime = None) -> int:
        """
        Add a date the recipe was last made.  This will be a list of
        all dates the recipe is made.

        MongoDriver.recipe_mark_made(recipe, date)

        :returns: (int) for success, 0 for failure or if trying to
            mark_made on the same date more than once.
        """
        if date is None:
            date = datetime.datetime.utcnow()
        r = Recipe.objects().filter(id=recipe.id).first()
        for d in r.when_made:
            day_delta = (d.date() - date.date()).days
            if day_delta == 0:
                return 0

        result = r.update(push__when_made=date)
        r._update_last_mod_date()
        return result

    @staticmethod
    def recipe_delete(recipe: RecipeModel) -> int:
        """
        Given a recipe instance, mark it as deleted

        MongoDriver.recipe_delete(recipe)

        :returns: (int) 1 for success, 0 for failure
        """
        r = Recipe.objects().filter(id=recipe.id).first()
        result = r.update(deleted=True)
        r._update_last_mod_date()
        return result

    #### UserDBInt methods ###################################################

    @staticmethod
    def _user_to_dict(user: User) -> dict:
        """Given a mongo User object, return it as a dict."""
        return {
            "_id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash,
            "created_date": user.created_date,
            "last_modified_date": user.last_modified_date,
            "recipe_ids": user.recipe_ids,
            "shared_recipe_ids": user.shared_recipe_ids,
            "email_distros": user.email_distros,
        }

    @staticmethod
    def user_create(name: str, email: str, password: str) -> Optional["UserModel"]:
        """
        Create and return the user.

        MongoDriver.user_create(name, email, password)

        :param name: (str) the user's name.
        :param email: (str) the user's email address.
        :param password: (str) the user's password.
        :returns: (UserModel) the user or None if user email already in use.
        """
        if User.objects().filter(email=email).first():
            return None
        user = User()
        user.name = name
        user.username = name
        user.email = email
        user.password_hash = auth.hash_password(password)
        user.save()
        return UserModel.from_dict(MongoDriver._user_to_dict(user))

    @staticmethod
    def user_find_by_id(user_id: str) -> Optional["UserModel"]:
        """
        Check to see if a user with that user_id exists.

        MongoDriver.user_find_by_id(user_id)

        :param user_id: (str) the user's id number.
        :returns: (UserModel) the user or None.
        """
        try:
            user = User.objects().filter(id=user_id).first()
        except mongoengine.errors.ValidationError:
            user = None
        if user:
            return UserModel.from_dict(MongoDriver._user_to_dict(user))

    @staticmethod
    def user_login(email: str, password: str) -> Optional["UserModel"]:
        """
        Logs in and returns the user.

        MongoDriver.user_login(email, password)

        :param email: (str) the user's email address.
        :param password: (str) the supplied password.
        :returns: (UserModel) the user.  None if user doesn't exist.
        """
        user = User.objects().filter(email=email).first()
        if not user:
            return None
        if not auth.verify_password(password, user.password_hash):
            return None
        return UserModel.from_dict(MongoDriver._user_to_dict(user))

    @staticmethod
    def user_find_by_email(email: str) -> Optional["UserModel"]:
        """
        Finds the user by email address.

        user = MongoDriver.user_find_by_email(email)

        :param email: (str) the user's email address.
        :returns: (UserModel) the user or None.
        """
        user = User.objects().filter(email=email).first()
        if user:
            return UserModel.from_dict(MongoDriver._user_to_dict(user))

    @staticmethod
    def users_list() -> List["UserModel"]:
        """
        Returns a list of all Users.

        MongoDriver.users_list()

        :returns: list(User)
        """
        users = list(User.objects())
        if users:
            return [
                UserModel.from_dict(MongoDriver._user_to_dict(user)) for user in users
            ]

    @staticmethod
    def user_add_recipe(user: "UserModel", recipe_id: str) -> int:
        """
        Adds a recipe reference to the user's recipes.

        MongoDriver.user_add_recipe(user, recipe_id)

        :param user: (UserModel) a reference to a user
        :param recipe_id: (str) a reference to a recipe.
        :returns: (int) 1 for success, 0 if unsuccessful.
        """
        user = User.objects().filter(id=user.id).first()
        result = user.update(add_to_set__recipe_ids=recipe_id)
        if result:
            user._update_last_mod_date()
        user.reload()
        return result

    @staticmethod
    def user_set_password(user: "UserModel", password: str) -> str:
        """
        Sets password_hash as the hash of the user's password and reloads
        the DB instance.  Can use this method to change user's password.

        MongoDriver.user_set_password(user, 'p@ssw0rd')

        :returns: password hash of the supplied password or None if unsuccesssful.
        """
        u = User.objects().filter(id=user.id).first()
        if u:
            password_hash = auth.hash_password(password)
            u.update(password_hash=password_hash)
            return password_hash
        return None
