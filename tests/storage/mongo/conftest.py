"""Fixtures for various test modules."""

import datetime

import pytest
import mongoengine

from pyrecipe.storage.mongo.image import Image
from pyrecipe.storage.mongo.ingredient import Ingredient
from pyrecipe.storage.mongo.recipe import Recipe
from pyrecipe.storage.mongo.user import User


@pytest.fixture(scope="session")
def mongodb(request):
    """
    Initialize a mocked mongodb instance using "mongomock".
    This will have session scope to use the same DB connection for all tests
    that require the DB.
    """
    db = mongoengine.connect(
        db="pyrecipe_testing", alias="core", host="mongomock://localhost"
    )
    yield db
    # db.drop_database("pyrecipe_testing")
    mongoengine.disconnect()


@pytest.fixture(scope="function")
def recipes(mongodb, ingredients, image):
    """Return two recipes for testing.  Delete upon test completion."""
    recipe_1 = Recipe()
    recipe_1.name = "spam and eggs"
    recipe_1.ingredients = ingredients
    recipe_1.num_ingredients = 2
    recipe_1.directions = ["fry eggs", "add spam", "eat"]
    recipe_1.prep_time = 10
    recipe_1.cook_time = 5
    recipe_1.servings = 1
    recipe_1.tags = ["breakfast", "fast"]
    recipe_1.images = [image]
    recipe_1.save()

    recipe_2 = Recipe()
    recipe_2.name = "spam and oatmeal"
    recipe_2.ingredients = ingredients
    recipe_2.num_ingredients = 2
    recipe_2.directions = ["microwave oatmeal", "add spam"]
    recipe_2.tags = ["breakfast", "slow"]
    recipe_2.save()

    yield [recipe_1, recipe_2]
    recipe_1.delete()
    recipe_2.delete()


@pytest.fixture(scope="function")
def ingredients(mongodb):
    """Return two ingredients."""
    ingredient_1 = Ingredient()
    ingredient_1.name = "garlic"
    ingredient_1.quantity = "1"
    ingredient_1.unit = "clove"
    ingredient_1.preparation = "minced"

    ingredient_2 = Ingredient()
    ingredient_2.name = "onion"
    ingredient_2.quantity = "1"
    ingredient_2.unit = "large"
    ingredient_2.preparation = "chopped"

    return [ingredient_1, ingredient_2]


@pytest.fixture(scope="function")
def image(mongodb):
    """Return Image data."""
    image = Image()
    image.recipe_id = "123456"
    image.filepath = "/path/to/image"
    image.description = "caption for image"
    return image


@pytest.fixture(scope="function")
def users(mongodb):
    """Return two users for testing.  Delete upon test completion."""
    user_1 = User()
    user_1.name = "King Arthur"
    user_1.username = "kingarthur"
    user_1.email = "kingarthur@mail.com"
    user_1.password_hash = "123456abcdef"
    user_1.save()

    user_2 = User()
    user_2.name = "Black Knight"
    user_2.username = "blackknight"
    user_2.email = "blackknight@mail.com"
    user_2.password_hash = "123456abcdef"
    user_2.save()

    yield [user_1, user_2]
    user_1.delete()
    user_2.delete()
