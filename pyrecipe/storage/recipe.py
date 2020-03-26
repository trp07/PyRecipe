"""
ODM for MongoDB

* Recipe -- DB representation of Recipe instance.
"""

import datetime
from typing import List
from typing import Optional

import mongoengine

from .ingredient import Ingredient
from .image import Image


class Recipe(mongoengine.Document):
    """
    ODM Class that maps to the Recipes collection in MongoDB.

    REQUIRED params:
    :param name: (str) name of the recipe.
    :param ingredients: (list(Ingredient)) list of ingredients, an embedded document.
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
    :param images: (list(dict)) filepath and description for an uploaded image.
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

    prep_time = mongoengine.FloatField(default=0, min_val=0.0)
    cook_time = mongoengine.FloatField(default=0, min_val=0.0)
    servings = mongoengine.IntField(default=0, min_val=1)
    tags = mongoengine.ListField(required=False)
    notes = mongoengine.ListField(field=mongoengine.StringField(), required=False)
    rating = mongoengine.FloatField(required=False, min_val=0.0, max_val=5.0)
    favorite = mongoengine.BooleanField(default=False)
    when_made = mongoengine.ListField(required=False)
    deleted = mongoengine.BooleanField(default=False)
    created_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    last_modified_date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    ingredients = mongoengine.EmbeddedDocumentListField(Ingredient, required=True)
    images = mongoengine.EmbeddedDocumentListField(Image, required=False)

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
            "ingredients.name",
            "when_made",
        ],
    }

    def __repr__(self):
        """Repr of instance for quick debugging purposes."""
        return "<Recipe: {}>".format(self.name)

    @staticmethod
    def create_recipe(
        name: str,
        prep_time: int,
        cook_time: int,
        servings: int,
        ingredients: List["ingredients"],
        directions: List["directions"],
        tags: List["tags"] = [],
        notes: List["notes"] = [],
    ) -> "Recipe":
        """
        Given the correct parameters, create a recipe.

        r = Recipe.create_recipe(**kwargs)

        :returns: Recipe instance and saves it into the DB.
        """
        r = Recipe()
        r.name = name

        r.prep_time = float(prep_time)
        r.cook_time = float(cook_time)
        r.servings = int(servings)

        igrs = []
        for i in ingredients:
            igr = Ingredient.create_ingredient(
                i.name, i.quantity, i.unit, i.preparation
            )
            igrs.append(igr)
        r.num_ingredients = len(igrs)
        r.ingredients = igrs

        r.directions = directions
        r.tags = tags
        r.notes = notes

        r.save()
        return r

    @staticmethod
    def find_recipe_by_id(recipe_id: str) -> Optional["Recipe"]:
        """Return the recipe with the given id."""
        return Recipe.objects().filter(id=recipe_id).first()

    @staticmethod
    def find_recipes_by_name(search_string: str) -> Optional["Recipe"]:
        """
        Returns a match of all recipes for the search_string using a case insensitive
        regex match in the Recipe.name field

        recipes = Recipe.find_recipes_by_name("spam")

        :param search_string: (str) string to search.
        :returns: List["Recipe"] a list of all recipes that match or None.
        """
        recipes = Recipe.objects().filter(name__icontains=search_string, deleted=False)
        return list(recipes)

    @staticmethod
    def find_recipes_by_tag(tags: List[str]) -> Optional["Recipe"]:
        """
        Returns a match of all recipes for with the given tag.

        recipes = Recipe.find_recipes_by_tag(["tag1", "tag2"])

        :param tags: List[str] list of strings (tags) to search.
        :returns: List["Recipe"] a list of all recipes that match or None.
        """
        tags = [tag.lower() for tag in tags]
        recipes = Recipe.objects().filter(tags__all=tags, deleted=False)
        return list(recipes)

    @staticmethod
    def get_tags() -> List["tags"]:
        """
        Returns a of all distinct tags in the recipe collection.

        recipes = Recipe.get_tags()

        :returns: List["tags"] a list of all distinct tags in the collection.
        """
        return list(Recipe.objects().distinct("tags"))

    @staticmethod
    def active_recipes(deleted=None) -> List["Recipe"]:
        """
        Get all the recipes that have not been marked as deleted.

        recipes = Recipe.all_recipes()

        :returns: List["Recipe"] of all recipes where deleted==False.
        """
        result = [r for r in Recipe.objects() if r.deleted == False]
        return result

    @staticmethod
    def deleted_recipes() -> Optional["Recipe"]:
        """
        Get all the recipes that have been marked as deleted.

        recipes = Recipe.deleted_recipes()

        :returns: List["Recipe"] of all recipes where deleted==True.
        """
        result = [r for r in Recipe.objects() if r.deleted == True]
        return result

    def copy_recipe(self) -> "Recipe":
        """
        Given a Recipe instance, produce a copy of it with a modified name

        new_recipe = recipe.copy_recipe()

        :param recipe: (Recipe) the Recipe instance to copy
        :returns: a Recipe instance with a modified name
            i.e. recipe.name = 'lasagna_COPY'
        """
        recipe = Recipe()
        recipe.name = self.name + "_COPY"
        recipe.num_ingredients = self.num_ingredients
        recipe.ingredients = self.ingredients
        recipe.directions = self.directions
        recipe.prep_time = self.prep_time
        recipe.cook_time = self.cook_time
        recipe.servings = self.servings
        recipe.tags = self.tags
        recipe.pictures = self.pictures
        recipe.notes = self.notes
        recipe.rating = self.rating
        recipe.save()
        return recipe

    def add_tag(self, tag: str) -> int:
        """
        Given a recipe instance, add a new tag

        recipe.add_tag("tag")

        :returns: (int) 1 for success, 0 for failure
        """
        result = self.update(add_to_set__tags=tag.lower())
        self._update_last_mod_date()
        return result

    def delete_tag(self, tag: str) -> int:
        """
        Given a recipe instance, delete a new tag

        recipe.delete_tag("tag")

        :returns: (int) 1 for success, 0 for failure
        """
        result = self.update(pull__tags=tag.lower())
        self._update_last_mod_date()
        return result

    def mark_made(self, date: datetime = datetime.datetime.utcnow()) -> int:
        """
        Add a date the recipe was last made.  This will be a list of
        all dates the recipe is made.

        recipe.mark_made(date)

        :returns: (int) for success, 0 for failure or if trying to
            mark_made on the same date more than once.
        """
        for d in self.when_made:
            day_delta = (d.date() - date.date()).days
            if day_delta == 0:
                return 0

        result = self.update(push__when_made=date)
        self._update_last_mod_date()
        return result

    def delete_recipe(self) -> int:
        """
        Given a recipe instance, mark it as deleted

        recipe.delete_recipe("tag")

        :returns: (int) 1 for success, 0 for failure
        """
        result = self.update(deleted=True)
        self._update_last_mod_date()
        return result

    def _update_last_mod_date(self) -> int:
        """
        Updates the recipe's "last_updated_date" attribute in the DB.

        recipe._update_last_mod_date()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        result = self.update(last_modified_date=datetime.datetime.utcnow())
        self.reload()
        return result

    def save(self) -> int:
        """
        Save the recipe's current state in the DB.  First refreshes the last
        modified date if it's already a DB record, before delegating to the
        built-in/inherited save() method.

        recipe.save()

        :returns: (int) 1 for success, 0 if unsuccessful
        """
        if self.id:
            self._update_last_mod_date()
        return super().save()
