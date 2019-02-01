"""Fixtures for various test modules."""

import datetime

import pytest
import mongoengine

from pyrecipe.storage import Recipe
from pyrecipe.storage import Ingredient
from pyrecipe.storage import User


@pytest.fixture(scope='session')
def mongodb(request):
    """
    Initialize the mongodb pyrecipe_tester collection for required tests.
    This will have session scope to use the same DB connection for all tests
    that require the DB.
    """
    db = mongoengine.connect(db='pyrecipe_tester', alias='core', host='mongodb://localhost')
    yield db
    db.close()


@pytest.fixture(scope="function")
def recipe_setup(mongodb):
    """
    Fixture to get the DB up and return a recipe.  Delete
    the recipe upon test completion.
    """
    db = mongodb
    recipe = Recipe()
    yield recipe
    recipe.delete()


@pytest.fixture(scope='function')
def get_ingredients():
    ingredient = Ingredient()
    ingredient.name = 'test ingredient'
    ingredient.quantity = '1'
    ingredient.unit = 'tsp'
    return ingredient


@pytest.fixture(scope='function')
def user_setup(mongodb):
    """
    Fixture to get the DB up and return a user.  Delete
    the user upon test completion.
    """
    db = mongodb
    user = User()
    yield user
    user.delete()
