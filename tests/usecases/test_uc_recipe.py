"""Test for the usecases/recipe_uc.py module."""

import pytest

from pyrecipe.usecases.recipe_uc import RecipeUC


def test_recipeuc_instantiation(rec_driver):
    """
    GIVEN a DB driver to instantiate in the Use Case
    WHEN instantiating
    THEN assert it is created
    """
    r = RecipeUC(rec_driver)
    assert r._driver is not None


@pytest.mark.parametrize("deleted, expected", [(True, 1), (False, 1), (None, 2)])
def test_get_all_recipes(rec_driver, deleted, expected):
    """
    GIVEN recipes
    WHEN asking for those by deleted=X
    THEN assert the correct # are returned
    """
    r = RecipeUC(rec_driver)
    recipes = r.get_all_recipes(deleted=deleted)
    assert len(recipes) == expected


def test_find_recipe_by_id(rec_driver):
    """
    GIVEN recipes
    WHEN asking for a recipe by it's DB id
    THEN assert it is returned
    """
    r = RecipeUC(rec_driver)
    recipe = r.find_recipe_by_id("123")
    assert recipe.name == "recipe1"


def test_create_recipe(rec_driver):
    """
    GIVEN a recipe to create
    WHEN creating it
    THEN assert it is returned
    """
    r = RecipeUC(rec_driver)
    result = r.create_recipe(
        name="test",
        prep_time=5,
        cook_time=10,
        servings=4,
        ingredients=["garlic", "onion"],
        directions=["make food"],
        tags=["quick", "spicy"],
        notes=["notes"],
    )
    assert result.name == "test"


@pytest.mark.parametrize(
    "tags, expected", [(["spicy"], 2), (["quick"], 1), (["slow"], 1)]
)
def test_find_recipes_by_tags(rec_driver, tags, expected):
    """
    GIVEN recipes in the DB with tags
    WHEN searching by given tag
    THEN assert the correct # are returned
    """
    r = RecipeUC(rec_driver)
    result = r.find_recipes_by_tag(tags)
    assert len(result) == expected


def test_get_tags(rec_driver):
    r = RecipeUC(rec_driver)
    result = r.get_tags()
    assert len(result) == 3
    for tag in ["spicy", "slow", "quick"]:
        assert tag in result
