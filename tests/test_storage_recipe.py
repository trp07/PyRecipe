"""
Tests for the pyrecipe.storage.recipe.py module.

Fixtures found in conftest.py
1. mongodb
2. recipe_setup
3. get_ingredients
"""

import datetime

import mongoengine
import pytest

from pyrecipe.storage.recipe import Recipe
from pyrecipe.storage.recipe import Ingredient


def test_recipe_creation_defaults(recipe_setup, get_ingredients):
    """
    GIVEN a mongodb instance
    WHEN a Recipe is added with only required values set, just using default values
        for non-required fields
    THEN assert a correct Recipe is added
    """
    r = recipe_setup
    r.name = 'Yummy'
    r.ingredients = [get_ingredients]
    r.num_ingredients = 1
    r.directions = ['cook']
    r.prep_time = 100
    r.cook_time = 120
    r.servings = 6
    r.save()

    assert r.name == 'Yummy'
    assert isinstance(r.ingredients[0], Ingredient)
    assert r.num_ingredients == 1
    assert r.prep_time == 100
    assert r.cook_time == 120
    assert r.servings == 6
    assert r.tags == []
    assert r.directions == ['cook']
    assert r.pictures == []
    assert r.rating is None
    assert r.favorite == False
    assert r.deleted == False
    assert isinstance(r.created_date, datetime.datetime)
    assert isinstance(r.last_modified_date, datetime.datetime)


def test_recipe_repr(capsys, mongodb):
    """
    GIVEN a mongodb instance
    WHEN repr(recipe) is called on a Recipe instance
    THEN assert the correct output prints
    """
    db = mongodb
    recipe = Recipe.objects().filter().first()
    print(repr(recipe))
    out, err = capsys.readouterr()
    assert "<Recipe: spam musubi>" in out


def test_recipe_find_recipes(mongodb):
    """
    GIVEN a mongodb instance
    WHEN a search query is initiated with Recipe.find_recipes()
    THEN assert the correct number of recipes are returned
    """
    db = mongodb
    search1 = Recipe.find_recipes(search_string="spam")
    search2 = Recipe.find_recipes(search_string="SPAM")
    search3 = Recipe.find_recipes(search_string="egg")

    assert len(search1) == 9
    assert len(search2) == 9
    assert len(search3) == 1


def test_recipe_copy_recipe(mongodb):
    """
    GIVEN a mongodb instance
    WHEN recipe.copy_recipe() is called
    THEN assert a copy is returned with all the correct attributes
    """
    db = mongodb
    recipe = Recipe.objects().filter().first()
    new_recipe = recipe.copy_recipe()

    assert new_recipe.id != recipe.id
    assert new_recipe.name == recipe.name + "_COPY"
    assert new_recipe.num_ingredients == recipe.num_ingredients
    assert new_recipe.ingredients == recipe.ingredients
    assert new_recipe.directions == recipe.directions
    assert new_recipe.prep_time == recipe.prep_time
    assert new_recipe.cook_time == recipe.cook_time
    assert new_recipe.servings == recipe.servings
    assert new_recipe.tags == recipe.tags
    assert new_recipe.pictures == recipe.pictures
    assert new_recipe.notes == recipe.notes
    assert new_recipe.rating == recipe.rating
    assert new_recipe.created_date != recipe.created_date
    assert new_recipe.last_modified_date != recipe.last_modified_date
    new_recipe.delete()


def test_recipe_add_delete_tag(mongodb):
    """
    GIVEN a mongodb instance
    WHEN a tag is added and then deleted
    THEN assert it was added then later deleted
    """
    db = mongodb
    recipe = Recipe.objects().filter().first()

    assert "test_tag" not in recipe.tags

    result = recipe.add_tag("test_tag")
    assert "test_tag" in recipe.tags
    assert result == 1

    result = recipe.delete_tag("test_tag")
    assert "test_tag" not in recipe.tags
    assert result == 1


def test_recipe_update_last_mod_date(mongodb):
    """
    GIVEN a mongodb instance
    WHEN recipe._update_last_mod_date is called
    THEN assert the a new date is inserted
    """
    db = mongodb
    recipe = Recipe.objects().filter().first()

    result = recipe._update_last_mod_date()
    assert result == 1
    assert isinstance(recipe.last_modified_date, datetime.datetime)


def test_recipe_save_goodID(mongodb, mocker):
    """
    GIVEN a mongodb instance
    WHEN recipe.save() is called on an already existing record
    THEN assert the record is saved with an updated modification date
    """
    date_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    recipe = Recipe.objects().filter().first()
    recipe.save()
    assert date_mock.call_count == 1


def test_recipe_save_noID(recipe_setup, get_ingredients, mocker):
    """
    GIVEN a mongodb instance
    WHEN recipe.save() is called on an newly created record
    THEN assert the record is saved without an updated modification date
    """
    date_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    recipe = recipe_setup
    recipe.name = 'test'
    recipe.ingredients = [get_ingredients]
    recipe.num_ingredients = 1
    recipe.directions = ['do a test!']
    recipe.save()
    assert date_mock.call_count == 0
