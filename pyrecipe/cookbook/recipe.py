"""
cookbook.recipe interface to Database

Interfaces:
* RecipeInterface -- Interface to be implemented by Recipe* classes.

Implementations:
* RecipeMongo -- Recipe class that interacts with MongoDB.
"""

import abc
import datetime
from typing import List

import pyrecipe.storage as db


##############################################################################
# Interfaces
##############################################################################


class RecipeInterface(metaclass=abc.ABCMeta):
    """Class for interacting with the PyRecipe Database Recipe Collection."""

    @classmethod
    @abc.abstractmethod
    def create_recipe(cls, name:str, ingredients:list, directions:list) -> 'Recipe':
        """
        Create a new Recipe and insert it into the DB.

        Recipe.create_recipe(name, ingredients, directions)

        :param name: (str) the name of the recipe
        :param ingredients: (list(dict)) list of ingredients, where each ingredient
            is a dict of the form {'name':'olive oil', 'quantity': '1', 'unit': 'tbsp'}
        :param directions: (list) ordered list of strings for each line of the directions.
            i.e. ['boil water', 'add rice', 'reduce heat']
        """

    @classmethod
    @abc.abstractmethod
    def fetch_recipe(cls, name:str) -> 'Recipe':
        """
        Fetch a recipe by name.

        Recipe.fetc_recipe(name)

        :param name: (str) the name of the recipe
        :returns: (Recipe) the Recipe instance or None
        """

    @abc.abstractmethod
    def copy_recipe(self, recipe:'Recipe') -> 'Recipe':
        """
        Given a Recipe instance, produce a copy of it with a modified name

        :param recipe: (Recipe) the Recipe instance to copy
        :returns: a Recipe instance with a modified name
            i.e. recipe.name = 'lasagna_COPY'
        """

    @abc.abstractmethod
    def update_recipe_data(self, data:dict) -> int:
        """
        Update a Recipe instance's given attribute.

        :param data: (dict) key=val to change
            i.e. {'name': 'lasagna'}
        :returns: (int) number of successfully changed attributes
        """


    @abc.abstractmethod
    def delete_recipe(self) -> int:
        """
        Given a recipe instance, set the deleted attribute=True

        :returns: (int) 1 for success, 0 for failure
        """

    @abc.abstractmethod
    def restore_recipe(self) -> int:
        """
        Given a recipe instance, set the deleted attribute=False

        :returns: (int) 1 for success, 0 for failure
        """

    @abc.abstractmethod
    def add_tag(self, tag:str) -> int:
        """
        Given a recipe instance, add a new tag

        :returns: (int) 1 for success, 0 for failure
        """

    @abc.abstractmethod
    def delete_tag(self, tag:str) -> int:
        """
        Given a recipe instance, delete a new tag

        :returns: (int) 1 for success, 0 for failure
        """

##############################################################################
# Implementations
##############################################################################


class RecipeMongo(RecipeInterface):
    """
    Each Instance will hold a recipe's data from the database.

    PARAMS:
    :param db_recipe: (db.User) an instance from the DB's recipe collection.

    ATTRIBUTES/PROPERTIES:
    :attr name: (str) name of the recipe.
    :attr ingredients: (list) list of ingredients.
    :attr num_ingredients: (int) total number of discrete ingredients.
    :attr directions: (list) ordered list of cooking instructions.
    :attr prep_time: (float) total # minutes to prep recipe.
    :attr cook_time: (float) total # minutes to cook recipe.
    :attr tags: (list) list of tags given
    :attr pictures: (list) list of filepaths for pictures in recipe.
    :attr notes: (list) list of strings for recipe notes.
    :attr rating: (int) rating of recipe, if given, [0.0 - 5.0] in .5 increments.
    :attr favorite: (bool) recipe tagged as favorite.
    :attr deleted: (bool) recipe marked deleted?
    :attr created_date: (datetime) UTC time of when recipe was created.
    :attr last_modified_date: (datetime) UTC time of when recipe was last modified.

    TODO:
    * modify update_user_data to use property.setters
    * test recipe creation so multiple recipes cannot exist with same name
      i.e. raise RecipeCreationError
    """

    def __init__(self, db_recipe=None):
        self._recipe = db_recipe

    @classmethod
    def create_recipe(cls, name:str, ingredients:list, directions:dict) -> 'Recipe':
        # see RecipeInterface docstring
        _recipe = db.Recipe()
        _recipe.name = name.lower()

        _recipe.ingredients = []
        for ingredient in ingredients:
            i = db.Ingredient()
            i.name = ingredient['name'].lower()
            i.quantity = ingredient['quantity'].lower()
            i.unit = ingredient['unit'].lower()
            _recipe.ingredients.append(i)

        _recipe.directions = directions
        _recipe.num_ingredients = len(_recipe.ingredients)
        _recipe.save()
        return cls(_recipe)

    @classmethod
    def fetch_recipe(cls, name:str) -> 'Recipe':
        # see RecipeInterface docstring
        _recipe = db.Recipe.objects().filter(name=name).first()
        if not _recipe:
            return None
        return cls(_recipe)

    @classmethod
    def copy_recipe(cls, recipe:'Recipe') -> 'Recipe':
        # see RecipeInterface docstring
        _recipe = db.Recipe()
        _recipe.name = recipe.name + "_COPY"
        _recipe.ingredients = recipe.ingredients
        _recipe.directions = recipe.directions
        _recipe.tags = recipe.tags
        _recipe.pictures = recipe.pictures
        _recipe.notes = recipe.notes
        _recipe.rating = recipe.rating
        _recipe.favorite = recipe.favorite
        _recipe.save()
        return cls(_recipe)

    def update_recipe_data(self, data:dict) -> int:
        # see RecipeInterface docstring
        count = 0
        for key, val in data.items():
            if key in ("name", "prep_time", "cook_time", "tags", "pictures", "notes", "rating", "favorite"):
                setattr(self._recipe, key, val)
                count += 1
            elif key in ("ingredients"):
                setattr(self._recipe, key, val)
                self._recipe.num_ingredients = len(val)
                count += 1
        self._recipe.save()
        self._update_last_mod_date()
        self._recipe = self._refresh_recipe()
        return count


    def delete_recipe(self) -> int:
        # see RecipeInterface docstring
        result = self._recipe.update(deleted=True)
        self._update_last_mod_date()
        self._recipe = self._refresh_recipe()
        return result


    def restore_recipe(self) -> int:
        # see RecipeInterface docstring
        result = self._recipe.update(deleted=False)
        self._update_last_mod_date()
        self._recipe = self._refresh_recipe()
        return result

    def add_tag(self, tag:str) -> int:
        # see RecipeInterface docstring
        result = self._recipe.update(add_to_set__tags=tag.lower())
        self._update_last_mod_date()
        self._recipe = self._refresh_recipe()
        return result

    def delete_tag(self, tag:str) -> int:
        # see RecipeInterface docstring
        result = self._recipe.update(pull__tags=tag.lower())
        self._update_last_mod_date()
        self._recipe = self._refresh_recipe()
        return result

    @property
    def _id(self) -> str:
        return self._recipe._id

    @property
    def name(self) -> str:
        return self._recipe.name

    @property
    def ingredients(self) -> List['Ingredient']:
        return self._recipe.ingredients

    @property
    def num_ingredients(self) -> int:
        return self._recipe.num_ingredients

    @property
    def directions(self) -> List[str]:
        return self._recipe.directions

    @property
    def prep_time(self) -> float:
        return self._recipe.prep_time

    @property
    def cook_time(self) -> float:
        return self._recipe.cook_time

    @property
    def tags(self) -> List['tags']:
        return self._recipe.tags

    @property
    def pictures(self) -> List['filepaths']:
        return self._recipe.pictures

    @property
    def notes(self) -> List[str]:
        return self._recipe.notes

    @property
    def rating(self) -> float:
        return self._recipe.rating

    @property
    def favorite(self) -> bool:
        return self._recipe.favorite

    @property
    def deleted(self) -> bool:
        return self._recipe.deleted

    @property
    def created_date(self) -> datetime.datetime:
        return self._recipe.created_date

    @property
    def last_modified_date(self) -> datetime.datetime:
        return self._recipe.last_modified_date

    def _refresh_recipe(self) -> db.Recipe:
        """
        Ensure recipe information is refreshed after saving/updating to the DB.

        recipe._refresh_user()

        :returns: (db.Recipe) refreshed recipe document after updating the DB.
        """
        return db.Recipe.objects().filter(id=self._id).first()

    def _update_last_mod_date(self) -> int:
        """
        Updates the recipe's "last_updated_date" attribute in the DB.

        recipe._update_last_mod_date()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        result = self._recipe.update(last_modified_date=datetime.datetime.utcnow())
        return result
