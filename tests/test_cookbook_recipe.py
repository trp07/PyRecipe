"""
Tests for the pyrecipe.cookbook.recipe.py module.

"get_recipe" is a fixture defined in conftest.py
"get_ingredient" is a fixture defined in conftest.py
"""

import collections.abc
import datetime

import pytest

from pyrecipe.cookbook.recipe import RecipeMongo as Recipe
from pyrecipe.cookbook.recipe import db


def test_recipe_init(get_recipe):
    """
    GIVEN a Recipe instance
    WHEN instantiated
    THEN assert it is correctly created
    """
    recipe = Recipe(get_recipe)
    assert recipe._id == "123"
    assert recipe.name == "Test_Rec"
    assert isinstance(recipe.ingredients, collections.abc.MutableSequence)
    assert recipe.num_ingredients == 2
    assert recipe.directions == ['cook']
    assert recipe.prep_time == 100.0
    assert recipe.cook_time == 110.0
    assert recipe.servings == 6
    assert recipe.tags == ['tag1', 'tag2']
    assert recipe.pictures == ['filepath1']
    assert recipe.notes == ['test note']
    assert recipe.rating == 4.5
    assert recipe.favorite == True
    assert recipe.deleted == False
    assert isinstance(recipe.created_date, datetime.datetime)
    assert isinstance(recipe.last_modified_date, datetime.datetime)


def test_create_recipe(get_recipe, get_ingredient, mocker):
    """
    GIVEN a need to create a Recipe
    WHEN Recipe.create_recipe is called with valid params
    THEN assert a Recipe is returned
    """
    db_rec_mock = mocker.patch.object(db, 'Recipe')
    db_rec_mock.return_value = get_recipe

    db_igr_mock = mocker.patch.object(db, 'Ingredient')
    db_igr_mock.return_value = get_ingredient

    name = 'TESTER'
    ingredients = [{'name': 'TEST', 'quantity': '1', 'unit': 'TSP'}]
    directions = ['Cook']

    recipe = Recipe.create_recipe(name, ingredients, directions)
    assert isinstance(recipe, Recipe)
    assert recipe.name == 'tester'
    assert recipe.ingredients[0].name == 'test'
    assert recipe.ingredients[0].quantity == '1'
    assert recipe.ingredients[0].unit == 'tsp'
    assert recipe.num_ingredients == 1
    assert recipe.directions == ['Cook']


def test_fetch_recipe_exists(get_recipe, mocker):
    """
    GIVEN a need to fetch a recipe by name
    WHEN Recipe.fetch_recipe is called with an existing recipe.name
    THEN assert a Recipe is returned
    """
    db_mock = mocker.patch.object(db, 'Recipe')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_recipe

    recipe = Recipe.fetch_recipe(name='test')
    assert isinstance(recipe, Recipe)



def test_fetch_recipe_NOTexists(get_recipe, mocker):
    """
    GIVEN a need to fetch a recipe by name
    WHEN Recipe.fetch_recipe is called with a non-existing recipe.name
    THEN assert None is returned
    """
    db_mock = mocker.patch.object(db, 'Recipe')
    db_mock.objects.return_value.filter.return_value.first.return_value = None

    recipe = Recipe.fetch_recipe(name='test')
    assert recipe is None


def test_copy_recipe(get_recipe, mocker):
    """
    GIVEN a need to copy a recipe
    WHEN Recipe.copy_recipe is called with a recipe instance
    THEN assert a copy is returned with a new name
    """
    db_mock = mocker.patch.object(db, 'Recipe')
    db_mock.return_value = get_recipe

    rec_to_copy = get_recipe
    rec_to_copy.name = 'unique name'

    recipe = Recipe.copy_recipe(rec_to_copy)
    assert isinstance(recipe, Recipe)
    assert recipe.name == 'unique name_COPY'
    assert recipe.ingredients == rec_to_copy.ingredients
    assert recipe.directions == rec_to_copy.directions
    assert recipe.prep_time == rec_to_copy.prep_time
    assert recipe.cook_time == rec_to_copy.cook_time
    assert recipe.servings == rec_to_copy.servings
    assert recipe.tags == rec_to_copy.tags
    assert recipe.pictures == rec_to_copy.pictures
    assert recipe.notes == rec_to_copy.notes
    assert recipe.rating == rec_to_copy.rating
    assert recipe.favorite == rec_to_copy.favorite


@pytest.mark.parametrize('attr, value', [
    ('name', 'new_name'),
    ('prep_time', 105.0),
    ('cook_time', 110.0),
    ('tags', ['t1']),
    ('pictures', ['path1']),
    ('notes', ['note1']),
    ('rating', 3.5),
    ('favorite', False),
    ('ingredients', ['ingredient']),
])
def test_update_recipe_data(get_recipe, attr, value, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe.update_recipe_data is called with a valid data dict
    THEN assert correct return value is returned
    """
    update_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(Recipe, '_refresh_recipe')

    recipe = Recipe(get_recipe)

    result = recipe.update_recipe_data({attr: value})
    assert result == 1
    assert update_mock.call_count == 1
    assert refresh_mock.call_count == 1


def test_delete_recipe(get_recipe, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe.delete_recipe is called
    THEN assert it is set to deleted and 1 is returned
    """
    update_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(Recipe, '_refresh_recipe')

    recipe = Recipe(get_recipe)

    result = recipe.delete_recipe()
    assert result == 1
    #assert recipe.deleted == True
    assert update_mock.call_count == 1
    assert refresh_mock.call_count == 1


def test_restore_recipe(get_recipe, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe.restore_recipe is called
    THEN assert it is set to deleted and 1 is returned
    """
    update_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(Recipe, '_refresh_recipe')

    recipe = Recipe(get_recipe)

    result = recipe.restore_recipe()
    assert result == 1
    #assert recipe.deleted == False
    assert update_mock.call_count == 1
    assert refresh_mock.call_count == 1


def test_add_tag(get_recipe, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe.add_tag is called
    THEN assert it is added and 1 is returned
    """
    update_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(Recipe, '_refresh_recipe')

    recipe = Recipe(get_recipe)

    result = recipe.add_tag('good')
    assert result == 1
    #assert 'good' in recipe.tags
    assert update_mock.call_count == 1
    assert refresh_mock.call_count == 1


def test_delete_tag(get_recipe, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe.delete_tag is called
    THEN assert it is removed and 1 is returned
    """
    update_mock = mocker.patch.object(Recipe, '_update_last_mod_date')
    refresh_mock = mocker.patch.object(Recipe, '_refresh_recipe')

    recipe = Recipe(get_recipe)

    result = recipe.delete_tag('good')
    assert result == 1
    #assert 'good' not in recipe.tags
    assert update_mock.call_count == 1
    assert refresh_mock.call_count == 1


def test_refresh_recipe(get_recipe, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe._refresh_recipe is called
    THEN assert a mocked DB recipe document is returned
    """
    db_mock = mocker.patch.object(db, 'Recipe')
    db_mock.objects.return_value.filter.return_value.first.return_value = get_recipe

    recipe = Recipe(get_recipe)

    result = recipe._refresh_recipe()
    assert result.__class__.__name__ == 'Fake_Recipe'


def test_update_last_mod_date(get_recipe, mocker):
    """
    GIVEN a Recipe instance
    WHEN recipe._update_last_mod_date is called and successfully entered in DB
    THEN assert return=1
    """
    recipe = Recipe(get_recipe)
    result = recipe._update_last_mod_date()
    assert result == 1
