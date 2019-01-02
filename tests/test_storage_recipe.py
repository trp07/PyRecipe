"""
Tests for the pyrecipe.storage.recipe.py module.

"mongodb" is a fixture defined in conftest.py
"""

import datetime

import pytest
import mongoengine

from pyrecipe.storage.recipe import Recipe


def test_recipe_creation_defaults(mongodb):
    """
    GIVEN a mongodb instance
    WHEN a Recipe is added with only required values set, just using default values
        for non-required fields
    THEN assert a correct Recipe is added
    """
    db = mongodb
    r = Recipe()
    r.name = 'Yummy'
    r.ingredients = {'salt': '1 tsp'}
    r.num_ingredients = 1
    r.directions = {'1': 'cook'}
    r.save()

    assert r.name == 'Yummy'
    assert r.ingredients == {'salt': '1 tsp'}
    assert r.num_ingredients == 1
    assert r.tags == []
    assert r.directions == {'1': 'cook'}
    assert r.pictures == []
    assert r.rating is None
    assert r.favorite == False
    assert r.deleted == False
    assert isinstance(r.created_date, datetime.datetime)
    assert isinstance(r.last_modified_date, datetime.datetime)


@pytest.mark.parametrize('name, ingredients, num_ingredients, directions',[
    (None, {'salt': '1 tsp'}, 1, {'1': 'cook'}),
    ('Yummy', None, 1, {'1': 'cook'}),
    ('Yummy', {'salt': '1 tsp'}, None, {'1': 'cook'}),
    ('Yummy', {'salt': '1 tsp'}, 1, None),
])
def test_recipe_creation_raisesExc(name, ingredients, num_ingredients, directions, mongodb):
    """
    GIVEN a mongodb instance
    WHEN a Recipe is added leaving a required field empty
    THEN assert mongoengine.errors.ValidationError is raised
    """
    db = mongodb
    r = Recipe()
    r.name = name
    r.ingredients = ingredients
    r.num_ingredients = num_ingredients
    r.directions = directions
    with pytest.raises(mongoengine.errors.ValidationError):
        r.save()
