"""
ODM for MongoDB

* Recipe -- DB representation of Recipe instance.
"""

import datetime

import mongoengine

from .ingredient import Ingredient


class Recipe(mongoengine.Document):
    """
    ODM Class that maps to the Recipes collection in MongoDB.

    REQUIRED params:
    :param name: (str) name of the recipe.
    :param ingredients: (list(Ingredient)) list of ingredients, an embedded document.
    :param num_ingredients: (int) total number of discrete ingredients.
        i.e. len(ingredients)
    :param directions: (dict) key=step number (str), value=direction (str).
        i.e. {'1': 'bring water to a boil'}

    NOT-REQUIRED params:
    :param tags: (list) descriptive tags for a recipe.
        i.e. ['bbq', 'vegetarian']
    :param pictures: (list) local filepath for a picture uploaded.
    :param notes: (list) list of notes about the recipe.
        i.e. "Substitute butter for ghee if you don't have ghee."
    :param rating: (int) user rating of recipe with 0.5 increments [0.0-5.0]
    :param favorite: (bool) user selected as a favorite.
    :param deleted: (bool) user selected recipe for deletion.
    :param created_date: (datetime) defaults to UTC time of when recipe is created.
    :param last_modified_date: (datetime) UTC time of when recipe is last modified.
    """

    name = mongoengine.StringField(required=True)
    num_ingredients = mongoengine.IntField(required=True, min_val=1)
    tags = mongoengine.ListField(required=False)
    directions = mongoengine.MapField(field=mongoengine.StringField(), required=True)
    pictures = mongoengine.ListField(field=mongoengine.StringField(), required=False)
    notes = mongoengine.ListField(field=mongoengine.StringField(), required=False)
    rating = mongoengine.FloatField(required=False, min_val=0.0, max_val=5.0)
    favorite = mongoengine.BooleanField(default=False)
    deleted = mongoengine.BooleanField(default=False)
    created_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    last_modified_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    ingredients = mongoengine.EmbeddedDocumentListField(Ingredient, required=True)

    meta = {
        "db_alias": "core",
        "collection": "recipes",
        "indexes": [
            "name",
            "num_ingredients",
            "tags",
            "favorite",
            "deleted",
            "ingredients.name",
        ]
    }
