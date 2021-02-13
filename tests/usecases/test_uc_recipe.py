"""Test for the usecases/recipe_uc.py module."""

import builtins
import datetime
import uuid

import pytest

import requests

import pyrecipe.usecases.recipe_uc as ruc
from pyrecipe.usecases.recipe_uc import RecipeUC
from pyrecipe.services import export


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
    assert recipe.images == ["../../static/img/recipe_images/testimg.jpg"]


def test_create_recipe(rec_driver, mocker):
    """
    GIVEN a recipe to create
    WHEN creating it
    THEN assert it is returned
    """
    proc_img_mock = mocker.patch.object(ruc, "process_image")
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
        images=["imagefile1.jpg", "imagefile2.jpg"],
    )
    assert proc_img_mock.call_count == 2
    assert result.name == "test"


def test_edit_recipe(rec_driver):
    """
    GIVEN a recipe to edit
    WHEN submitting new attributes
    THEN assert it is returned with new attributes saved
    """
    r = RecipeUC(rec_driver)
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
    assert result.name == "Newtest"


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
    """
    GIVEN a db with recipes
    WHEN requesting all discrete tags in all recipes
    THEN assert the proper tags and number are returned
    """
    r = RecipeUC(rec_driver)
    result = r.get_tags()
    assert len(result) == 3
    for tag in ["spicy", "slow", "quick"]:
        assert tag in result


def test_delete_recipe_goodID(rec_driver):
    """
    GIVEN a db with recipes
    WHEN requesting to delete a specific recipe
    THEN assert the recipe is marked as deleted
    """
    r = RecipeUC(rec_driver)
    result = r.delete_recipe(recipe_id=123)
    assert result == 1


def test_delete_recipe_badID(rec_driver):
    """
    GIVEN a db with recipes
    WHEN requesting to delete a nonexistent recipe
    THEN assert 0 is returned
    """
    r = RecipeUC(rec_driver)
    result = r.delete_recipe(recipe_id=789)
    assert result == 0


def test_recipes_search(rec_driver, mocker):
    """
    GIVEN a db with recipes
    WHEN the user supplies a search string
    THEN assert the recipes that match are returned
    """
    r = RecipeUC(rec_driver)
    search_mock = mocker.patch.object(r, "recipes_search")
    search_mock.return_value = ["r1", "r2"]
    result = r.recipes_search("spam")
    assert len(result)== 2


def test_export_recipe_fileDoesNotExist(rec_driver, mocker):
    """
    GIVEN a recipe in the DB
    WHEN the user requests to export the recipe for the first time
    THEN assert the correct functions are called
    """
    r = RecipeUC(rec_driver)
    find_mock = mocker.patch.object(r, "find_recipe_by_id")
    date_mock = mocker.patch.object(datetime, "datetime")
    date_mock.strftime.return_value = "filename"
    export_mock = mocker.patch.object(export, "export_to_pdf")
    export_mock.return_value = "/path/to/file"
    result = r.export_recipe("12345")
    assert result == "/path/to/file"
    assert find_mock.call_count == 1
    assert export_mock.call_count == 1


def test_export_recipe_fileAlreadyExists(rec_driver, mocker):
    """
    GIVEN a recipe in the DB
    WHEN the user requests to export the recipe for a already existing file
    THEN assert the correct functions are called but no pdf is recreated
    """
    r = RecipeUC(rec_driver)
    find_mock = mocker.patch.object(r, "find_recipe_by_id")
    date_mock = mocker.patch.object(datetime, "datetime")
    date_mock.strftime.return_value = "filename"
    file_mock = mocker.patch.object(ruc, "EXPORTDIR")
    file_mock.joinpath.return_value.is_file.return_value = True
    export_mock = mocker.patch.object(export, "export_to_pdf")
    export_mock.return_value = "/path/to/file"
    result = r.export_recipe("12345")
    assert find_mock.call_count == 1
    assert export_mock.call_count == 0


def test_import_recipe_from_url(mocker, rec_driver):
    """
    GIVEN a recipe to import via url
    WHEN the url imported
    THEN assert it is sent to the database
    """
    r = RecipeUC(rec_driver)
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


def test_save_image(mocker, rec_driver):
    """
    GIVEN a url-imported recipe with an image url in the data dict
    WHEN importing
    THEN assert the file is also downloaded and saved
    """
    r = RecipeUC(rec_driver)
    req_mock = mocker.patch.object(requests, "get")
    req_mock.return_value.content.return_value = "imagedata"
    uuid_mock = mocker.patch.object(uuid, "uuid4")
    uuid_mock.return_value = "12345"
    file_mock = mocker.patch.object(builtins, "open")

    result = r._save_image("url")
    assert result == "12345.jpg"

