"""Fixtures for the pyrecipe/app/views module."""

import sys
import os

import pytest

from pyrecipe.app import app as flask_app


class TestUser:
    def __init__(self, email, password, name):
        self.name, self.email, self.password = name, email, password
        self.id = "12345"

class TestRecipe:
    def __init__(self, name, prep_time, cook_time, servings, ingredients,
        directions, notes, tags):
        self.name = name
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.ingredients = ingredients
        self.directions = directions
        self.notes = notes
        self.tags = tags
        self.images = []
        self.id = "12345"
        self._id = self.id


@pytest.fixture(scope="function")
def testuser():
    """Returns a dummy test user for testing."""
    def _user(email, password, name="dude"):
        return TestUser(email, password, name)
    yield _user


@pytest.fixture(scope="function")
def testrecipe():
    """Returns a dummy recipe for testing."""
    def _recipe(name, prep_time, cook_time, servings, ingredients, directions, notes, tags):
        return TestRecipe(name, prep_time, cook_time, servings, ingredients, directions, notes, tags)
    yield _recipe


@pytest.fixture(scope="function")
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    # noinspection PyBroadException,PyUnusedLocal
    try:
        pyrecipe.app.app.register_blueprints()
    except Exception as x:
        # print(x)
        pass

    yield client
