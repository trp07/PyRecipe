"""Test for the usecases/recipe_uc.py module."""

import builtins
import datetime
import uuid
from unittest.mock import Mock

import pytest

import requests

import pyrecipe.usecases.recipe_uc as ruc
from pyrecipe.usecases.recipe_uc import RecipeUC
from pyrecipe.services import export


def test_recipeuc_instantiation():
    """
    GIVEN a DB driver to instantiate in the Use Case
    WHEN instantiating
    THEN assert it is created
    """
    r = RecipeUC(Mock())
    assert r._driver is not None


@pytest.mark.parametrize("deleted, expected", [(False,[1,0,0]), (True,[0,1,0]), (None,[0,0,1])])
def test_get_all_recipes(deleted, expected):
    """
    GIVEN recipes
    WHEN asking for those by deleted=X
    THEN assert the correct db functions are called
    """
    r = RecipeUC(Mock())
    recipes = r.get_all_recipes(deleted=deleted)
    assert r._driver.recipes_active.call_count == expected[0]
    assert r._driver.recipes_deleted.call_count == expected[1]
    assert r._driver.recipes_all.call_count == expected[2]


def test_find_recipe_by_id():
    """
    GIVEN recipes
    WHEN asking for a recipe by it's DB id
    THEN assert then assert the DB calls are made
    """
    class Recipe:
        images = ["testimg.jpg"]

    r = RecipeUC(Mock())
    r._driver.recipe_find_by_id.return_value = Recipe()

    recipe = r.find_recipe_by_id("123")
    assert recipe is not None
    assert recipe.images == ["../../static/img/recipe_images/testimg.jpg"]


def test_create_recipe(mocker):
    """
    GIVEN a recipe to create
    WHEN creating it
    THEN assert the correct sequence of events occur
    """
    r = RecipeUC(Mock())
    proc_img_mock = mocker.patch.object(ruc, "process_image")

    recipe = r.create_recipe(
        name="test",
        prep_time=5,
        cook_time=10,
        servings=4,
        ingredients=["garlic", "onion"],
        directions=["make food"],
        tags=["quick", "spicy"],
        notes=["notes"],
        images=["imagefile1.jpg", "imagefile2.jpg"],
    )
    assert proc_img_mock.call_count == 2
    assert r._driver.recipe_create.call_count == 1


def test_edit_recipe():
    """
    GIVEN a recipe to edit
    WHEN submitting new attributes
    THEN assert the correct sequence of events occur
    """
    r = RecipeUC(Mock())
    result = r.edit_recipe(
        _id=123,
        name="Newtest",
        prep_time=5,
        cook_time=10,
        servings=4,
        ingredients=["garlic", "onion"],
        directions=["make food"],
        tags=["quick", "spicy"],
        notes=["notes"],
    )
    assert r._driver.recipe_edit.call_count == 1


def test_find_recipes_by_tags():
    """
    GIVEN recipes in the DB with tags
    WHEN searching by given tag
    THEN assert the correct DB call is made
    """
    r = RecipeUC(Mock())
    result = r.find_recipes_by_tag(["tag1", "tag2"])
    assert r._driver.recipes_find_by_tag.call_count == 1


def test_get_tags():
    """
    GIVEN a db with recipes
    WHEN requesting all discrete tags in all recipes
    THEN assert the correct DB call is made
    """
    r = RecipeUC(Mock())
    result = r.get_tags()
    assert r._driver.recipes_get_tags.call_count == 1


def test_delete_recipe():
    """
    GIVEN a db with recipes
    WHEN requesting to delete a specific recipe
    THEN assert 1 is returned
    """
    r = RecipeUC(Mock())
    r._driver.recipe_delete.return_value = 1
    result = r.delete_recipe(recipe_id=123)
    assert result == 1


def test_recipes_search():
    """
    GIVEN a db with recipes
    WHEN the user supplies a search string
    THEN assert the correct DB calls are made and combined upon return
    """
    r = RecipeUC(Mock())
    r._driver.recipes_find_by_name.return_value = ["test_recipe"]
    r._driver.recipes_search.return_value = ["testing_recipe"]
    result = r.recipes_search("test")
    assert result == ["test_recipe", "testing_recipe"]


def test_export_recipe_fileDoesNotExist(mocker):
    """
    GIVEN a recipe in the DB
    WHEN the user requests to export the recipe for the first time
    THEN assert the correct functions are called
    """
    r = RecipeUC(Mock())
    find_mock = mocker.patch.object(r, "find_recipe_by_id")
    date_mock = mocker.patch.object(datetime, "datetime")
    date_mock.strftime.return_value = "filename"
    export_mock = mocker.patch.object(export, "export_to_pdf")
    export_mock.return_value = "/path/to/file"
    result = r.export_recipe("12345")
    assert result == "/path/to/file"
    assert find_mock.call_count == 1
    assert export_mock.call_count == 1


def test_export_recipe_fileAlreadyExists(mocker):
    """
    GIVEN a recipe in the DB
    WHEN the user requests to export the recipe for a already existing file
    THEN assert the correct functions are called but no pdf is recreated
    """
    r = RecipeUC(Mock())
    find_mock = mocker.patch.object(r, "find_recipe_by_id")
    date_mock = mocker.patch.object(datetime, "datetime")
    date_mock.strftime.return_value = "filename"
    file_mock = mocker.patch.object(ruc, "EXPORTDIR")
    file_mock.joinpath.return_value.is_file.return_value = True
    export_mock = mocker.patch.object(export, "export_to_pdf")
    export_mock.return_value = "/path/to/file"
    result = r.export_recipe("12345")
    assert r.find_recipe_by_id.call_count == 1
    assert export_mock.call_count == 0


def test_import_recipe_from_url(mocker):
    """
    GIVEN a recipe to import via url
    WHEN the url imported
    THEN assert it is sent to the database
    """
    r = RecipeUC(Mock())
    import_mock = mocker.patch.object(ruc, "import_from_url")
    import_mock.return_value = {
        "images": "path_to_an_image"
    }
    save_image_mock = mocker.patch.object(r, "_save_image")
    save_image_mock.return_value = "filename"
    create_mock = mocker.patch.object(r, "create_recipe")

    result = r.import_recipe_from_url("url")
    assert import_mock.call_count == 1
    assert save_image_mock.call_count == 1
    assert create_mock.call_count == 1


def test_save_image(mocker):
    """
    GIVEN a url-imported recipe with an image url in the data dict
    WHEN importing
    THEN assert the file is also downloaded and saved
    """
    r = RecipeUC(Mock())
    req_mock = mocker.patch.object(requests, "get")
    req_mock.return_value.content.return_value = "imagedata"
    uuid_mock = mocker.patch.object(uuid, "uuid4")
    uuid_mock.return_value = "12345"
    file_mock = mocker.patch.object(builtins, "open")

    result = r._save_image("url")
    assert result == "12345.jpg"

