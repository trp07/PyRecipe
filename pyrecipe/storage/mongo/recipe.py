"""ODM for MongoDB Recipe Collection."""

import datetime

import mongoengine

from .shared import BaseDocument


class Recipe(BaseDocument):
    """
    ODM Class that maps to the Recipes collection in MongoDB.

    REQUIRED params:
    :param name: (str) name of the recipe.
    :param ingredients: (list) list of ingredients, an embedded document.
    :param num_ingredients: (int) total number of discrete ingredients.
        i.e. len(ingredients)
    :param directions: (list) ordered list of cooking directions.
        i.e. ['boil water', 'add rice', 'reduce heat']

    NOT-REQUIRED params:
    :param prep_time: (float) time to prep recipe in minutes.
    :param cook_time: (float) time to cook recipe in minutes.
    :param servings: (int) number of servings in the recipe.
    :param tags: (list) descriptive tags for a recipe.
        i.e. ['bbq', 'vegetarian']
    :param images: (list filepath for an uploaded image.
    :param notes: (list) list of notes about the recipe.
        i.e. "Substitute butter for ghee if you don't have ghee."
    :param rating: (float) user rating of recipe with 0.5 increments [0.0-5.0]
    :param favorite: (bool) user selected as a favorite.
    :param when_made: list(dates) list of dates the recipe was made by the user.
    :param deleted: (bool) user selected recipe for deletion.
    :param created_date: (datetime) defaults to UTC time of when recipe is created.
    :param last_modified_date: (datetime) UTC time of when recipe is last modified.
    """

    name = mongoengine.StringField(required=True)
    num_ingredients = mongoengine.IntField(required=True, min_val=1)
    directions = mongoengine.ListField(field=mongoengine.StringField(), required=True)
    ingredients = mongoengine.ListField(field=mongoengine.StringField(), required=True)

    prep_time = mongoengine.FloatField(default=0, min_val=0.0)
    cook_time = mongoengine.FloatField(default=0, min_val=0.0)
    servings = mongoengine.IntField(default=0, min_val=1)
    tags = mongoengine.ListField(required=False)
    images = mongoengine.ListField(field=mongoengine.StringField(), required=False)
    notes = mongoengine.ListField(field=mongoengine.StringField(), required=False)
    rating = mongoengine.FloatField(required=False, min_val=0.0, max_val=5.0)
    favorite = mongoengine.BooleanField(default=False)
    when_made = mongoengine.ListField(required=False)
    deleted = mongoengine.BooleanField(default=False)
    created_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    last_modified_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "db_alias": "core",
        "collection": "recipes",
        "indexes": [
            "name",
            "num_ingredients",
            "prep_time",
            "cook_time",
            "servings",
            "tags",
            "rating",
            "favorite",
            "deleted",
            "ingredients",
            "when_made",
            {
                "fields": ["$name", "$ingredients", "$directions", "$tags"],
                "default_language": "english",
                "weights": {"name": 10, "tags": 5, "ingredients": 4, "directions": 2},
            },
        ],
    }

    def __repr__(self):
        """Repr of instance for quick debugging purposes."""
        return "<Recipe: {}>".format(self.name)
